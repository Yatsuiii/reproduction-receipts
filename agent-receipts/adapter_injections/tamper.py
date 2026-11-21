"""Tamper cases for the framework adapters, written before the adapters. Frozen in FROZEN.json.

Each function takes a list of records (the receipt as dicts, or the framework's native tool events as dicts) plus the index
of the calls in plan order, and returns the tampered list. The native list has no signatures, so the only possible check on
it is that it parses: its expected verdict is `passes` for every case (the baseline).
"""
from __future__ import annotations

ATTACKER_SEED = bytes(range(100, 132))


def _receipt_calls(rs):
    return [i for i, r in enumerate(rs) if isinstance(r, dict) and r.get("type") == "call"]


def edit_reply_args(rs, native=False):
    i = 3 if native else _receipt_calls(rs)[3]
    rs[i]["args"]["body"] = "Refund denied."
    if not native:
        from agent_receipts.canon import sha256_json
        rs[i]["args_sha256"] = sha256_json(rs[i]["args"])
    return rs


def hide_failure(rs, native=False):
    i = 2 if native else _receipt_calls(rs)[2]
    if native:
        rs[i]["is_error"], rs[i]["output"] = False, {"order_id": "A-404", "status": "refunded"}
    else:
        from agent_receipts.canon import sha256_json
        res = {"order_id": "A-404", "status": "refunded"}
        rs[i].update(status="ok", error=None, result=res, result_sha256=sha256_json(res))
    return rs


def delete_failed_call(rs, native=False):
    del rs[2 if native else _receipt_calls(rs)[2]]
    return rs


def foreign_resign(rs, native=False):
    edit_reply_args(rs, native)
    if not native:
        from agent_receipts import Signer, record_hash, seal
        s = Signer.from_seed(ATTACKER_SEED)
        for i, r in enumerate(rs):
            r["prev"] = None if i == 0 else record_hash(rs[i - 1])
            seal(r, s)
    return rs


CASES = {"edit_reply_args": edit_reply_args, "hide_failure": hide_failure, "delete_failed_call": delete_failed_call,
         "foreign_resign": foreign_resign}
