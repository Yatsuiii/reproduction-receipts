"""Score rerun.py against the frozen failure injections, next to a naive baseline.

Each fixture's pkg/ is copied into a fresh git repository with a fixed author and date, then rerun.py runs its spec.json.
A case passes when status, command outcomes, output classes, flags and the reproduced list all equal EXPECTED.json.

The naive baseline is the receipt most people would write by hand: every declared output of a command that exited 0
"reproduced". It is scored on the reproduced list only, which is the claim that matters.

Also checks the receipt text rules listed in EXPECTED.json.

usage: python receiptgen/run_fixtures.py [--json results/fixtures.json]
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rerun  # noqa: E402

GIT_ENV = {"GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid", "GIT_COMMITTER_NAME": "fixture",
           "GIT_COMMITTER_EMAIL": "fixture@example.invalid", "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z",
           "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"}


def make_repo(pkg: Path, dest: Path) -> str:
    shutil.copytree(pkg, dest)
    env = {**os.environ, **GIT_ENV}
    for args in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
        subprocess.run(["git", *args], cwd=dest, env=env, check=True, capture_output=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=dest, capture_output=True, text=True).stdout.strip()


def text_rule_problems(res: dict, receipt: str) -> list:
    problems = []
    if rerun.BANNED.search(receipt):
        problems.append("banned wording")
    rows = [l for l in receipt.splitlines() if l.startswith("| ") and "`" in l and l.rstrip().endswith(("yes |", "no |"))]
    for o, e in res["outputs"].items():
        row = next((r for r in rows if f"`{o}`" in r), None)
        if row is None:
            problems.append(f"no result row for {o}")
        elif row.rstrip().endswith("yes |") != (o in res["reproduced"]):
            problems.append(f"reproduced column wrong for {o}")
    failed_section = receipt.split("## Failed, stopped or killed runs", 1)[1].split("##", 1)[0]
    for c in res["commands"]:
        if c["outcome"] != "exit0" and (c["cmd"] not in failed_section or c["log"] not in failed_section):
            problems.append(f"failed command {c['id']} not listed with its log")
    if res["status"] == "ran":
        for needle in [res["commit"], "| OS |", "| CPU |", "| Cores |", "| RAM |", "Wall clock and cost", "USD"]:
            if needle not in receipt:
                problems.append(f"receipt lacks {needle!r}")
        for c in res["commands"]:
            if c["cmd"] not in receipt:
                problems.append(f"command not named exactly: {c['cmd']}")
    elif "No package code ran" not in receipt:
        problems.append("aborted receipt does not say no package code ran")
    return problems


def main(argv: list) -> int:
    expected = json.loads((HERE / "fixtures" / "EXPECTED.json").read_text())
    rows, passed, naive_ok, text_ok = [], 0, 0, 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for case in expected["cases"]:
            name = case["fixture"]
            fx = HERE / "fixtures" / name
            head = make_repo(fx / "pkg", tmp / name / "repo")
            spec = json.loads((fx / "spec.json").read_text().replace("{{REPO}}", str(tmp / name / "repo")).replace("{{HEAD}}", head))
            res = rerun.rerun(spec, tmp / name / "out")
            got = {"status": res["status"], "commands": {c["id"]: c["outcome"] for c in res["commands"]},
                   "outputs": {o: e["class"] for o, e in res["outputs"].items()}, "flags": sorted(res["flags"]),
                   "reproduced": sorted(res["reproduced"])}
            want = {k: (sorted(case[k]) if isinstance(case[k], list) else case[k])
                    for k in ("status", "commands", "outputs", "flags", "reproduced")}
            ok = got == want
            if "differing_numbers" in case:
                n = sum(e.get("numbers_differ", 0) for e in res["outputs"].values())
                ok = ok and n == case["differing_numbers"]
            naive = sorted(o for c in res["commands"] if c["outcome"] == "exit0"
                           for o in next(s["outputs"] for s in spec["commands"] if s["id"] == c["id"]))
            n_ok = naive == want["reproduced"]
            receipt = (tmp / name / "out" / "RECEIPT.md").read_text()
            problems = text_rule_problems(res, receipt)
            passed += ok
            naive_ok += n_ok
            text_ok += not problems
            rows.append({"fixture": name, "pass": ok, "naive_baseline_pass": n_ok, "text_rule_problems": problems,
                         "got": got, "want": want})
            print(f"{'PASS' if ok else 'FAIL'} {'text-ok' if not problems else 'TEXT ' + '; '.join(problems)} "
                  f"naive={'ok' if n_ok else 'wrong'} {name}" + ("" if ok else f"\n  got  {got}\n  want {want}"))
    n = len(expected["cases"])
    print(f"\nrerun.py {passed}/{n}; receipt text rules {text_ok}/{n}; naive 'exit 0 means reproduced' baseline {naive_ok}/{n}")
    if "--json" in argv:
        out = Path(argv[argv.index("--json") + 1])
        out.parent.mkdir(parents=True, exist_ok=True)
        rerun_sha = rerun.sha256_bytes((HERE / "rerun.py").read_bytes())
        out.write_text(json.dumps({"rerun_py_sha256": rerun_sha, "passed": passed, "text_rules_passed": text_ok,
                                   "naive_baseline_passed": naive_ok, "cases": n, "rows": rows}, indent=1) + "\n")
    return 0 if passed == n and text_ok == n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
