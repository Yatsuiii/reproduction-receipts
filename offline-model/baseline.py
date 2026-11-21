"""Cheap baselines for the personal-identifier task. Stdlib only, no model, no network.

majority: answer NO for every line (32 of 60 lines are NO).
regex:    YES if the line matches an email, a phone-like or account-like digit run, a known ID keyword, a personal
          title, or a street address. Written before any model output existed; it has no rule for bare names.

usage: python -I offline-model/baseline.py [--out FILE]"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

RULES = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "digit_run": re.compile(r"(?:\+?\d[\d \-/]{7,}\d)"),
    "id_keyword": re.compile(r"\b(?:DOB|Born|MRN|SSN|Passport|NHS number|licence|license|IBAN|Employee ID|sort code)\b", re.I),
    "title": re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Officer)\.?\s+[A-Z]"),
    "street": re.compile(r"\b\d+\s+(?:[A-Z][a-z]+\s+){1,3}(?:St|Street|Dr|Drive|Rd|Road|Row|Ave|Avenue|Lane)\b"),
}


def regex_pred(text: str):
    hits = [k for k, r in RULES.items() if r.search(text)]
    return ("YES" if hits else "NO"), hits


def main(argv: list) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    items = [json.loads(l) for l in (HERE / "task/items.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = []
    for it in items:
        pred, hits = regex_pred(it["text"])
        rows.append({"id": it["id"], "label": it["label"], "majority": "NO", "regex": pred, "regex_rules": hits})
    res = {"format": "offline-baseline/1", "items": len(rows)}
    for b in ("majority", "regex"):
        c = sum(r["label"] == r[b] for r in rows)
        res[b] = {"correct": c, "accuracy": round(c / len(rows), 6),
                  "wrong": [r["id"] for r in rows if r["label"] != r[b]]}
    res["rows"] = rows
    text = json.dumps(res, indent=1) + "\n"
    if a.out:
        a.out.write_text(text, encoding="utf-8", newline="\n")
    print(f"majority {res['majority']['correct']}/{len(rows)}, regex {res['regex']['correct']}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
