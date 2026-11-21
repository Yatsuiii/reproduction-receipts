"""Frozen-file guard for agent-receipts.

FROZEN.json pins by SHA-256 the format spec and the failure injections (the scenario, the mutations and the expected verdicts).
They were committed before agent_receipts/ existed, so the expected verdicts could not be fitted to the implementation. This
check fails when a pinned file changes or disappears, or a new file appears under injections/ without being registered. A
deliberate change is logged in FROZEN_CHANGES.md first, then `python agent-receipts/check_frozen.py --update` rewrites the
registry, in the same commit.

Stdlib only. Exit 0 when clean, 1 on any finding.
usage: python agent-receipts/check_frozen.py [--update]"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "FROZEN.json"
FILES = ["FORMAT.md"]
ROOTS = ["injections"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def current() -> dict:
    paths = [HERE / f for f in FILES]
    for root in ROOTS:
        paths += [p for p in (HERE / root).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    return {p.relative_to(HERE).as_posix(): sha256(p) for p in sorted(paths) if p.exists()}


def main(argv: list) -> int:
    if "--update" in argv:
        REGISTRY.write_text(json.dumps({"format": "agent-receipts-frozen/1", "files": current()}, indent=1) + "\n",
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
        print("Frozen agent-receipts files changed. Log the change in agent-receipts/FROZEN_CHANGES.md, then run "
              "python agent-receipts/check_frozen.py --update.")
        return 1
    print(f"frozen: {len(pinned)} agent-receipts files match FROZEN.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
