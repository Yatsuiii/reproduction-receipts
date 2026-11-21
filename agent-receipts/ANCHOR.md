# Anchoring a receipt in a public transparency log

Written before the implementation, with the tamper cases in [`anchor_injections/`](anchor_injections/). Frozen.

## The gap it closes

Whoever holds the signing key can rewrite a receipt and re-sign every record (`holder_rewrite` in the v0 injections). Only a
record of the receipt kept by someone else catches that. An anchor puts that record in a public append-only log the key
holder does not control, and the log's own signatures let anyone check the anchor offline afterwards.

## What gets anchored

The artifact is the receipt's `close` record: its canonical bytes as defined in FORMAT.md (the record without `sig`). The
close record names the hash of the record before it, so it commits to the whole chain.

The log is Sigstore's public Rekor (v1 API, `https://rekor.sigstore.dev`), entry type `hashedrekord` v0.0.1, which accepts
Ed25519 keys with Ed25519ph signatures over a SHA-512 digest. The anchor entry is:

```json
{"apiVersion": "0.0.1", "kind": "hashedrekord",
 "spec": {"data": {"hash": {"algorithm": "sha512", "value": "<hex SHA-512 of the close record's canonical bytes>"}},
          "signature": {"content": "<base64 Ed25519ph signature of those bytes>",
                        "publicKey": {"content": "<base64 of the PEM SubjectPublicKeyInfo of the receipt's key>"}}}}
```

It is signed with the receipt's own key, so the log entry is bound to the same identity as the receipt.

## The anchor bundle

Saved next to the receipt as `<receipt>.anchor.json`:

```json
{"format": "agent-receipts-anchor/rekor-v1",
 "log_url": "https://rekor.sigstore.dev",
 "uuid": "...",
 "entry": {"body": "<base64>", "integratedTime": 0, "logID": "<hex>", "logIndex": 0,
           "verification": {"signedEntryTimestamp": "<base64>",
                            "inclusionProof": {"checkpoint": "...", "hashes": ["<hex>"], "logIndex": 0,
                                               "rootHash": "<hex>", "treeSize": 0}}}}
```

`entry` is the log's response for the entry, unchanged.

## Offline verification

Given the receipt, the bundle, the receipt trust list, and the log's public key (ECDSA P-256, pinned by the verifier), with no
network:

| code | failure when |
| --- | --- |
| `anchor_missing` | an anchor is required and there is no bundle |
| `anchor_malformed` | the bundle or the entry body does not parse, or is not a hashedrekord with sha512 |
| `anchor_untrusted_log` | `logID` is not the SHA-256 of a pinned log key's DER encoding |
| `anchor_set_invalid` | the signed entry timestamp does not verify: ECDSA P-256 over SHA-256 of the RFC 8785 canonical JSON of `{body, integratedTime, logID, logIndex}` |
| `anchor_inclusion_invalid` | the RFC 6962 inclusion proof of `SHA-256(0x00 ‖ body)` does not reach `rootHash`, or `rootHash` differs from the checkpoint's |
| `anchor_checkpoint_invalid` | the checkpoint's signed-note signature does not verify against the log key |
| `anchor_key_mismatch` | the entry's public key is not the receipt's key |
| `anchor_bad_signature` | the entry's Ed25519ph signature does not verify over the close record's bytes |
| `anchor_mismatch` | the entry's sha512 is not the SHA-512 of this receipt's close record (or the receipt has no close) |
| `anchor_late` | `integratedTime` is more than `max_delay` seconds (default 3600) after the close record's `t`, or more than 300 s before it |

## What it still does not prove

A key holder who rewrites the receipt, shifts every timestamp forward, and anchors the rewrite as a new entry produces a
receipt that passes offline: the log holds both entries, but the verifier is shown only one. Catching that needs a search of
the log for every entry made with the key, which is an online check. It is listed as an expected blind spot.

The log is a third party that is trusted not to rewrite its own history. Rekor is designed to make that detectable by
monitors, but this verifier does not check consistency between checkpoints.

## Python API the injections are written against

```python
from agent_receipts import rekor, p256

entry = rekor.proposed_entry(close_record, signer)        # the hashedrekord JSON above
bundle = rekor.upload(path, signer, log_url=...)          # POST /api/v1/log/entries, writes <path>.anchor.json
findings = rekor.verify_anchor(path, bundle, log_keys=[pem_bytes], max_delay=3600)   # list of (code, detail)
verify(path, trusted=..., anchor_bundle=bundle, log_keys=[pem], require_anchor=False)  # adds those codes to the report

p256.generate() -> (priv_int, pub_pem_bytes)                # for the simulated log in the injections
p256.sign(priv_int, msg_bytes) -> der_sig                   # ECDSA over SHA-256(msg)
p256.verify(pub_pem_bytes, msg_bytes, der_sig) -> bool
ed25519.sign_ph(seed, msg) / ed25519.verify_ph(pub, msg, sig)   # Ed25519ph, RFC 8032 section 5.1
```
