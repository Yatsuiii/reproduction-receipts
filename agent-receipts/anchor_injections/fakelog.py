"""A local stand-in for Rekor v1, used by the anchor injections because this work's container cannot reach the public log.

It produces entries in the format ANCHOR.md describes (and the verifier must accept): a canonical hashedrekord body, an RFC
6962 Merkle tree, a signed-note checkpoint and a signed entry timestamp, all signed with a P-256 key of its own. Whether those
formats match the real Rekor is checked separately, against live entries, in CI (tests/test_rekor_live.py).
"""
from __future__ import annotations

import base64
import hashlib
import json


def _h(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def leaf_hash(body: bytes) -> bytes:
    return _h(b"\x00" + body)


def node_hash(left: bytes, right: bytes) -> bytes:
    return _h(b"\x01" + left + right)


def mth(leaves: list) -> bytes:
    """RFC 6962 Merkle tree hash over leaf hashes."""
    n = len(leaves)
    if n == 1:
        return leaves[0]
    k = 1
    while k * 2 < n:
        k *= 2
    return node_hash(mth(leaves[:k]), mth(leaves[k:]))


def path(m: int, leaves: list) -> list:
    """RFC 6962 audit path for leaf m."""
    n = len(leaves)
    if n == 1:
        return []
    k = 1
    while k * 2 < n:
        k *= 2
    if m < k:
        return path(m, leaves[:k]) + [mth(leaves[k:])]
    return path(m - k, leaves[k:]) + [mth(leaves[:k])]


def jcs(obj) -> bytes:
    """RFC 8785 for the plain objects used here (strings and integers only)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class FakeRekor:
    def __init__(self, origin="rekor.sigstore.dev - 0", clock=None, tree_offset=0):
        from agent_receipts import p256
        self.priv, self.pub_pem = p256.generate()
        self.der = p256.der_from_pem(self.pub_pem)
        self.log_id = hashlib.sha256(self.der).hexdigest()
        self.origin, self.clock, self.tree_offset = origin, clock, tree_offset
        self.leaves, self.bodies = [], []
        for i in range(3):  # some unrelated entries first, so proofs are not trivial
            self._append(jcs({"apiVersion": "0.0.1", "kind": "hashedrekord", "filler": i}))

    def _append(self, body: bytes) -> int:
        self.bodies.append(body)
        self.leaves.append(leaf_hash(body))
        return len(self.leaves) - 1

    def sign_note(self, text: str) -> str:
        from agent_receipts import p256
        sig = p256.sign(self.priv, text.encode("utf-8"))
        hint = hashlib.sha256(self.der).digest()[:4]
        name = self.origin.split(" ")[0]
        return text + "\n" + f"— {name} {base64.b64encode(hint + sig).decode()}\n"

    def add(self, proposed: dict, integrated_time: int) -> dict:
        """Accept a proposed entry, return the log's response (one {uuid: entry})."""
        from agent_receipts import p256
        body = jcs(proposed)
        idx = self._append(body)
        for i in range(2):   # entries after ours, as in a live log
            self._append(jcs({"apiVersion": "0.0.1", "kind": "hashedrekord", "after": idx, "n": i}))
        size = len(self.leaves)
        root = mth(self.leaves)
        b64body = base64.b64encode(body).decode()
        global_index = idx + self.tree_offset
        set_payload = {"body": b64body, "integratedTime": integrated_time, "logID": self.log_id,
                       "logIndex": global_index}
        set_sig = p256.sign(self.priv, jcs(set_payload))
        checkpoint = self.sign_note(f"{self.origin}\n{size}\n{base64.b64encode(root).decode()}\n")
        entry = {
            "body": b64body, "integratedTime": integrated_time, "logID": self.log_id, "logIndex": global_index,
            "verification": {
                "signedEntryTimestamp": base64.b64encode(set_sig).decode(),
                "inclusionProof": {"checkpoint": checkpoint, "hashes": [h.hex() for h in path(idx, self.leaves)],
                                   "logIndex": idx, "rootHash": root.hex(), "treeSize": size},
            },
        }
        return {hashlib.sha256(leaf_hash(body)).hexdigest(): entry}

    def bundle(self, response: dict) -> dict:
        (uuid, entry), = response.items()
        return {"format": "agent-receipts-anchor/rekor-v1", "log_url": "fake://local", "uuid": uuid, "entry": entry}
