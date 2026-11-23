"""Turn a run directory into the results table. Reads only the committed JSON.

    python3 client-teardown/summarize.py client-teardown/runs/20261121-run1
"""

import json
import sys
from pathlib import Path

SC = ("clean", "eof-ignore", "term-ignore", "wrapped")


def cell(c: dict) -> str:
    n = c["n"]
    counts = c["counts"]
    if counts.get("CLEAN", 0) == n:
        return f"clean {n}/{n}"
    if counts.get("RESIDUE", 0) == n:
        return f"**residue {n}/{n}**"
    return " ".join(f"{k.lower()} {v}" for k, v in sorted(counts.items())) + f" of {n}"


def table(files: list[Path]) -> list[str]:
    out = ["| target | " + " | ".join(SC) + " |", "|---|" + "---|" * len(SC)]
    for f in files:
        d = json.loads(f.read_text())
        cells = {c["scenario"]: cell(c) for c in d["cells"]}
        out.append(f"| `{f.stem}` | " + " | ".join(cells.get(s, "not run") for s in SC) + " |")
    return out


def main() -> int:
    run = Path(sys.argv[1])
    lines = ["Reference clients (arming gate: every cell must match its expected value in every trial)", ""]
    arm = sorted((run / "arm").glob("*.json"))
    lines.append("| reference | " + " | ".join(SC) + " |")
    lines.append("|---|" + "---|" * len(SC))
    for f in arm:
        d = json.loads(f.read_text())
        row = []
        for c in d["cells"]:
            row.append(f"{cell(c)} (expected {c['expected'].lower()}{'' if c['armed'] else ', NOT ARMED'})")
        lines.append(f"| `{d['target']}` | " + " | ".join(row) + " |")
    lines += ["", "Targets", ""]
    lines += table(sorted((run / "targets").glob("*.json")))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
