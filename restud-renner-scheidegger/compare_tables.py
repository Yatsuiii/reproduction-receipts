"""Compare the numbers in two folders of generated .tex tables, cell by cell.

Usage: python compare_tables.py REFERENCE_DIR CANDIDATE_DIR

Every table in REFERENCE_DIR is compared with the file of the same name in CANDIDATE_DIR. Numbers are pulled out
in order, so "1.6\\cdot 10^{-6}" and "1.6e-06" both read as 1.6e-06, and are compared as printed, at the precision
the reference prints. Exit code 1 if any cell differs or a table is missing.
"""
import re
import sys
from pathlib import Path

NUM = re.compile(r"(-?\d+\.\d+)(?:\s*\\cdot\s*10\^\{(-?\d+)\}|e([+-]?\d+))?")


def numbers(text: str) -> list[str]:
    out = []
    for m in NUM.finditer(text):
        mant, exp1, exp2 = m.groups()
        exp = exp1 if exp1 is not None else exp2
        out.append(f"{mant}e{int(exp):+03d}" if exp is not None else mant)
    return out


def main() -> int:
    ref, cand = Path(sys.argv[1]), Path(sys.argv[2])
    names = sorted(p.name for p in ref.glob("*.tex"))
    bad = 0
    for name in names:
        c = cand / name
        if not c.exists():
            print(f"MISSING  {name}")
            bad += 1
            continue
        a, b = numbers((ref / name).read_text()), numbers(c.read_text())
        if a == b:
            print(f"MATCH    {name}  ({len(a)} numbers)")
        else:
            bad += 1
            print(f"DIFFER   {name}")
            for i in range(max(len(a), len(b))):
                x = a[i] if i < len(a) else "-"
                y = b[i] if i < len(b) else "-"
                if x != y:
                    print(f"         cell {i}: reference {x}  candidate {y}")
    print(f"{len(names) - bad}/{len(names)} tables match")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
