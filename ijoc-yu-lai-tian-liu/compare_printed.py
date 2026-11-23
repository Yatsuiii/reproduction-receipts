"""Compare the per-cell lines a value-estimation script prints with the committed CSV, at the precision it prints.

Usage: python compare_printed.py COMMITTED.csv RUN.log

Handles the three long scripts' print formats:
  intruder_monitor.py   "# SETTING A ...", "  VALUE  lsa (...)", "    N=  8  mean=..  bias=..  stdev=..  mse=.."
  inventory_control.py  "Setting 1 [main]: ...", "  VALUE  LSA (...)", same N line
  ttt4x4_value_estimation.py  "N= 20 | est=lsa      | mean=.. | bias=.. | stdev=.. | mse=.."
Each printed value is compared, as text, with the committed float rounded to the same number of decimals.
Used for runs that have not written their CSV yet. Cells not printed are not compared.
"""
import csv
import re
import sys

SET = [re.compile(r"^# SETTING (\w+)\s"), re.compile(r"^Setting (\w+) \[")]
EST = re.compile(r"^\s+VALUE\s+(\w+) \(")
LINE = re.compile(r"N=\s*(\d+)\s+(?:\|\s*est=(\w+)\s*\|\s*)?mean=(\S+?)\s+\|?\s*bias=(\S+?)\s+\|?\s*stdev=(\S+?)\s+\|?\s*mse=([-+0-9.eE]+)")


def fmt(x, printed):
    d = len(printed.split(".")[1])
    s = f"{float(x):.{d}f}"
    if printed[0] == "+" and not s.startswith("-"):
        s = "+" + s
    return s


def main():
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    has_setting = "setting" in rows[0]
    table = {((r["setting"] if has_setting else ""), r["estimator"], r["N"]): r for r in rows}
    setting, est = "", None
    match = differ = cells = 0
    for line in open(sys.argv[2], encoding="utf-8", errors="replace"):
        for p in SET:
            if m := p.match(line):
                setting = m.group(1).lower() if m.group(1).isalpha() else m.group(1)
        if m := EST.match(line):
            est = m.group(1)
        elif m := LINE.search(line):
            n, e, *vals = m.groups()
            key = (setting if has_setting else "", e or est, n)
            r = table[key]
            cells += 1
            for name, printed in zip(["mean_V", "bias", "stdev", "mse"], vals):
                if fmt(r[name], printed) == printed:
                    match += 1
                else:
                    differ += 1
                    print(f"DIFFER {key} {name}: committed {r[name]} printed {printed}")
    print(f"{cells} of {len(rows)} CSV rows printed so far; {match + differ} values compared: "
          f"{match} match the committed CSV at printed precision, {differ} differ")
    return 1 if differ else 0


if __name__ == "__main__":
    sys.exit(main())
