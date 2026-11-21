"""Cheap baselines for the clinical-action task. Stdlib only, no model, no network.

majority: answer NO for every note (33 of 60 are NO).
keywords: YES if the note contains any common action word or request phrase. No handling of tense, negation or who
          is speaking, which is the point: it is the rule a busy team would write first.

usage: python -I offline-model/clinical/baseline_keywords.py [--out FILE]"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

ACTION = re.compile(r"\b(?:start|stop|hold|withhold|reduce|increase|uptitrate|add|refer|arrange|book|order|repeat|"
                    r"recheck|check|monitor|consider|offer|give|remove|escalate|restrict|switch|get|ask|needs?|needed|"
                    r"should|recommend\w*|would benefit|please|plan)\b", re.I)


def main(argv: list) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    items = [json.loads(l) for l in (HERE / "task/items.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = []
    for it in items:
        hits = sorted({m.group(0).lower() for m in ACTION.finditer(it["text"])})
        rows.append({"id": it["id"], "label": it["label"], "majority": "NO", "keywords": "YES" if hits else "NO",
                     "keyword_hits": hits})
    res = {"format": "offline-baseline/1", "task": "clinical", "items": len(rows)}
    for b in ("majority", "keywords"):
        c = sum(r["label"] == r[b] for r in rows)
        res[b] = {"correct": c, "accuracy": round(c / len(rows), 6), "wrong": [r["id"] for r in rows if r["label"] != r[b]]}
    res["rows"] = rows
    if a.out:
        a.out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"majority {res['majority']['correct']}/{len(rows)}, keywords {res['keywords']['correct']}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
