"""Cheap baseline 2: an unsigned hash chain. The same checks as the SDK except signatures and key trust, so anyone who can
edit the file can also recompute the chain."""
from agent_receipts import verify as _verify


def verify(path, revoked=(), anchor=None):
    rep = _verify(path, check_signatures=False, revoked=revoked, anchor=anchor)
    return {"passes": rep.ok, "codes": sorted(rep.codes()), "stale": rep.stale}
