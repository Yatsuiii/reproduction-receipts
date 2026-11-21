"""Shared by the three framework examples: the tools, the scripted plan, and the scoring against the frozen
adapter_injections/EXPECTED.json. No model is called anywhere; each framework's own runtime executes the plan."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PKG))

from adapter_injections import tamper  # noqa: E402
from agent_receipts import verify  # noqa: E402

EXPECTED = json.loads((PKG / "adapter_injections" / "EXPECTED.json").read_text(encoding="utf-8"))
PLAN = EXPECTED["plan"]
ACTOR = "support-agent@example.test"
POLICY = {
    "read_note": {"sources": ["file:policy.txt"], "replayable": True},
    "search_kb": {"sources": ["kb:support-kb"], "replayable": True},
    "lookup_order": {"sources": ["db:orders"], "replayable": True},
    "send_reply": {},
}


def read_note(name: str) -> dict:
    """Read an internal note."""
    return {"name": name, "text": "Refunds within 30 days of delivery."}


def search_kb(query: str) -> dict:
    """Search the support knowledge base."""
    return {"query": query, "hits": ["kb/refunds.md#30-days"]}


def lookup_order(order_id: str) -> dict:
    """Look up an order by id."""
    if order_id != "A-100":
        raise ValueError(f"no order {order_id}")
    return {"order_id": order_id, "total": 49.0}


def send_reply(to: str, body: str) -> dict:
    """Send a reply to the customer."""
    return {"queued": True, "to": to}


FUNCS = {f.__name__: f for f in (read_note, search_kb, lookup_order, send_reply)}


def _lines(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines()]


def score(framework: str, receipt: Path, native: list, public_hex: str, anchor: str, framework_finished: bool,
          versions: dict) -> dict:
    """native: the framework's own record of the run, as [{tool, args, output, is_error}]."""
    trusted = {ACTOR: public_hex}
    recs = _lines(receipt)
    calls = [r for r in recs if r["type"] == "call"]
    rep = verify(receipt, trusted=trusted, anchor=anchor)
    fid = {
        "receipt_statuses": [c["status"] for c in calls],
        "receipt_args_equal_plan": [c["args"] for c in calls] == [p["args"] for p in PLAN],
        "receipt_calls_equal_native_calls": [c["tool"] for c in calls] == [n["tool"] for n in native],
        "framework_continues_after_tool_error": framework_finished and len(native) == len(PLAN),
    }
    departures = [f"{k}: got {fid[k]!r}, expected {v!r}" for k, v in EXPECTED["fidelity"].items() if fid[k] != v]
    if not rep.ok:
        departures.append(f"clean receipt did not verify: {sorted(rep.codes())}")

    tamper_rows = {}
    with tempfile.TemporaryDirectory() as td:
        for case, fn in tamper.CASES.items():
            exp = EXPECTED["tamper"][case]
            t = Path(td) / f"{case}.jsonl"
            t.write_text("".join(json.dumps(r) + "\n" for r in fn(copy.deepcopy(recs))), encoding="utf-8")
            got = verify(t, trusted=trusted, anchor=None)
            fn(copy.deepcopy(native), native=True)          # the baseline: nothing to check but that it parses
            row = {"receipt": {"passes": got.ok, "codes": sorted(got.codes())}, "native": {"passes": True}}
            missing = set(exp["receipt"]["detect"]) - set(got.codes())
            if got.ok != exp["receipt"]["passes"] or missing:
                departures.append(f"tamper {case}: receipt passes={got.ok} codes={sorted(got.codes())}")
            tamper_rows[case] = row

    native_marks = any(n["is_error"] for n in native if n["tool"] == "lookup_order")
    return {
        "format": "agent-receipts-framework-example/1",
        "framework": framework,
        "versions": versions,
        "python": sys.version.split()[0],
        "model_calls": 0,
        "cost_usd": 0,
        "fidelity": fid,
        "native_marks_the_failure_as_an_error": native_marks,
        "native_marks_guess": EXPECTED["native_marks_the_failure_as_an_error_guess"][framework],
        "tamper_detected": {"receipt": sum(not r["receipt"]["passes"] for r in tamper_rows.values()),
                            "native": 0, "of": len(tamper_rows)},
        "tamper": tamper_rows,
        "native": native,
        "departures_from_expected": departures,
    }


# Departures from the frozen EXPECTED.json that were reviewed and explained in results/departures.md. Listed, not fixed.
REVIEWED = {
    ("crewai", "receipt_statuses"), ("crewai", "receipt_args_equal_plan"), ("crewai", "receipt_calls_equal_native_calls"),
}


def write(framework: str, out_dir: Path, summary: dict, write_results: bool) -> int:
    unreviewed = [d for d in summary["departures_from_expected"] if (framework, d.split(":")[0]) not in REVIEWED]
    summary["unreviewed_departures"] = unreviewed
    (out_dir / "native.json").write_text(json.dumps(summary["native"], indent=1) + "\n")
    if write_results:
        (PKG / "results" / f"{framework}_example.json").write_text(json.dumps(summary, indent=1) + "\n", newline="\n")
    print(json.dumps({k: summary[k] for k in ("framework", "fidelity", "native_marks_the_failure_as_an_error",
                                              "tamper_detected", "departures_from_expected",
                                              "unreviewed_departures")}, indent=1))
    return 1 if unreviewed else 0
