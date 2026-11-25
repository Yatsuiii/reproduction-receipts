"""Rerun a replication package from a clean checkout and write a receipt.

Given a spec (repository, commit, the exact commands, the outputs each command should write), this clones the repository
into an empty directory, checks out the commit, hashes every tracked file, runs each command with a timeout, and compares each
declared output with the committed file of the same path. It writes:

  OUT/results.json       every number behind the receipt, machine-readable
  OUT/RECEIPT.md         the receipt, in a fixed template
  OUT/evidence/          package-files.sha256, environment.json, one log per command, regenerated outputs

What the receipt may call reproduced is narrow on purpose (see fixtures/EXPECTED.json): an output counts only when the run
wrote it, the command that wrote it exited 0, and it equals the committed file byte for byte or number for number within
rel_tol with the same text. An output the run did not write is reported as not rewritten, never as a match, because a
committed result read back is not a recomputation.

Stdlib only, Python 3.10+. It runs package code: run it on a machine where that is acceptable.

usage: python receiptgen/rerun.py SPEC.json --out DIR [--workdir DIR] [--set KEY=VALUE ...]
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FORMAT = "receiptgen-results/1"
NUMBER = re.compile(r"(?<![A-Za-z_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
BANNED = re.compile(r"\b(wrong|incorrect|error in the paper|fails? to replicate)\b", re.I)
REPRODUCED_CLASSES = {"identical", "numbers-match"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sh(args: list, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


# ---------------------------------------------------------------- comparison

def split_numbers(text: str) -> tuple[list, list]:
    """Text with every number replaced by a placeholder, and the numbers with their line numbers."""
    skeleton, numbers, pos = [], [], 0
    for m in NUMBER.finditer(text):
        skeleton.append(text[pos:m.start()])
        skeleton.append("\0")
        numbers.append((text.count("\n", 0, m.start()) + 1, m.group()))
        pos = m.end()
    skeleton.append(text[pos:])
    return skeleton, numbers


def numbers_equal(a: str, b: str, rel_tol: float) -> bool:
    if a == b:
        return True
    try:
        x, y = float(a), float(b)
    except ValueError:
        return False
    return x == y or abs(x - y) <= rel_tol * max(abs(x), abs(y))


def compare(committed: bytes, regenerated: bytes, rel_tol: float) -> dict:
    if committed == regenerated:
        return {"class": "identical"}
    try:
        c_text, r_text = committed.decode("utf-8"), regenerated.decode("utf-8")
    except UnicodeDecodeError:
        return {"class": "binary-differs"}
    c_skel, c_nums = split_numbers(c_text.replace("\r\n", "\n"))
    r_skel, r_nums = split_numbers(r_text.replace("\r\n", "\n"))
    if c_skel != r_skel or len(c_nums) != len(r_nums):
        return {"class": "text-differs", "numbers_committed": len(c_nums), "numbers_regenerated": len(r_nums)}
    diffs = [{"line": cl, "committed": cv, "regenerated": rv}
             for (cl, cv), (_, rv) in zip(c_nums, r_nums) if not numbers_equal(cv, rv, rel_tol)]
    exact = sum(1 for (_, cv), (_, rv) in zip(c_nums, r_nums) if cv == rv)
    out = {"numbers": len(c_nums), "numbers_text_identical": exact, "numbers_differ": len(diffs), "differences": diffs}
    out["class"] = "numbers-differ" if diffs else "numbers-match"
    return out


# ---------------------------------------------------------------- environment

def first_line(args: list) -> str | None:
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (r.stdout or r.stderr).strip()
    return text.splitlines()[0] if text else None


def environment(extra: list) -> dict:
    env = {"platform": platform.platform(), "machine": platform.machine(), "cores": os.cpu_count()}
    try:
        osr = dict(line.split("=", 1) for line in Path("/etc/os-release").read_text().splitlines() if "=" in line)
        env["os"] = osr.get("PRETTY_NAME", "").strip('"')
    except OSError:
        env["os"] = platform.system()
    try:
        cpu = [l.split(":", 1)[1].strip() for l in Path("/proc/cpuinfo").read_text().splitlines() if l.startswith("model name")]
        env["cpu"] = cpu[0] if cpu else platform.processor()
    except OSError:
        env["cpu"] = platform.processor()
    try:
        kb = int(next(l.split()[1] for l in Path("/proc/meminfo").read_text().splitlines() if l.startswith("MemTotal")))
        env["ram_gb"] = round(kb / 1024 / 1024, 1)
    except (OSError, StopIteration):
        env["ram_gb"] = None
    env["gpu"] = first_line(["nvidia-smi", "-L"]) if shutil.which("nvidia-smi") else "none"
    tools = {"git": ["git", "--version"], "python3": ["python3", "--version"], "R": ["R", "--version"],
             "julia": ["julia", "--version"], "stata": ["stata-mp", "-q", "-b", "about"], "matlab": ["matlab", "-batch", "version"]}
    env["tools"] = {k: first_line(v) for k, v in tools.items() if shutil.which(v[0])}
    env["extra"] = {}
    for item in extra:
        env["extra"][item["id"]] = subprocess.run(item["cmd"], shell=True, capture_output=True, text=True).stdout
    return env


# ---------------------------------------------------------------- running

def run_command(cmd: dict, clone: Path, logdir: Path) -> dict:
    cwd = clone / cmd.get("cwd", ".")
    timeout = cmd.get("timeout_s", 3600)
    log = logdir / f"{cmd['id']}.log"
    start, t0 = now(), time.monotonic()
    with open(log, "w", encoding="utf-8") as fh:
        fh.write(f"# command: {cmd['cmd']}\n# cwd: {cmd.get('cwd', '.')}\n# start: {start}\n# timeout_s: {timeout}\n")
        fh.flush()
        proc = subprocess.Popen(["bash", "-c", cmd["cmd"]], cwd=cwd, stdout=fh, stderr=subprocess.STDOUT,
                                start_new_session=True, env={**os.environ, **cmd.get("env", {})})
        try:
            code = proc.wait(timeout=timeout)
            outcome = "exit0" if code == 0 else "failed"
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            code = proc.wait()
            outcome = "timeout"
        seconds = round(time.monotonic() - t0, 2)
        end = now()
        fh.write(f"\n# end: {end}\n# exit: {code}\n# seconds: {seconds}\n# outcome: {outcome}\n")
    return {"id": cmd["id"], "cmd": cmd["cmd"], "cwd": cmd.get("cwd", "."), "timeout_s": timeout, "start": start, "end": end,
            "exit_code": code, "seconds": seconds, "outcome": outcome, "log": f"evidence/logs/{log.name}"}


def expand_outputs(items: list, tracked: list, hash_only: set) -> list:
    """Outputs are paths, or {"glob": ..., "compare": "hash-only"} for files such as PDF figures whose bytes carry
    metadata. A glob is expanded against the committed tree, so it names only files there is something to compare with."""
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(item)
            continue
        paths = [t for t in tracked if fnmatch.fnmatch(t, item["glob"])] if "glob" in item else [item["path"]]
        if item.get("compare") == "hash-only":
            hash_only.update(paths)
        out.extend(p for p in sorted(paths) if p not in out)
    return out


def snapshot(path: Path) -> tuple | None:
    if not path.is_file():
        return None
    st = path.stat()
    return (st.st_mtime_ns, st.st_ino, sha256_bytes(path.read_bytes()))


def rerun(spec: dict, out: Path, workdir: Path | None = None) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    ev = out / "evidence"
    (ev / "logs").mkdir(parents=True, exist_ok=True)
    (ev / "outputs").mkdir(parents=True, exist_ok=True)
    rel_tol = float(spec.get("compare", {}).get("rel_tol", 1e-12))
    res = {"format": FORMAT, "spec": spec, "started": now(), "status": "ran", "flags": [], "commands": [], "outputs": {},
           "reproduced": []}
    own_tmp = workdir is None
    work = Path(tempfile.mkdtemp(prefix="receiptgen-")) if own_tmp else workdir
    clone = work / "checkout"
    try:
        r = sh(["git", "clone", "--quiet", "--no-checkout", spec["repo"], str(clone)])
        if r.returncode != 0:
            res.update(status="aborted", abort_reason=f"git clone failed: {r.stderr.strip()}")
            res["flags"].append("CLONE_FAILED")
            return finish(res, out, spec)
        r = sh(["git", "checkout", "--quiet", spec["commit"]], cwd=clone)
        head = sh(["git", "rev-parse", "HEAD"], cwd=clone).stdout.strip()
        if r.returncode != 0 or not head.startswith(spec["commit"]):
            res.update(status="aborted", abort_reason=f"commit {spec['commit']} was not found in {spec['repo']}")
            res["flags"].append("COMMIT_NOT_FOUND")
            return finish(res, out, spec)
        res["commit"] = head
        tracked = sh(["git", "ls-files", "-z"], cwd=clone).stdout.split("\0")
        tracked = [t for t in tracked if t and (clone / t).is_file()]
        lines = [f"{sha256_bytes((clone / t).read_bytes())}  {t}" for t in sorted(tracked)]
        (ev / "package-files.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
        res["package_files"] = len(lines)
        res["package_files_sha256"] = sha256_bytes(("\n".join(lines) + "\n").encode())
        res["environment"] = environment(spec.get("environment_commands", []))
        hash_only = set()
        for c in spec["commands"]:
            c["outputs"] = expand_outputs(c.get("outputs", []), tracked, hash_only)
        declared = {o for c in spec["commands"] for o in c["outputs"]}
        tracked_set = set(tracked)
        for cmd in spec.get("setup", []) + spec["commands"]:
            outputs = cmd.get("outputs", [])
            before = {o: snapshot(clone / o) for o in outputs}
            c = run_command(cmd, clone, ev / "logs")
            c["setup"] = cmd in spec.get("setup", [])
            res["commands"].append(c)
            changed = [l[3:] for l in sh(["git", "status", "--porcelain", "--untracked-files=no"], cwd=clone).stdout.splitlines()]
            undeclared = sorted(p for p in changed if p not in declared)
            if undeclared and not c["setup"]:
                c["undeclared_tracked_changes"] = undeclared
                if "UNDECLARED_TRACKED_CHANGE" not in res["flags"]:
                    res["flags"].append("UNDECLARED_TRACKED_CHANGE")
            for o in outputs:
                after = snapshot(clone / o)
                committed = sh(["git", "cat-file", "-e", f"HEAD:{o}"], cwd=clone).returncode == 0
                rewritten = after is not None and after != before[o]
                entry = {"command": cmd["id"], "committed": committed, "rewritten": rewritten}
                if after is None:
                    entry["class"] = "missing"
                elif not rewritten:
                    entry["class"] = "not-rewritten" if committed else "missing"
                else:
                    regenerated = (clone / o).read_bytes()
                    dest = ev / "outputs" / o
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(regenerated)
                    entry["sha256"] = sha256_bytes(regenerated)
                    if o in hash_only:
                        entry["class"] = "rewritten-not-compared"
                    elif not committed:
                        entry["class"] = "no-reference"
                    else:
                        blob = subprocess.run(["git", "show", f"HEAD:{o}"], cwd=clone, capture_output=True).stdout
                        entry["committed_sha256"] = sha256_bytes(blob)
                        entry.update(compare(blob, regenerated, rel_tol))
                    if c["outcome"] != "exit0" and "OUTPUT_FROM_FAILED_COMMAND" not in res["flags"]:
                        res["flags"].append("OUTPUT_FROM_FAILED_COMMAND")
                entry["reproduced"] = c["outcome"] == "exit0" and rewritten and entry["class"] in REPRODUCED_CLASSES
                res["outputs"][o] = entry
                if entry["reproduced"]:
                    res["reproduced"].append(o)
        res["untracked_after"] = len(sh(["git", "ls-files", "--others", "--exclude-standard"], cwd=clone).stdout.splitlines())
        res["tracked_not_declared_ok"] = sorted(tracked_set & declared)
        return finish(res, out, spec)
    finally:
        if own_tmp and not spec.get("keep_workdir"):
            shutil.rmtree(work, ignore_errors=True)


def finish(res: dict, out: Path, spec: dict) -> dict:
    res["finished"] = now()
    secs = sum(c["seconds"] for c in res["commands"])
    res["wall_clock_seconds"] = round(secs, 2)
    rate = spec.get("cost_per_hour_usd")
    res["cost_usd"] = round(secs / 3600 * rate, 4) if rate is not None else None
    (out / "results.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    if res.get("environment"):
        (out / "evidence" / "environment.json").write_text(json.dumps(res["environment"], indent=1) + "\n", encoding="utf-8")
    text = render(res)
    bad = BANNED.findall(text)
    if bad:
        raise SystemExit(f"receipt text uses banned wording {bad}; fix the spec's free text")
    (out / "RECEIPT.md").write_text(text, encoding="utf-8")
    return res


# ---------------------------------------------------------------- receipt

CLASS_WORDS = {
    "identical": "identical to the committed file",
    "numbers-match": "every number equal to the committed file within the tolerance; bytes differ",
    "numbers-differ": "did not regenerate the committed values",
    "text-differs": "text differs from the committed file",
    "binary-differs": "binary file differs from the committed file",
    "not-rewritten": "not written by this run, so not compared",
    "missing": "not produced",
    "no-reference": "produced; nothing committed to compare with",
    "rewritten-not-compared": "rewritten; hashed only, not compared (declared hash-only in the spec)",
}


def fmt_secs(s: float) -> str:
    s = int(round(s))
    return f"{s // 3600} h {s % 3600 // 60} min" if s >= 3600 else (f"{s // 60} min {s % 60} s" if s >= 60 else f"{s} s")


def headline(res: dict) -> str:
    if res["status"] == "aborted":
        return f"Not run. {res['abort_reason']}. No package code ran."
    cmds = [c for c in res["commands"] if not c["setup"]]
    ok = sum(c["outcome"] == "exit0" for c in cmds)
    outs = res["outputs"]
    n = len(outs)
    by = {k: [o for o, e in outs.items() if e["class"] == k] for k in CLASS_WORDS}
    parts = [f"{ok} of {len(cmds)} commands exited 0.",
             f"{len(res['reproduced'])} of {n} declared outputs reproduced"]
    sub = []
    ident = sum(1 for o in res["reproduced"] if outs[o]["class"] == "identical")
    if ident:
        sub.append(f"{ident} byte-identical")
    if len(res["reproduced"]) - ident:
        sub.append(f"{len(res['reproduced']) - ident} equal in every number within {res['spec'].get('compare', {}).get('rel_tol', 1e-12)} relative")
    parts[-1] += f" ({', '.join(sub)})." if sub else "."
    differ = by["numbers-differ"] + by["text-differs"] + by["binary-differs"]
    if differ:
        nvals = sum(outs[o].get("numbers_differ", 0) for o in by["numbers-differ"])
        tail = f", {nvals} value{'s' if nvals != 1 else ''} in all" if nvals else ""
        parts.append(f"{len(differ)} did not regenerate the committed file{tail}; the committed materials did not reproduce "
                     f"those values here, reason unknown.")
    if by["not-rewritten"]:
        parts.append(f"{len(by['not-rewritten'])} were not written by the run, so they are not counted.")
    if by["rewritten-not-compared"]:
        parts.append(f"{len(by['rewritten-not-compared'])} (figures or other files declared hash-only) were rewritten and "
                     f"hashed, not compared.")
    if by["missing"]:
        parts.append(f"{len(by['missing'])} were not produced.")
    if by["no-reference"]:
        parts.append(f"{len(by['no-reference'])} had nothing committed to compare with.")
    return " ".join(parts)


def render(res: dict) -> str:
    spec = res["spec"]
    L = [f"# Receipt: {spec.get('title', spec['repo'])}", ""]
    date = res["finished"][:16].replace("T", " ") + " UTC"
    L += [f"**Status, {date}: {headline(res)}**", ""]
    if spec.get("unasked", True):
        L += ["This was done unasked, by someone with no connection to the authors or the journal. It says what the committed",
              "materials did on this machine. It does not say anything about whether the paper is right.", ""]
    L += ["## What was checked", ""]
    L.append(f"- Package: {spec.get('package_label', spec['repo'])}, commit `{res.get('commit', spec['commit'])}`.")
    if spec.get("paper"):
        L.append(f"- Paper: {spec['paper']}.")
    if res["status"] == "ran":
        L.append(f"- {res['package_files']} tracked files, each hashed in [`evidence/package-files.sha256`]"
                 f"(evidence/package-files.sha256) (SHA-256 of that list `{res['package_files_sha256'][:16]}…`).")
    if spec.get("protocol"):
        L.append(f"- Protocol and comparison rule, committed before any package code ran: [`{spec['protocol']}`]({spec['protocol']}).")
    L.append(f"- Comparison: each declared output, after the run, against the committed file of the same path. Numbers are "
             f"compared one by one with relative tolerance {spec.get('compare', {}).get('rel_tol', 1e-12)}; all other text "
             f"must be identical.")
    for note in spec.get("scope_notes", []):
        L.append(f"- {note}")
    L.append("")
    if res["status"] == "aborted":
        L += ["## Result", "", f"Nothing ran: {res['abort_reason']}. No package code ran, so no output is compared.", ""]
    else:
        L += ["## Result", "", "| Command | Exit | Time | Output | Outcome | Reproduced |", "|---|---|---|---|---|---|"]
        for c in res["commands"]:
            if c["setup"]:
                continue
            outs = [(o, e) for o, e in res["outputs"].items() if e["command"] == c["id"]] or [("(none declared)", None)]
            for i, (o, e) in enumerate(outs):
                first = i == 0
                exit_txt = (str(c["exit_code"]) if c["outcome"] != "timeout" else f"killed at {c['timeout_s']} s") if first else ""
                outcome = ""
                if e:
                    outcome = CLASS_WORDS[e["class"]]
                    if e["class"] == "numbers-differ":
                        outcome += f": {e['numbers_differ']} of {e['numbers']} numbers"
                    elif e["class"] == "numbers-match":
                        outcome += f" ({e['numbers_text_identical']} of {e['numbers']} numbers identical text)"
                    if e.get("rewritten") and c["outcome"] != "exit0":
                        outcome += "; written by a command that did not exit 0"
                L.append(f"| {'`' + c['cmd'] + '`' if first else ''} | {exit_txt} | {fmt_secs(c['seconds']) if first else ''} "
                         f"| `{o}` | {outcome} | {('yes' if e['reproduced'] else 'no') if e else ''} |")
        L.append("")
        differ = [(o, e) for o, e in res["outputs"].items() if e["class"] == "numbers-differ"]
        if differ:
            L += ["### Values that did not regenerate", "",
                  "The committed materials did not reproduce these values on this machine, reason unknown. Line numbers are lines "
                  "of the output file. The full list is in `results.json`.", "",
                  "| Output | Line | Committed | Regenerated |", "|---|---|---|---|"]
            for o, e in differ:
                for d in e["differences"][:40]:
                    L.append(f"| `{o}` | {d['line']} | {d['committed']} | {d['regenerated']} |")
                if len(e["differences"]) > 40:
                    L.append(f"| `{o}` | … | {len(e['differences']) - 40} more in `results.json` | |")
            L.append("")
        replay = [o for o, e in res["outputs"].items() if e["class"] == "not-rewritten"]
        if replay:
            L += [f"Not written by this run: {', '.join('`' + o + '`' for o in replay)}. A committed file that the run leaves "
                  "untouched may be read back rather than recomputed, so it counts for nothing here.", ""]
    for section in spec.get("extra_sections", []):
        L += [f"## {section['heading']}", "", section["body"].rstrip(), ""]
    if res["status"] == "ran":
        env = res["environment"]
        L += ["## Environment", "", "| | |", "|---|---|",
              f"| OS | {env.get('os')} |", f"| CPU | {env.get('cpu')} |", f"| Cores | {env.get('cores')} |",
              f"| RAM | {env.get('ram_gb')} GB |", f"| GPU | {env.get('gpu')} |"]
        for k, v in env.get("tools", {}).items():
            L.append(f"| {k} | {v} |")
        L.append("")
        if env.get("extra"):
            L.append("Full environment listings: [`evidence/environment.json`](evidence/environment.json).")
            L.append("")
        L += ["## Wall clock and cost", ""]
        L.append(f"Commands ran for {fmt_secs(res['wall_clock_seconds'])} in all, one after another, from {res['started']} to "
                 f"{res['finished']}.")
        if res["cost_usd"] is not None:
            L.append(f"At {spec['cost_per_hour_usd']} USD an hour for this machine ({spec.get('cost_basis', 'stated rate')}), "
                     f"that is about {res['cost_usd']:.2f} USD.")
        L.append("")
    L += ["## Deviations, in order", ""]
    devs = list(spec.get("deviations", []))
    for c in res["commands"]:
        if c.get("undeclared_tracked_changes"):
            devs.append(f"`{c['cmd']}` changed tracked files that are not declared outputs: "
                        + ", ".join(f"`{p}`" for p in c["undeclared_tracked_changes"]) + ".")
    if "OUTPUT_FROM_FAILED_COMMAND" in res["flags"]:
        devs.append("At least one output was written by a command that did not exit 0. It is listed but not counted as reproduced.")
    L += [f"{i}. {d}" for i, d in enumerate(devs, 1)] if devs else ["None. No package file was edited before or between commands."]
    L.append("")
    L += ["## Failed, stopped or killed runs", ""]
    bad = [c for c in res["commands"] if c["outcome"] != "exit0"]
    if bad:
        for i, c in enumerate(bad, 1):
            what = f"killed at the {c['timeout_s']} s limit" if c["outcome"] == "timeout" else f"exit {c['exit_code']}"
            L.append(f"{i}. `{c['cmd']}`: {what} after {fmt_secs(c['seconds'])}. [Log]({c['log']}).")
    else:
        L.append("None." if res["status"] == "ran" else "None; nothing ran.")
    L.append("")
    L += ["## Evidence", "", "- [`results.json`](results.json): every number above, with each command's start, end and exit code.",
          "- [`evidence/logs/`](evidence/logs/): stdout and stderr of every command."]
    if res["status"] == "ran":
        L.append("- [`evidence/outputs/`](evidence/outputs/): every output this run wrote.")
    L.append(f"- Generated by `receiptgen/rerun.py` from the spec in `results.json`.")
    L.append("")
    return "\n".join(L)


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir")
    ap.add_argument("--set", action="append", default=[], help="KEY=VALUE substituted for {{KEY}} in the spec text")
    a = ap.parse_args(argv)
    text = Path(a.spec).read_text(encoding="utf-8")
    for kv in a.set:
        k, v = kv.split("=", 1)
        text = text.replace("{{" + k + "}}", v)
    res = rerun(json.loads(text), Path(a.out), Path(a.workdir) if a.workdir else None)
    print(headline(res))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
