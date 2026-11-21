"""Anchor a receipt in Sigstore's Rekor transparency log, and verify the anchor offline. See ANCHOR.md.

    bundle = upload("run.jsonl", signer)                      # needs network to the log; writes run.jsonl.anchor.json
    verify("run.jsonl", trusted=..., anchor_bundle=bundle, log_keys=[REKOR_PEM])   # no network

Only the upload talks to the network (stdlib urllib). Verification uses the pinned log key and pure-Python ECDSA P-256.
"""
from __future__ import annotations

import base64
import hashlib
import json
import urllib.request
from pathlib import Path

from . import ed25519, p256
from .canon import body as record_body

DEFAULT_LOG = "https://rekor.sigstore.dev"
BUNDLE_FORMAT = "agent-receipts-anchor/rekor-v1"
_ED25519_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")


def ed25519_pem(pub: bytes) -> bytes:
    return p256.pem_from_der(_ED25519_SPKI_PREFIX + pub)


def ed25519_from_pem(pem: bytes) -> bytes:
    der = p256.der_from_pem(pem)
    if not der.startswith(_ED25519_SPKI_PREFIX) or len(der) != len(_ED25519_SPKI_PREFIX) + 32:
        raise ValueError("not an Ed25519 SubjectPublicKeyInfo")
    return der[len(_ED25519_SPKI_PREFIX):]


def proposed_entry(close_record: dict, signer) -> dict:
    """The hashedrekord entry for a close record, signed with Ed25519ph by the receipt's own key."""
    artifact = record_body(close_record)
    sig = ed25519.sign_ph(signer._seed, artifact)
    return {"apiVersion": "0.0.1", "kind": "hashedrekord",
            "spec": {"data": {"hash": {"algorithm": "sha512", "value": hashlib.sha512(artifact).hexdigest()}},
                     "signature": {"content": base64.b64encode(sig).decode(),
                                   "publicKey": {"content": base64.b64encode(ed25519_pem(signer.public)).decode()}}}}


def _close(path) -> dict:
    lines = [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines or lines[-1].get("type") != "close":
        raise ValueError("receipt has no close record; close() it before anchoring")
    return lines[-1]


def bundle_path(path) -> Path:
    return Path(str(path) + ".anchor.json")


def upload(path, signer, *, log_url: str = DEFAULT_LOG, timeout: float = 30.0) -> dict:
    """POST the anchor entry to the log and save the bundle next to the receipt. The entry is public and permanent."""
    entry = proposed_entry(_close(path), signer)
    req = urllib.request.Request(log_url.rstrip("/") + "/api/v1/log/entries", data=json.dumps(entry).encode(),
                                 headers={"Content-Type": "application/json", "Accept": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        (uuid, logged), = json.loads(resp.read()).items()
    bundle = {"format": BUNDLE_FORMAT, "log_url": log_url, "uuid": uuid, "entry": logged}
    bundle_path(path).write_text(json.dumps(bundle, indent=1) + "\n", encoding="utf-8")
    return bundle


# ---- offline verification ----

def _jcs(obj) -> bytes:
    # RFC 8785 coincides with sorted, compact json.dumps for objects holding only strings and integers, as here.
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _node(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


def inclusion_root(index: int, size: int, leaf: bytes, hashes: list) -> bytes | None:
    """RFC 9162 section 2.1.3.2: the root an inclusion proof leads to, or None if the proof has the wrong shape."""
    if not 0 <= index < size:
        return None
    fn, sn, r = index, size - 1, leaf
    for p in hashes:
        if sn == 0:
            return None
        if fn & 1 or fn == sn:
            r = _node(p, r)
            if not fn & 1:
                while fn and not fn & 1:
                    fn >>= 1
                    sn >>= 1
        else:
            r = _node(r, p)
        fn >>= 1
        sn >>= 1
    return r if sn == 0 else None


def parse_checkpoint(text: str):
    """Signed note: 'origin\\nsize\\nb64root\\n[other lines]\\n\\n— name b64sig\\n...'. Returns (note, size, root, sigs)."""
    if "\n\n" not in text:
        raise ValueError("checkpoint has no signature block")
    note, sigblock = text.split("\n\n", 1)
    note += "\n"
    lines = note.split("\n")
    size, root = int(lines[1]), base64.b64decode(lines[2])
    sigs = []
    for ln in sigblock.strip("\n").split("\n"):
        if not ln.startswith("— "):
            raise ValueError("bad signature line")
        _, name, b64 = ln.split(" ", 2)
        sigs.append((name, base64.b64decode(b64)))
    return note, size, root, sigs


def verify_checkpoint(text: str, log_pem: bytes) -> bool:
    try:
        note, _, _, sigs = parse_checkpoint(text)
    except (ValueError, IndexError):
        return False
    hint = hashlib.sha256(p256.der_from_pem(log_pem)).digest()[:4]
    return any(raw[:4] == hint and p256.verify(log_pem, note.encode("utf-8"), raw[4:]) for _, raw in sigs)


def log_id(log_pem: bytes) -> str:
    return hashlib.sha256(p256.der_from_pem(log_pem)).hexdigest()


def verify_entry(entry: dict, log_keys) -> list:
    """Log-side checks only (no receipt): which pinned key, SET, inclusion proof, checkpoint. Returns [(code, detail)]."""
    out = []
    keys = {log_id(k): k for k in log_keys}
    key = keys.get(entry.get("logID"))
    if key is None:
        return [("anchor_untrusted_log", f"logID {str(entry.get('logID'))[:16]}... is not a pinned log key")]
    ver = entry.get("verification") or {}
    payload = {k: entry[k] for k in ("body", "integratedTime", "logID", "logIndex")}
    try:
        set_ok = p256.verify(key, _jcs(payload), base64.b64decode(ver["signedEntryTimestamp"]))
    except (KeyError, ValueError):
        set_ok = False
    if not set_ok:
        out.append(("anchor_set_invalid", "signed entry timestamp does not verify"))
    proof = ver.get("inclusionProof") or {}
    try:
        leaf = hashlib.sha256(b"\x00" + base64.b64decode(entry["body"])).digest()
        root = inclusion_root(int(proof["logIndex"]), int(proof["treeSize"]), leaf,
                              [bytes.fromhex(h) for h in proof["hashes"]])
        _, cp_size, cp_root, _ = parse_checkpoint(proof["checkpoint"])
        if root is None or root.hex() != proof["rootHash"]:
            out.append(("anchor_inclusion_invalid", "inclusion proof does not lead to rootHash"))
        elif cp_root.hex() != proof["rootHash"] or cp_size != int(proof["treeSize"]):
            out.append(("anchor_inclusion_invalid", "rootHash or treeSize differs from the checkpoint"))
        if not verify_checkpoint(proof["checkpoint"], key):
            out.append(("anchor_checkpoint_invalid", "checkpoint signature does not verify against the log key"))
    except (KeyError, ValueError, IndexError) as e:
        out.append(("anchor_inclusion_invalid", f"inclusion proof unreadable: {e}"))
    return out


def verify_anchor(path, bundle: dict | None, *, log_keys, max_delay: float = 3600, require: bool = False) -> list:
    """All anchor checks for one receipt. Returns [(code, detail)]; empty means the anchor holds."""
    if bundle is None:
        return [("anchor_missing", "no anchor bundle")] if require else []
    try:
        if bundle.get("format") != BUNDLE_FORMAT:
            raise ValueError(f"bundle format {bundle.get('format')!r}")
        entry = bundle["entry"]
        body = json.loads(base64.b64decode(entry["body"]))
        if body.get("kind") != "hashedrekord" or body["spec"]["data"]["hash"]["algorithm"] != "sha512":
            raise ValueError("entry is not a sha512 hashedrekord")
        logged_hash = body["spec"]["data"]["hash"]["value"]
        entry_key = ed25519_from_pem(base64.b64decode(body["spec"]["signature"]["publicKey"]["content"]))
        entry_sig = base64.b64decode(body["spec"]["signature"]["content"])
    except (KeyError, ValueError, TypeError) as e:
        return [("anchor_malformed", str(e))]

    out = verify_entry(entry, log_keys)
    try:
        close = _close(path)
    except ValueError as e:
        return out + [("anchor_mismatch", str(e))]
    artifact = record_body(close)
    if entry_key.hex() != close.get("key", "").lower():
        out.append(("anchor_key_mismatch", "the log entry was made with a different key from the receipt's"))
    elif not ed25519.verify_ph(entry_key, artifact, entry_sig):
        out.append(("anchor_bad_signature", "the entry's Ed25519ph signature does not cover this close record"))
    if logged_hash != hashlib.sha512(artifact).hexdigest():
        out.append(("anchor_mismatch", "the logged hash is not this receipt's close record"))
    t = entry.get("integratedTime")
    if isinstance(t, int):
        if t - close["t"] > max_delay:
            out.append(("anchor_late", f"anchored {int(t - close['t'])} s after the receipt closed (max {int(max_delay)})"))
        elif close["t"] - t > 300:
            out.append(("anchor_late", f"anchored {int(close['t'] - t)} s before the receipt says it closed"))
    return out
