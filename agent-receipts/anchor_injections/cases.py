"""Anchor tamper cases, written before the anchoring code. Frozen.

build() records one session, anchors it in a FakeRekor at close time, and returns everything a case needs. Each case returns
(receipt_records, bundle_or_None, verifier_kwargs). The expected verdicts are in EXPECTED.json.
"""
from __future__ import annotations

import base64
import copy
import json
from pathlib import Path

SEED = bytes(range(32))
OTHER_SEED = bytes(range(50, 82))
ACTOR = "support-agent@example.test"


def build(td: Path):
    from agent_receipts import Recorder, Signer, rekor
    from fakelog import FakeRekor
    t = [1_763_700_000.0]

    def clock():
        t[0] += 1.0
        return t[0]

    def record(path, seed, body="Refund approved."):
        rec = Recorder(path, signer=Signer.from_seed(seed), actor=ACTOR, clock=clock)
        rec.call("lookup_order", lambda order_id: {"id": order_id, "ok": True}, {"order_id": "A-100"})
        rec.call("send_reply", lambda to, body: {"queued": True}, {"to": "c@example.test", "body": body})
        rec.close()
        return [json.loads(x) for x in path.read_text().splitlines()]

    log = FakeRekor()
    other_log = FakeRekor()
    signer = Signer.from_seed(SEED)
    original = record(td / "original.jsonl", SEED)
    close = original[-1]
    bundle = log.bundle(log.add(rekor.proposed_entry(close, signer), int(close["t"]) + 2))
    other = record(td / "other.jsonl", SEED, body="Another session.")
    other_bundle = log.bundle(log.add(rekor.proposed_entry(other[-1], signer), int(other[-1]["t"]) + 2))
    return {"log": log, "other_log": other_log, "signer": signer, "original": original, "bundle": bundle,
            "other": other, "other_bundle": other_bundle}


def _resign(rs, seed, shift=0.0):
    from agent_receipts import Signer, record_hash, seal
    s = Signer.from_seed(seed)
    for i, r in enumerate(rs):
        if shift:
            r["t"] += shift
            if "t_start" in r:
                r["t_start"] += shift
        r["prev"] = None if i == 0 else record_hash(rs[i - 1])
        seal(r, s)
    return rs


def _rewrite(rs):
    rs[2]["args"]["body"] = "Refund denied."
    from agent_receipts.canon import sha256_json
    rs[2]["args_sha256"] = sha256_json(rs[2]["args"])
    return rs


def clean(w):
    return w["original"], w["bundle"], {}


def holder_rewrite(w):
    return _resign(_rewrite(copy.deepcopy(w["original"])), SEED), w["bundle"], {}


def holder_rewrite_edits_bundle(w):
    """Rewrite, then patch the logged hash inside the bundle to match the rewrite."""
    from agent_receipts import Signer, rekor
    rs = _resign(_rewrite(copy.deepcopy(w["original"])), SEED)
    b = copy.deepcopy(w["bundle"])
    b["entry"]["body"] = base64.b64encode(
        json.dumps(rekor.proposed_entry(rs[-1], Signer.from_seed(SEED)), sort_keys=True,
                   separators=(",", ":")).encode()).decode()
    return rs, b, {}


def holder_rewrite_reanchor_later(w):
    """Rewrite two days later and anchor the rewrite as a new entry, leaving the timestamps alone."""
    from agent_receipts import rekor
    rs = _resign(_rewrite(copy.deepcopy(w["original"])), SEED)
    b = w["log"].bundle(w["log"].add(rekor.proposed_entry(rs[-1], w["signer"]), int(rs[-1]["t"]) + 2 * 86400))
    return rs, b, {}


def holder_rewrite_shift_and_reanchor(w):
    """Blind spot: rewrite, move every timestamp two days on, anchor the rewrite. Passes offline."""
    from agent_receipts import rekor
    rs = _resign(_rewrite(copy.deepcopy(w["original"])), SEED, shift=2 * 86400)
    b = w["log"].bundle(w["log"].add(rekor.proposed_entry(rs[-1], w["signer"]), int(rs[-1]["t"]) + 2))
    return rs, b, {}


def forged_log(w):
    """An entire entry from a log the verifier has not pinned."""
    from agent_receipts import rekor
    rs = w["original"]
    b = w["other_log"].bundle(w["other_log"].add(rekor.proposed_entry(rs[-1], w["signer"]), int(rs[-1]["t"]) + 2))
    return rs, b, {}


def inclusion_hash_flipped(w):
    b = copy.deepcopy(w["bundle"])
    h = b["entry"]["verification"]["inclusionProof"]["hashes"]
    h[0] = ("0" if h[0][0] != "0" else "1") + h[0][1:]
    return w["original"], b, {}


def checkpoint_sig_flipped(w):
    b = copy.deepcopy(w["bundle"])
    cp = b["entry"]["verification"]["inclusionProof"]["checkpoint"]
    head, sig_line = cp.rstrip("\n").rsplit("\n", 1)
    dash, name, sig = sig_line.split(" ")
    raw = bytearray(base64.b64decode(sig))
    raw[-1] ^= 1
    b["entry"]["verification"]["inclusionProof"]["checkpoint"] = f"{head}\n{dash} {name} {base64.b64encode(bytes(raw)).decode()}\n"
    return w["original"], b, {}


def set_flipped(w):
    b = copy.deepcopy(w["bundle"])
    b["entry"]["integratedTime"] += 1
    return w["original"], b, {}


def anchor_of_other_session(w):
    return w["original"], w["other_bundle"], {}


def anchor_by_other_key(w):
    """An attacker logs the honest close record's hash with their own key and attaches that entry."""
    from agent_receipts import Signer, rekor
    rs = w["original"]
    b = w["log"].bundle(w["log"].add(rekor.proposed_entry(rs[-1], Signer.from_seed(OTHER_SEED)), int(rs[-1]["t"]) + 2))
    return rs, b, {}


def missing_but_required(w):
    return w["original"], None, {"require_anchor": True}


CASES = {f.__name__: f for f in (clean, holder_rewrite, holder_rewrite_edits_bundle, holder_rewrite_reanchor_later,
                                 holder_rewrite_shift_and_reanchor, forged_log, inclusion_hash_flipped,
                                 checkpoint_sig_flipped, set_flipped, anchor_of_other_session, anchor_by_other_key,
                                 missing_but_required)}
