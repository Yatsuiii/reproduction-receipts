"""Compare a regenerated results file with the committed one, number by number.

Usage: python compare_results.py committed_file regenerated_file

Both files are read line by line. Every number on a line (as printed, e.g. -0.308 or 1{,}000)
is put in one class:
  exact    same printed text
  differs  anything else, reported with both values
Lines with no numbers must match as text. A missing or extra line is reported.
Exit code 0 only if every number is exact and every line is present.
Written before any package code ran (see PROTOCOL.md).
"""
import re, sys

NUM = re.compile(r"-?\d+(?:\{,\}\d+)*(?:\.\d+)?(?:[eE][-+]?\d+)?")

def numbers(line):
    return NUM.findall(line)

def main(a, b):
    la = open(a, encoding="utf-8", errors="replace").read().splitlines()
    lb = open(b, encoding="utf-8", errors="replace").read().splitlines()
    exact = differs = text_diff = 0
    report = []
    for i in range(max(len(la), len(lb))):
        if i >= len(la):
            report.append(f"line {i+1}: extra line in regenerated file: {lb[i]!r}"); text_diff += 1; continue
        if i >= len(lb):
            report.append(f"line {i+1}: missing in regenerated file: {la[i]!r}"); text_diff += 1; continue
        na, nb = numbers(la[i]), numbers(lb[i])
        if not na and not nb:
            if la[i].strip() != lb[i].strip():
                report.append(f"line {i+1}: text differs: {la[i]!r} vs {lb[i]!r}"); text_diff += 1
            continue
        if len(na) != len(nb):
            report.append(f"line {i+1}: {len(na)} numbers committed, {len(nb)} regenerated: {la[i]!r} vs {lb[i]!r}")
            differs += max(len(na), len(nb)); continue
        for x, y in zip(na, nb):
            if x == y:
                exact += 1
            else:
                differs += 1
                report.append(f"line {i+1}: committed {x} regenerated {y}")
        if NUM.sub("#", la[i]).strip() != NUM.sub("#", lb[i]).strip():
            report.append(f"line {i+1}: non-numeric text differs: {la[i]!r} vs {lb[i]!r}"); text_diff += 1
    print(f"{a} vs {b}: {exact} numbers exact, {differs} differ, {text_diff} text lines differ")
    for r in report[:200]:
        print("  " + r)
    return 0 if differs == 0 and text_diff == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
