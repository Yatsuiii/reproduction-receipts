"""Compare a regenerated CSV with the committed one, cell by cell.

Usage: python compare_csv.py COMMITTED.csv REGENERATED.csv

Classes per numeric cell: exact (same text), float-equal (<=1e-12 relative), close (<=1e-6 relative), differs.
Prints one summary line and every cell that is not exact. Exit 1 if any cell differs, or rows/columns do not line up.
"""
import csv
import math
import sys


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f))


def num(s):
    try:
        return float(s)
    except ValueError:
        return None


def rel(a, b):
    if a == b:
        return 0.0
    if math.isnan(a) and math.isnan(b):
        return 0.0
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def main():
    a, b = load(sys.argv[1]), load(sys.argv[2])
    counts = {"exact": 0, "float-equal": 0, "close": 0, "differs": 0, "text-differs": 0}
    notes = []
    if a[:1] != b[:1]:
        notes.append(f"HEADER committed={a[:1]} regenerated={b[:1]}")
    if len(a) != len(b):
        notes.append(f"ROWS committed={len(a)} regenerated={len(b)}")
    header = a[0] if a else []
    worst = 0.0
    for i in range(1, min(len(a), len(b))):
        ra, rb = a[i], b[i]
        if len(ra) != len(rb):
            notes.append(f"row {i}: {len(ra)} vs {len(rb)} columns")
        for j in range(min(len(ra), len(rb))):
            x, y = ra[j], rb[j]
            col = header[j] if j < len(header) else str(j)
            if x == y:
                counts["exact"] += 1
                continue
            fx, fy = num(x), num(y)
            if fx is None or fy is None:
                counts["text-differs"] += 1
                notes.append(f"row {i} {col}: committed {x!r} regenerated {y!r}")
                continue
            r = rel(fx, fy)
            worst = max(worst, r)
            k = "float-equal" if r <= 1e-12 else "close" if r <= 1e-6 else "differs"
            counts[k] += 1
            notes.append(f"row {i} {col}: {k} committed {x} regenerated {y} rel {r:.3g}")
    total = sum(counts.values())
    print(f"{sys.argv[2]}: {total} cells; " + ", ".join(f"{k} {v}" for k, v in counts.items()) + f"; worst rel {worst:.3g}")
    for n in notes:
        print("  " + n)
    bad = counts["differs"] + counts["text-differs"] + sum(1 for n in notes if n.startswith(("HEADER", "ROWS", "row ")) and "columns" in n or n.startswith(("HEADER", "ROWS")))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
