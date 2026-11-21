"""Run the frozen anchor tamper cases against the anchored verifier and the v0 verifier without an anchor (the baseline).
Writes results/anchor_injections.json and .md. Exit 1 on any departure from anchor_injections/EXPECTED.json."""
import json
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "anchor_injections"))

import cases  # noqa: E402
from agent_receipts import verify  # noqa: E402

EXPECTED = json.loads((HERE / "anchor_injections" / "EXPECTED.json").read_text(encoding="utf-8"))
REVIEWED = set()   # (case, verifier) departures reviewed in results/departures.md


def main() -> int:
    t0 = time.perf_counter()
    rows, unreviewed = [], []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        w = cases.build(td)
        trusted = {cases.ACTOR: w["signer"].public_hex}
        for name, case in EXPECTED["cases"].items():
            recs, bundle, kw = cases.CASES[name](w)
            p = td / f"{name}.jsonl"
            p.write_text("".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8")
            a = verify(p, trusted=trusted, anchor_bundle=bundle, log_keys=[w["log"].pub_pem], **kw)
            b = verify(p, trusted=trusted)
            got = {"sdk_anchored": {"passes": a.ok, "codes": sorted(a.codes()), "findings": [str(f) for f in a.findings]},
                   "v0_no_anchor": {"passes": b.ok, "codes": sorted(b.codes())}}
            dep = {}
            e = case["sdk_anchored"]
            bad = []
            if a.ok != e["passes"]:
                bad.append(f"passes={a.ok}")
            if set(e["detect"]) - a.codes():
                bad.append(f"missing {sorted(set(e['detect']) - a.codes())}")
            if e.get("exact") and a.codes() != set(e["detect"]):
                bad.append(f"codes {sorted(a.codes())}")
            if bad:
                dep["sdk_anchored"] = bad
            if b.ok != case["v0_no_anchor"]["passes"]:
                dep["v0_no_anchor"] = [f"passes={b.ok}"]
            for v in dep:
                if (name, v) not in REVIEWED:
                    unreviewed.append((name, v))
            rows.append({"case": name, "holder": case["holder"], "attack": case["attack"], "got": got, "departures": dep})
    attacks = [r for r in rows if r["attack"]]
    holder = [r for r in attacks if r["holder"]]
    score = {v: sum(not r["got"][v]["passes"] for r in attacks) for v in ("sdk_anchored", "v0_no_anchor")}
    hscore = {v: sum(not r["got"][v]["passes"] for r in holder) for v in ("sdk_anchored", "v0_no_anchor")}
    out = {"format": "agent-receipts-anchor-results/1", "python": sys.version.split()[0],
           "log": "local Rekor v1 stand-in (anchor_injections/fakelog.py); live-log formats are checked in tests/test_rekor_live.py",
           "wall_seconds": round(time.perf_counter() - t0, 3), "attacks": len(attacks), "detected": score,
           "holder_attacks": len(holder), "holder_detected": hscore, "unreviewed_departures": len(unreviewed),
           "cases": rows}
    (HERE / "results" / "anchor_injections.json").write_text(json.dumps(out, indent=1) + "\n", newline="\n")
    md = ["# Anchor tamper cases: results", "",
          f"Expected verdicts frozen before the anchoring code. Unreviewed departures: **{len(unreviewed)}**.", "",
          f"Attacks caught: anchored **{score['sdk_anchored']}/{len(attacks)}**, v0 without an anchor "
          f"{score['v0_no_anchor']}/{len(attacks)}. Attacks needing the signing key: anchored "
          f"**{hscore['sdk_anchored']}/{len(holder)}**, v0 {hscore['v0_no_anchor']}/{len(holder)}.", "",
          "Run against a local stand-in for Rekor, because the public log is unreachable from the machine that built this.", "",
          "| case | needs key | anchored | v0, no anchor |", "| --- | --- | --- | --- |"]
    for r in rows:
        c = lambda v: ("pass" if r["got"][v]["passes"] else "**FAIL**") + " " + ", ".join(
            x for x in r["got"][v]["codes"] if x != "ok")
        md.append(f"| {r['case']} | {'yes' if r['holder'] else 'no'} | {c('sdk_anchored')} | {c('v0_no_anchor')} |")
    md += ["", "`holder_rewrite_shift_and_reanchor` passing is the expected blind spot: a key holder who rewrites, moves every "
               "timestamp and anchors the rewrite. Only an online search of the log for the key's other entries finds it."]
    if unreviewed or any(r["departures"] for r in rows):
        md += ["", "## Departures", ""] + [f"- {r['case']} / {v}: {'; '.join(d)}" for r in rows for v, d in r["departures"].items()]
    (HERE / "results" / "anchor_injections.md").write_text("\n".join(md) + "\n", newline="\n")
    print("\n".join(md))
    return 1 if unreviewed else 0


if __name__ == "__main__":
    sys.exit(main())
