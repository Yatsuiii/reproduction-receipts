"""Cheap baseline 1: the JSONL tool-call log most agent stacks already write. The only check available is "every line parses".
Provenance (stale) is computed from the same fields, because that part does not depend on signatures."""
import json
from pathlib import Path

from agent_receipts.verify import stale_calls


def verify(path, revoked=()):
    codes, recs = set(), []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError:
            codes.add("malformed")
    recs = [r for r in recs if isinstance(r, dict)]
    stale = stale_calls(recs, revoked)
    if stale:
        codes.add("stale")
    return {"passes": "malformed" not in codes, "codes": sorted(codes) or ["ok"], "stale": stale}
