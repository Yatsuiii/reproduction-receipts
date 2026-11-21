"""Batch runner: does a stdio MCP server leave processes behind after the
client shuts it down the way the MCP spec says to?

    python mcp-teardown/runner.py --targets mcp-teardown/targets.jsonl --workers 4

What one trial does, for one published package:

1. Launch the package's own entry point directly (never through npx or uvx,
   so a wrapper's behaviour is not blamed on the server), as user `nobody`,
   with no network (`unshare --net`), an empty environment plus a trial tag,
   in its own session.
2. Complete a real MCP handshake: initialize, notifications/initialized,
   tools/list. A server that does not answer is DEAD, not a finding.
3. Shut it down with the stdio sequence from the MCP lifecycle spec: close
   stdin, wait, SIGTERM, wait, SIGKILL.
4. Wait SETTLE_S, then list every live process still carrying the trial tag.
   The tag is inherited through fork and exec and survives reparenting, which
   is why it is used instead of process ancestry (see
   agent-disclosure-fidelity/README.md).

Arms. Arm `pid` sends the signals to the server's pid only, which is what a
client that follows the spec literally does. Arm `group` sends the same
signals to the server's whole process group. Nothing else differs between
the arms. A target is CONFIRMED only when `pid` leaves residue in 10 of 10
trials and `group` leaves none in 10 of 10. Anything in between is kept in
the results with its counts but gets no receipt.

Arming. Before any target runs, the batch runs its own control fixtures
(fixtures/control_server.mjs). The leaky control must be CONFIRMED, the clean
control must pass 10 of 10, and a probe for a tag nobody carries must return
nothing. If any of that fails the batch stops and reports nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import queue
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAG_ENV = "SHUTDOWN_INTEGRITY_TRIAL"
NOBODY = 65534
PLACEHOLDER = "placeholder-not-a-real-credential"

HANDSHAKE_TIMEOUT_S = 30.0
EOF_WAIT_S = 2.0
TERM_WAIT_S = 2.0
SETTLE_S = 5.0
CONFIRM_TRIALS = 10
INSTALL_TIMEOUT_S = 300


# --------------------------------------------------------------------- probe

def _stat(pid: str) -> list[str]:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        return []
    return raw.rpartition(")")[2].split()


def tagged_processes(tag: str) -> list[dict]:
    """Live, non-zombie processes whose environ carries TAG_ENV=tag."""
    needle = f"{TAG_ENV}={tag}".encode()
    found = []
    for entry in Path("/proc").iterdir():
        pid = entry.name
        if not pid.isdigit():
            continue
        try:
            env = (entry / "environ").read_bytes()
        except OSError:
            continue
        if needle not in env.split(b"\0"):
            continue
        st = _stat(pid)
        if not st or st[0] == "Z":
            continue
        try:
            cmd = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace").strip()
        except OSError:
            cmd = ""
        found.append({"pid": int(pid), "ppid": int(st[1]), "state": st[0], "cmdline": cmd[:300]})
    return found


def kill_tagged(tag: str) -> None:
    for _ in range(20):
        procs = tagged_processes(tag)
        if not procs:
            return
        for p in procs:
            try:
                os.kill(p["pid"], signal.SIGKILL)
            except ProcessLookupError:
                pass
        time.sleep(0.1)


# ------------------------------------------------------------------- install

@dataclass
class Install:
    ok: bool
    reason: str = ""
    argv: list[str] = field(default_factory=list)
    path_dirs: list[str] = field(default_factory=list)
    artefact: dict = field(default_factory=dict)
    log: str = ""


def _run(cmd: list[str], timeout: float, **kw) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)
        return p.returncode, (p.stdout + p.stderr)[-20000:]
    except subprocess.TimeoutExpired as e:
        return -1, f"timeout after {timeout}s: {e}"


def install_npm(t: dict, root: Path) -> Install:
    spec = f"{t['identifier']}@{t['package_version']}" if t.get("package_version") else t["identifier"]
    pkg_dir = root / "pkg"
    pkg_dir.mkdir(parents=True)
    # --ignore-scripts: no package code runs at install time, outside the sandbox.
    cmd = ["npm", "install", "--prefix", str(pkg_dir), "--ignore-scripts", "--no-audit", "--no-fund",
           "--omit=dev", "--loglevel=error", spec]
    rc, log = _run(cmd, INSTALL_TIMEOUT_S)
    if rc != 0:
        return Install(False, "npm install failed", log=f"$ {' '.join(cmd)}\n{log}")
    mod = pkg_dir / "node_modules" / t["identifier"]
    try:
        meta = json.loads((mod / "package.json").read_text())
    except OSError:
        return Install(False, "installed package has no package.json", log=log)
    bins = meta.get("bin")
    if isinstance(bins, str):
        bins = {meta.get("name", t["identifier"]).split("/")[-1]: bins}
    if not bins:
        return Install(False, "package declares no bin entry point", log=log)
    short = t["identifier"].split("/")[-1]
    if len(bins) == 1:
        name, rel = next(iter(bins.items()))
    elif short in bins:
        name, rel = short, bins[short]
    else:
        return Install(False, f"ambiguous bin entry points: {sorted(bins)}", log=log)
    entry = (mod / rel).resolve()
    lock = {}
    try:
        lock = json.loads((pkg_dir / "package-lock.json").read_text())["packages"][f"node_modules/{t['identifier']}"]
    except (OSError, KeyError, ValueError):
        pass
    node = shutil.which("node")
    head = entry.read_bytes()[:200] if entry.exists() else b""
    is_js = entry.suffix in (".js", ".mjs", ".cjs") or b"node" in head.split(b"\n")[0]
    argv = ([node, str(entry)] if is_js else [str(entry)]) + list(t.get("package_args") or [])
    return Install(True, argv=argv, path_dirs=[str(Path(node).parent)], log=f"$ {' '.join(cmd)}\n{log}",
                   artefact={"registry": "npm", "spec": spec, "resolved_version": meta.get("version"),
                             "bin": name, "integrity": lock.get("integrity"), "resolved": lock.get("resolved")})


def _pypi_digests(name: str, version: str | None) -> list[dict]:
    if not version:
        return []
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=30) as r:
            data = json.load(r)
        return [{"filename": u["filename"], "sha256": u["digests"]["sha256"]} for u in data.get("urls", [])]
    except (OSError, ValueError, KeyError):
        return []


def install_pypi(t: dict, root: Path) -> Install:
    venv = root / "venv"
    spec = f"{t['identifier']}=={t['package_version']}" if t.get("package_version") else t["identifier"]
    log = ""
    for cmd in (["uv", "venv", "-q", "--python", sys.executable, str(venv)],
                # wheels only: building an sdist would run package code outside the sandbox
                ["uv", "pip", "install", "-q", "--python", str(venv / "bin" / "python"), "--only-binary", ":all:", spec]):
        rc, out = _run(cmd, INSTALL_TIMEOUT_S)
        log += f"$ {' '.join(cmd)}\n{out}\n"
        if rc != 0:
            return Install(False, "uv install failed (wheels only)", log=log)
    probe = ("import importlib.metadata as m,json,sys;d=m.distribution(sys.argv[1]);"
             "print(json.dumps([[e.name,e.value] for e in d.entry_points if e.group=='console_scripts']+[['__version__',d.version]]))")
    rc, out = _run([str(venv / "bin" / "python"), "-I", "-c", probe, t["identifier"]], 60)
    try:
        pairs = json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return Install(False, "could not read entry points", log=log + out)
    version = dict(pairs).pop("__version__", None)
    scripts = [n for n, _ in pairs if n != "__version__"]
    norm = lambda s: re.sub(r"[-_.]+", "-", s).lower()
    if len(scripts) == 1:
        name = scripts[0]
    else:
        match = [s for s in scripts if norm(s) == norm(t["identifier"])]
        if len(match) != 1:
            return Install(False, f"ambiguous or missing console scripts: {scripts}", log=log)
        name = match[0]
    argv = [str(venv / "bin" / name)] + list(t.get("package_args") or [])
    return Install(True, argv=argv, path_dirs=[str(venv / "bin")], log=log,
                   artefact={"registry": "pypi", "spec": spec, "resolved_version": version, "console_script": name,
                             "published_files": _pypi_digests(t["identifier"], t.get("package_version"))})


def install_control(mode: str, root: Path) -> Install:
    node = shutil.which("node")
    fixture = root / "control_server.mjs"
    shutil.copy(HERE / "fixtures" / "control_server.mjs", fixture)
    digest = hashlib.sha256(fixture.read_bytes()).hexdigest()
    return Install(True, argv=[node, str(fixture), mode], path_dirs=[str(Path(node).parent)],
                   artefact={"registry": "control", "fixture_sha256": digest, "mode": mode})


# --------------------------------------------------------------------- trial

@dataclass
class Trial:
    arm: str
    tag: str
    handshake_ok: bool = False
    handshake_error: str = ""
    server_name: str = ""
    tool_count: int | None = None
    exit_stage: str = ""
    teardown_return_s: float | None = None
    residuals: list[dict] = field(default_factory=list)
    # Tagged processes alive just before shutdown, server included. A server
    # that never starts a child cannot leave one behind, so this is the
    # denominator that a clean result should be read against.
    live_before_shutdown: int | None = None
    stdout_noise_lines: int = 0
    stdout_noise_sample: list[str] = field(default_factory=list)


def _reader(stream, q: queue.Queue) -> None:
    for line in iter(stream.readline, b""):
        q.put(line)
    q.put(None)


def _await_response(q: queue.Queue, want_id: int, deadline: float, trial: Trial) -> dict | None:
    while True:
        left = deadline - time.monotonic()
        if left <= 0:
            return None
        try:
            line = q.get(timeout=left)
        except queue.Empty:
            return None
        if line is None:
            return None
        try:
            msg = json.loads(line)
        except ValueError:
            trial.stdout_noise_lines += 1
            if len(trial.stdout_noise_sample) < 5:
                trial.stdout_noise_sample.append(line[:200].decode("utf-8", "replace").rstrip())
            continue
        if isinstance(msg, dict) and msg.get("id") == want_id:
            return msg


def run_trial(inst: Install, t: dict, root: Path, arm: str, stderr_path: Path) -> Trial:
    tag = f"mcpt-{uuid.uuid4().hex[:16]}"
    trial = Trial(arm=arm, tag=tag)
    home = root / "home"
    tmp = root / "tmp"
    home.mkdir(exist_ok=True)
    tmp.mkdir(exist_ok=True)
    env = {"PATH": ":".join(inst.path_dirs + ["/usr/local/bin", "/usr/bin", "/bin"]),
           "HOME": str(home), "TMPDIR": str(tmp), "LANG": "C.UTF-8", TAG_ENV: tag}
    env.update(t.get("default_env") or {})
    for name in t.get("required_env") or []:
        env[name] = PLACEHOLDER
    sandbox = ["unshare", "--net", "--", "setpriv", f"--reuid={NOBODY}", f"--regid={NOBODY}", "--clear-groups", "--"]
    with open(stderr_path, "ab") as err:
        err.write(f"\n=== trial {tag} arm={arm}\n".encode())
        err.flush()
        proc = subprocess.Popen(sandbox + inst.argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err,
                                env=env, cwd=str(home), start_new_session=True)
    q: queue.Queue = queue.Queue()
    threading.Thread(target=_reader, args=(proc.stdout, q), daemon=True).start()

    def send(msg: dict) -> None:
        proc.stdin.write((json.dumps(msg) + "\n").encode())
        proc.stdin.flush()

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "teardown-receipt-runner", "version": "0.1.0"}}})
        resp = _await_response(q, 1, time.monotonic() + HANDSHAKE_TIMEOUT_S, trial)
        if not resp or "result" not in resp:
            trial.handshake_error = "no initialize result" if not resp else f"initialize error: {resp.get('error')}"
        else:
            trial.server_name = str((resp["result"].get("serverInfo") or {}).get("name", ""))
            send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
            tl = _await_response(q, 2, time.monotonic() + 15, trial)
            if tl and "result" in tl:
                trial.handshake_ok = True
                trial.tool_count = len(tl["result"].get("tools") or [])
            else:
                trial.handshake_error = "no tools/list result"
        time.sleep(1.0)
        trial.live_before_shutdown = len(tagged_processes(tag))
    except (BrokenPipeError, OSError) as e:
        trial.handshake_error = f"pipe closed during handshake: {e}"

    # Spec stdio shutdown. The only difference between arms is the signal target.
    def signal_target(sig: int) -> None:
        try:
            if arm == "group":
                os.killpg(proc.pid, sig)
            else:
                os.kill(proc.pid, sig)
        except ProcessLookupError:
            pass

    t0 = time.monotonic()
    try:
        proc.stdin.close()
    except OSError:
        pass
    try:
        proc.wait(EOF_WAIT_S)
        trial.exit_stage = "exited_on_stdin_eof"
    except subprocess.TimeoutExpired:
        signal_target(signal.SIGTERM)
        try:
            proc.wait(TERM_WAIT_S)
            trial.exit_stage = "exited_on_sigterm"
        except subprocess.TimeoutExpired:
            signal_target(signal.SIGKILL)
            proc.wait()
            trial.exit_stage = "needed_sigkill"
    trial.teardown_return_s = round(time.monotonic() - t0, 3)
    time.sleep(SETTLE_S)
    trial.residuals = tagged_processes(tag)
    kill_tagged(tag)
    return trial


# -------------------------------------------------------------------- target

def slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)[:120]


def run_target(t: dict, work: Path, out_dir: Path, keep: bool = False) -> dict:
    started = time.time()
    tdir = out_dir / slug(t["name"])
    tdir.mkdir(parents=True, exist_ok=True)
    root = work / f"{slug(t['name'])}-{uuid.uuid4().hex[:6]}"
    root.mkdir(parents=True)
    result: dict = {"target": t, "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started))}
    try:
        kind = t["registry_type"]
        if kind == "npm":
            inst = install_npm(t, root)
        elif kind == "pypi":
            inst = install_pypi(t, root)
        elif kind == "control":
            inst = install_control(t["identifier"], root)
        else:
            inst = Install(False, f"unsupported registry {kind}")
        (tdir / "install.log").write_text(inst.log)
        result["install"] = {"ok": inst.ok, "reason": inst.reason, "argv": inst.argv, "artefact": inst.artefact}
        if not inst.ok:
            result["verdict"] = "DEAD"
            result["reason"] = inst.reason
            return result
        # HOME and TMPDIR must exist before the chown, or the server cannot write
        # to its own home (first full run, 2026-11-21, lost targets to this).
        (root / "home").mkdir(exist_ok=True)
        (root / "tmp").mkdir(exist_ok=True)
        subprocess.run(["chown", "-R", f"{NOBODY}:{NOBODY}", str(root)], check=False)
        stderr_path = tdir / "server-stderr.log"
        trials: list[Trial] = []
        screen = run_trial(inst, t, root, "pid", stderr_path)
        trials.append(screen)
        if not screen.handshake_ok:
            result["verdict"] = "DEAD"
            result["reason"] = f"handshake failed: {screen.handshake_error}" + (
                f" ({screen.stdout_noise_lines} non-JSON stdout lines)" if screen.stdout_noise_lines else "")
        elif not screen.residuals:
            result["verdict"] = "PASS_SCREEN"
        else:
            for arm in ("pid", "group"):
                for _ in range(CONFIRM_TRIALS):
                    trials.append(run_trial(inst, t, root, arm, stderr_path))
            conf = trials[1:]
            pid = [x for x in conf if x.arm == "pid"]
            grp = [x for x in conf if x.arm == "group"]
            live = all(x.handshake_ok for x in conf)
            pid_leaks = sum(bool(x.residuals) for x in pid)
            grp_leaks = sum(bool(x.residuals) for x in grp)
            result["counts"] = {"pid_trials": len(pid), "pid_with_residue": pid_leaks,
                                "group_trials": len(grp), "group_with_residue": grp_leaks,
                                "all_handshakes_ok": live}
            if live and pid_leaks == len(pid) and grp_leaks == 0:
                result["verdict"] = "CONFIRMED"
            elif live and pid_leaks == len(pid) and grp_leaks == len(grp):
                result["verdict"] = "RESIDUE_BOTH_ARMS"
            else:
                result["verdict"] = "UNCONFIRMED"
        result["trials"] = [asdict(x) for x in trials]
        return result
    except Exception as e:  # a crash in one target must not stop the batch
        result["verdict"] = "RUNNER_ERROR"
        result["reason"] = f"{type(e).__name__}: {e}"
        return result
    finally:
        result["wall_clock_s"] = round(time.time() - started, 1)
        (tdir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True))
        if not keep and result.get("verdict") not in ("CONFIRMED",):
            shutil.rmtree(root, ignore_errors=True)


# ------------------------------------------------------------------- arming

def arm(work: Path, out_dir: Path) -> dict:
    checks = {}
    bogus = f"mcpt-never-{uuid.uuid4().hex}"
    checks["negative_probe_empty"] = tagged_processes(bogus) == []
    leaky = run_target({"name": "control.leaky", "registry_type": "control", "identifier": "leaky"},
                       work, out_dir / "_controls")
    checks["leaky_control_confirmed"] = leaky.get("verdict") == "CONFIRMED"
    clean_t = {"name": "control.clean", "registry_type": "control", "identifier": "clean"}
    root = work / "control-clean"
    root.mkdir(parents=True, exist_ok=True)
    inst = install_control("clean", root)
    subprocess.run(["chown", "-R", f"{NOBODY}:{NOBODY}", str(root)], check=False)
    (out_dir / "_controls" / "control.clean").mkdir(parents=True, exist_ok=True)
    clean_trials = [run_trial(inst, clean_t, root, "pid", out_dir / "_controls" / "control.clean" / "server-stderr.log")
                    for _ in range(CONFIRM_TRIALS)]
    checks["clean_control_pass"] = all(x.handshake_ok and not x.residuals for x in clean_trials)
    (out_dir / "_controls" / "control.clean" / "result.json").write_text(
        json.dumps([asdict(x) for x in clean_trials], indent=2))
    checks["armed"] = all(checks.values())
    return checks


# ---------------------------------------------------------------------- main

def environment() -> dict:
    def ver(cmd):
        rc, out = _run(cmd, 30)
        return out.strip().splitlines()[0] if rc == 0 and out.strip() else None
    cpu = ""
    try:
        cpu = next(l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name"))
    except (OSError, StopIteration):
        pass
    mem_kb = 0
    try:
        mem_kb = int(next(l.split()[1] for l in open("/proc/meminfo") if l.startswith("MemTotal")))
    except (OSError, StopIteration):
        pass
    return {"os": platform.platform(), "kernel": platform.release(), "cpu": cpu, "cpus": os.cpu_count(),
            "mem_gb": round(mem_kb / 1048576, 1), "python": platform.python_version(),
            "node": ver(["node", "-v"]), "npm": ver(["npm", "-v"]), "uv": ver(["uv", "--version"]),
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "timeouts": {"handshake_s": HANDSHAKE_TIMEOUT_S, "eof_wait_s": EOF_WAIT_S,
                         "term_wait_s": TERM_WAIT_S, "settle_s": SETTLE_S, "confirm_trials": CONFIRM_TRIALS}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", type=Path, default=HERE / "targets.jsonl")
    ap.add_argument("--out", type=Path, default=None, help="results dir (default results/<run id>)")
    ap.add_argument("--work", type=Path, default=Path("/var/tmp/mcp-teardown-work"))
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args(argv)
    if os.geteuid() != 0:
        print("needs root: unshare --net and dropping to nobody", file=sys.stderr)
        return 2

    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out_dir = args.out or HERE / "results" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    os.chmod(args.work, 0o755)
    targets = [json.loads(l) for l in args.targets.read_text().splitlines() if l.strip()]
    targets = targets[args.offset: None if args.limit is None else args.offset + args.limit]
    run = {"run_id": run_id, "targets_file": str(args.targets),
           "targets_sha256": hashlib.sha256(args.targets.read_bytes()).hexdigest(),
           "n_targets": len(targets), "environment": environment(),
           "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    t0 = time.time()
    run["arming"] = arm(args.work, out_dir)
    print(f"arming: {run['arming']}", file=sys.stderr)
    if not run["arming"]["armed"]:
        run["stopped"] = "arming failed; no target was run"
        (out_dir / "run.json").write_text(json.dumps(run, indent=2))
        return 1
    tally: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool, (out_dir / "summary.jsonl").open("a") as summ:
        futs = {pool.submit(run_target, t, args.work, out_dir): t for t in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            r = fut.result()
            v = r.get("verdict", "RUNNER_ERROR")
            tally[v] = tally.get(v, 0) + 1
            summ.write(json.dumps({"name": r["target"]["name"], "repo": r["target"].get("repo"), "verdict": v,
                                   "reason": r.get("reason"), "counts": r.get("counts"),
                                   "live_before_shutdown": (r.get("trials") or [{}])[0].get("live_before_shutdown"),
                                   "wall_clock_s": r.get("wall_clock_s")}) + "\n")
            summ.flush()
            print(f"[{i}/{len(targets)}] {v:18} {r['target']['name']}", file=sys.stderr)
    run["tally"] = tally
    run["wall_clock_s"] = round(time.time() - t0, 1)
    run["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out_dir / "run.json").write_text(json.dumps(run, indent=2))
    print(json.dumps(tally), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
