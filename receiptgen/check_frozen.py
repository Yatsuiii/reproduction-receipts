"""Frozen-file guard for the receipt generator failure injections and frozen entry points.

FROZEN.json pins the SHA-256 of every file under triage/fixtures/, including EXPECTED.json. Those files were committed before
triage.py existed, so the expected verdicts could not be fitted to the implementation. This check fails when a pinned file changes,
disappears, or a new file appears under fixtures/ without being registered. A deliberate change goes in FROZEN_CHANGES.md first,
then `python receiptgen/check_frozen.py --update` rewrites the registry; the registry diff and the log entry land in the same commit.

Stdlib only. Exit 0 when clean, 1 on any finding.
usage: python receiptgen/check_frozen.py [--update]"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "FROZEN.json"
ROOTS = ["fixtures"]
# Frozen entry points: pinned after they first passed every fixture. A change needs a FROZEN_CHANGES.md entry and a
# fresh results/fixtures.json in the same commit.
ENTRY_POINTS = ["rerun.py", "run_fixtures.py"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def current() -> dict:
    out = {}
    for root in ROOTS:
        for p in sorted((HERE / root).rglob("*")):
            if p.is_file():
                out[p.relative_to(HERE).as_posix()] = sha256(p)
    for name in ENTRY_POINTS:
        out[name] = sha256(HERE / name)
    return out


def main(argv: list) -> int:
    if "--update" in argv:
        REGISTRY.write_text(json.dumps({"format": "receiptgen-frozen/1", "roots": ROOTS, "entry_points": ENTRY_POINTS, "files": current()}, indent=1) + "\n",
                            encoding="utf-8", newline="\n")
        print(f"wrote {REGISTRY.name}; log the reason in FROZEN_CHANGES.md in the same commit")
        return 0
    pinned = json.loads(REGISTRY.read_text(encoding="utf-8"))["files"]
    now = current()
    problems = [f"changed: {k}" for k in pinned if k in now and now[k] != pinned[k]]
    problems += [f"missing: {k}" for k in pinned if k not in now]
    problems += [f"unregistered: {k}" for k in now if k not in pinned]
    for line in problems:
        print(f"FROZEN: {line}")
    if problems:
        print("Frozen failure injections changed. Log the change in receiptgen/FROZEN_CHANGES.md, then run "
              "python receiptgen/check_frozen.py --update.")
        return 1
    print(f"frozen: {len(pinned)} files match FROZEN.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
