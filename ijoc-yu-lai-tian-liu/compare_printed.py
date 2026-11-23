"""Compare the per-cell lines intruder_monitor.py prints with the committed CSV, at the precision it prints.

Usage: python compare_printed.py COMMITTED.csv RUN.log

Each printed line "N=..  mean=..  bias=..  stdev=..  mse=.." under a SETTING and VALUE header is matched to the
committed row (setting, estimator, N). The committed float is rounded to the printed number of decimals and compared
as text. Used only for a run that was stopped before it wrote its CSV.
"""
import csv
import re
import sys

SET = re.compile(r"^# SETTING (\w+)\s")
EST = re.compile(r"^\s+VALUE\s+(\w+) \(")
LINE = re.compile(r"N=\s*(\d+)\s+mean=(\S+)\s+bias=(\S+)\s+stdev=(\S+)\s+mse=(\S+)")


def main():
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        rows = {(r["setting"], r["estimator"], r["N"]): r for r in csv.DictReader(f)}
    setting = est = None
    match = differ = 0
    for line in open(sys.argv[2], encoding="utf-8"):
        if m := SET.match(line):
            setting = m.group(1).lower()
        elif m := EST.match(line):
            est = m.group(1)
        elif m := LINE.search(line):
            n, *vals = m.groups()
            r = rows[(setting, est, n)]
            for name, printed in zip(["mean_V", "bias", "stdev", "mse"], vals):
                d = len(printed.split(".")[1])
                want = f"{float(r[name]):+.{d}f}" if printed[0] in "+-" and name == "bias" else f"{float(r[name]):.{d}f}"
                if want == printed:
                    match += 1
                else:
                    differ += 1
                    print(f"DIFFER {setting} {est} N={n} {name}: committed {r[name]} printed {printed}")
            print(f"{setting} {est} N={n}: compared")
    print(f"{match + differ} printed values compared: {match} match the committed CSV at printed precision, {differ} differ")
    return 1 if differ else 0


if __name__ == "__main__":
    sys.exit(main())
