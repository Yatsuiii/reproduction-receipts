"""Failure injections for agent-receipts, written before the implementation.

One clean session is recorded (`build_clean`), then each injection rewrites the receipt file the way one kind of attacker or
accident would. EXPECTED.json says what each verifier must report. Both files are pinned in FROZEN.json.

Two kinds of attacker, because they need different answers:
- outsider: has the file, not the signing key. Edits lines. Against the baselines it also repairs whatever integrity the format
  lets anyone repair (an unsigned hash chain can be recomputed by anyone).
- holder: has the signing key, so can re-sign anything. A signature cannot stop this; only an anchor published elsewhere can.
  These are the blind spots, and they are expected to PASS unless an anchor is given.

Stdlib only, apart from the package under test.
"""
from __future__ import annotations

import json
from pathlib import Path

SEED_REAL = bytes(range(32))
SEED_ATTACKER = bytes(range(100, 132))
ACTOR = "support-agent@example.test"

NOTES = "Refund policy: 30 days. Contact: billing team."


# Tools of the toy agent. Deterministic so they can be replayed.
def read_file(path):
    return {"path": path, "text": NOTES}


def search(query):
    return {"query": query, "hits": ["kb/refunds.md", "kb/billing.md"]}


def summarize(text, hits):
    return {"summary": text.split(".")[0] + ".", "n_hits": len(hits)}


def send_email(to, body):            # side effect: never replayable
    return {"queued": True, "to": to}


def lookup_order(order_id):
    raise KeyError(f"order {order_id} not found")


TOOLS = {"read_file": read_file, "search": search, "summarize": summarize, "send_email": send_email,
         "lookup_order": lookup_order}


def changed_search(query):           # the same tool after an upstream change
    return {"query": query, "hits": ["kb/refunds-v2.md"]}


class Clock:
    def __init__(self, start=1_763_700_000.0, step=0.25):
        self.t, self.step = start, step

    def __call__(self):
        self.t += self.step
        return self.t


def build_clean(path: Path, *, seed=SEED_REAL, session_meta=None):
    """Record the clean session: 5 calls, one of which fails and stays visible. Returns the anchor."""
    from agent_receipts import Recorder, Signer
    rec = Recorder(path, signer=Signer.from_seed(seed), actor=ACTOR, clock=Clock(), meta=session_meta or {"task": "refund q"})
    f = rec.call("read_file", read_file, {"path": "notes.txt"}, sources=["file:notes.txt"], replayable=True)      # seq 1
    s = rec.call("search", search, {"query": "refund window"}, sources=["web:kb.example.test"], replayable=True)  # seq 2
    rec.call("summarize", summarize, {"text": f["text"], "hits": s["hits"]}, derived_from=[1, 2], replayable=True)  # seq 3
    try:
        rec.call("lookup_order", lookup_order, {"order_id": "A-17"}, replayable=True)                               # seq 4
    except KeyError:
        pass
    rec.call("send_email", send_email, {"to": "customer@example.test", "body": "30 days."}, derived_from=[3])     # seq 5
    return rec.close()                                                                                            # seq 6


# ---- helpers on the file as a list of dicts ----

def load(path: Path) -> list:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump(path: Path, records: list) -> None:
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in records), encoding="utf-8")


def rechain_unsigned(records: list) -> None:
    """What anyone can do to an unsigned hash chain: recompute every prev and close count."""
    from agent_receipts import record_hash
    calls = sum(r.get("type") == "call" for r in records)
    for i, r in enumerate(records):
        r["seq"] = i
        r["session"] = records[0]["session"]
        r["prev"] = None if i == 0 else record_hash(records[i - 1])
        if r.get("type") == "close":
            r["count"] = calls


def resign_all(records: list, seed: bytes) -> None:
    """What a key holder can do: recompute the chain and re-sign every record."""
    from agent_receipts import Signer, record_hash, seal
    signer = Signer.from_seed(seed)
    calls = sum(r.get("type") == "call" for r in records)
    for i, r in enumerate(records):
        r["seq"] = i
        r["prev"] = None if i == 0 else record_hash(records[i - 1])
        if r.get("type") == "close":
            r["count"] = calls
        seal(r, signer)


def _redigest(r: dict) -> None:
    from agent_receipts.canon import sha256_json
    if r.get("args") is not None:
        r["args_sha256"] = sha256_json(r["args"])
    if r.get("result") is not None:
        r["result_sha256"] = sha256_json(r["result"])


# ---- injections. Each takes the clean record list and a mode, returns the mutated list. ----
# mode is "signed" (attack the real format, no repair possible without the key) or "repair" (outsider fixes what the
# format allows anyone to fix; used for the baselines).

def edit_args(rs, mode):
    rs[5]["args"]["to"] = "attacker@example.test"
    _redigest(rs[5])
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def edit_result(rs, mode):
    rs[2]["result"]["hits"] = ["kb/refunds.md"]
    _redigest(rs[2])
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def hide_failure(rs, mode):
    """Turn the failed lookup into a success: failures are the first thing someone will want to remove."""
    r = rs[4]
    r["status"], r["error"], r["result"] = "ok", None, {"order_id": "A-17", "status": "refunded"}
    _redigest(r)
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def delete_middle(rs, mode):
    del rs[4]
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def reorder(rs, mode):
    rs[3], rs[5] = rs[5], rs[3]
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def truncate_tail(rs, mode):
    """Drop the last call and the close, as if the session ended early. Against an unsigned format the outsider can also
    write a fresh close record, so in repair mode this keeps the close and fixes it."""
    if mode == "repair":
        del rs[5]
        rechain_unsigned(rs)
        return rs
    return rs[:-2]


def drop_close_keep_count(rs, mode):
    """Drop the last call but keep the close record."""
    del rs[5]
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def foreign_resign(rs, mode):
    """An outsider edits, then re-signs everything with their own key."""
    rs[5]["args"]["to"] = "attacker@example.test"
    _redigest(rs[5])
    resign_all(rs, SEED_ATTACKER)
    return rs


def splice_other_session(rs, mode, other=None):
    """Insert a correctly signed call from another session by the same key."""
    rs.insert(3, other[2])
    if mode == "repair":
        rechain_unsigned(rs)
    return rs


def inline_digest_lie(rs, mode):
    """The key holder keeps the honest digest but shows a different inline result, then re-signs."""
    rs[1]["result"]["text"] = "Refund policy: 365 days."
    resign_all(rs, SEED_REAL)
    return rs


def malformed_line(rs, mode):
    rs[2] = "{not json"
    return rs


def holder_rewrite(rs, mode):
    """Blind spot. The key holder edits a call and re-signs the whole chain."""
    rs[5]["args"]["to"] = "attacker@example.test"
    _redigest(rs[5])
    resign_all(rs, SEED_REAL)
    return rs


def holder_clock_backwards(rs, mode):
    rs[3]["t"] = rs[1]["t"] - 10
    resign_all(rs, SEED_REAL)
    return rs


def untouched(rs, mode):
    return rs


INJECTIONS = {
    "clean": untouched,
    "edit_args": edit_args,
    "edit_result": edit_result,
    "hide_failure": hide_failure,
    "delete_middle": delete_middle,
    "reorder": reorder,
    "truncate_tail": truncate_tail,
    "drop_close_keep_count": drop_close_keep_count,
    "foreign_resign": foreign_resign,
    "splice_other_session": splice_other_session,
    "inline_digest_lie": inline_digest_lie,
    "malformed_line": malformed_line,
    "holder_rewrite": holder_rewrite,
    "holder_rewrite_with_anchor": holder_rewrite,
    "holder_clock_backwards": holder_clock_backwards,
    "revoked_source": untouched,
    "replay_tool_changed": untouched,
}


def write_mutated(name: str, clean: Path, other: Path, out: Path, mode: str) -> None:
    rs = load(clean)
    fn = INJECTIONS[name]
    if fn is splice_other_session:
        rs = fn(rs, mode, other=load(other))
    else:
        rs = fn(rs, mode)
    out.write_text("".join((r if isinstance(r, str) else json.dumps(r, sort_keys=True)) + "\n" for r in rs),
                   encoding="utf-8")
