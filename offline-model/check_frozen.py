"""Frozen-file guard for the offline-model receipt.

FROZEN.json pins the SHA-256 of the task, the failure injections, and (once frozen) the entry points and the model pin.
The task and injections were committed before any harness code existed. This check fails when a pinned file changes or
disappears, or when a new file appears under a pinned directory. A deliberate change is logged in FROZEN_CHANGES.md
first, then `python offline-model/check_frozen.py --update` rewrites the registry in the same commit.

Stdlib only. Exit 0 when clean, 1 on any finding.
usage: python offline-model/check_frozen.py [--update]"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "FROZEN.json"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def roots() -> list:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["roots"]


def current(rs: list) -> dict:
    out = {}
    for root in rs:
        base = HERE / root
        paths = [base] if base.is_file() else sorted(base.rglob("*"))
        for p in paths:
            if p.is_file() and "__pycache__" not in p.parts:
                out[p.relative_to(HERE).as_posix()] = sha256(p)
    return out


def main(argv: list) -> int:
    rs = roots()
    if "--update" in argv:
        REGISTRY.write_text(json.dumps({"format": "offline-frozen/1", "roots": rs, "files": current(rs)}, indent=1) + "\n",
                            encoding="utf-8", newline="\n")
        print(f"wrote {REGISTRY.name}; log the reason in FROZEN_CHANGES.md in the same commit")
        return 0
    pinned = json.loads(REGISTRY.read_text(encoding="utf-8"))["files"]
    now = current(rs)
    problems = [f"changed: {k}" for k in pinned if k in now and now[k] != pinned[k]]
    problems += [f"missing: {k}" for k in pinned if k not in now]
    problems += [f"unregistered: {k}" for k in now if k not in pinned]
    for line in problems:
        print(f"FROZEN: {line}")
    if problems:
        print("Frozen offline-model files changed. Log the change in offline-model/FROZEN_CHANGES.md, then run "
              "python offline-model/check_frozen.py --update.")
        return 1
    print(f"frozen: {len(pinned)} files match FROZEN.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
