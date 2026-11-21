"""Check an offline run without trusting the person who ran it. Stdlib only, no model, no network.

  run DIR       output hashes match run.json; the task in this checkout matches the hashes the run recorded; accuracy and
                the confusion counts recomputed from predictions.csv and this checkout's labels match what run.json states.
  compare A B   predictions must be identical item by item; logits are compared and the largest margin difference is
                reported, with a separate line saying whether logits.csv is byte-identical. Logit drift alone is not a FAIL.
  ledger FILE   every run listed in RUNS.json still has its directory and its run.json status matches the ledger, so a
                failed run cannot be dropped quietly.

Exit 0 on PASS, 1 on FAIL.
usage: python -I offline-model/verify.py run DIR | compare A B | ledger offline-model/RUNS.json"""
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_csv(p: Path) -> list:
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify_run(d: Path) -> list:
    fails = []
    rec = json.loads((d / "run.json").read_text(encoding="utf-8"))
    if rec.get("status") != "ok":
        return [f"run status is {rec.get('status')!r} ({rec.get('reason')}), not ok"]
    for name, pinned in rec["outputs"].items():
        got = sha256_file(d / name)
        if got != pinned:
            fails.append(f"{name} is {got}, run.json records {pinned}")
    for name, pinned in rec["task"].items():
        got = sha256_file(HERE / name)
        if got != pinned:
            fails.append(f"task file {name} in this checkout is {got}, the run used {pinned}")
    labels = {json.loads(l)["id"]: json.loads(l)["label"]
              for l in (HERE / "task/items.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    rows = read_csv(d / "predictions.csv")
    if [r["id"] for r in rows] != list(labels):
        fails.append("predictions.csv item ids do not match task/items.jsonl")
    for r in rows:
        if labels.get(r["id"]) != r["label"]:
            fails.append(f"{r['id']}: predictions.csv label {r['label']} differs from task label {labels.get(r['id'])}")
    correct = sum(labels.get(r["id"]) == r["pred"] for r in rows)
    acc = round(correct / len(rows), 6) if rows else None
    stated = rec["result"]
    if stated["correct"] != correct or stated["accuracy"] != acc:
        fails.append(f"run.json states {stated['correct']} correct (accuracy {stated['accuracy']}), "
                     f"recomputed {correct} (accuracy {acc})")
    conf = {f"label_{l}_pred_{p}": sum(labels.get(r["id"]) == l and r["pred"] == p for r in rows)
            for l in ("YES", "NO") for p in ("YES", "NO")}
    if stated.get("confusion") != conf:
        fails.append(f"run.json confusion {stated.get('confusion')} differs from recomputed {conf}")
    logit_rows = read_csv(d / "logits.csv")
    for p, l in zip(rows, logit_rows):
        if ("YES" if float(l["logit_yes"]) > float(l["logit_no"]) else "NO") != p["pred"]:
            fails.append(f"{p['id']}: prediction {p['pred']} does not follow from its logits")
    print(f"run {d}: {correct}/{len(rows)} correct recomputed from this checkout's labels")
    return fails


def compare(a: Path, b: Path) -> list:
    fails = []
    pa, pb = read_csv(a / "predictions.csv"), read_csv(b / "predictions.csv")
    diff = [x["id"] for x, y in zip(pa, pb) if x != y]
    if len(pa) != len(pb):
        fails.append(f"item counts differ: {len(pa)} vs {len(pb)}")
    if diff:
        fails.append(f"predictions differ on: {diff}")
    la, lb = read_csv(a / "logits.csv"), read_csv(b / "logits.csv")
    worst = max((abs(float(x["margin"]) - float(y["margin"])), x["id"]) for x, y in zip(la, lb))
    prompts_same = all(x["prompt_sha256"] == y["prompt_sha256"] for x, y in zip(la, lb))
    if not prompts_same:
        fails.append("rendered prompts differ between runs")
    print(f"predictions.csv byte-identical: {(a / 'predictions.csv').read_bytes() == (b / 'predictions.csv').read_bytes()}")
    print(f"logits.csv byte-identical: {(a / 'logits.csv').read_bytes() == (b / 'logits.csv').read_bytes()}")
    print(f"largest margin difference: {worst[0]!r} on {worst[1]}")
    return fails


def ledger(path: Path) -> list:
    fails = []
    led = json.loads(path.read_text(encoding="utf-8"))
    for r in led["runs"]:
        d = path.parent / r["dir"]
        if not (d / "run.json").is_file():
            fails.append(f"ledger lists {r['id']} at {r['dir']} but its run.json is gone")
            continue
        status = json.loads((d / "run.json").read_text(encoding="utf-8")).get("status")
        if status != r["status"]:
            fails.append(f"{r['id']}: ledger says {r['status']}, run.json says {status}")
    print(f"ledger: {len(led['runs'])} runs listed")
    return fails


def main(argv: list) -> int:
    if len(argv) == 2 and argv[0] == "run":
        fails = verify_run(Path(argv[1]))
    elif len(argv) == 3 and argv[0] == "compare":
        fails = compare(Path(argv[1]), Path(argv[2]))
    elif len(argv) == 2 and argv[0] == "ledger":
        fails = ledger(Path(argv[1]))
    else:
        print(__doc__)
        return 2
    for f in fails:
        print("FAIL:", f)
    print("FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
