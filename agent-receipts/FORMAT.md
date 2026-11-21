# Receipt format `agent-receipts/0`

Written before the implementation, together with the failure injections in [`injections/`](injections/). The implementation
has to meet this file, not the other way round. Changes are logged in [`FROZEN_CHANGES.md`](FROZEN_CHANGES.md).

A receipt is one JSON Lines file. Each line is one record. Every record is signed on its own and names the hash of the record
before it, so the file is a signed hash chain.

## Records

Common fields on every record:

| field | meaning |
| --- | --- |
| `type` | `open`, `call` or `close` |
| `format` | `agent-receipts/0` |
| `session` | random 128-bit hex id, the same on every record of one receipt |
| `seq` | 0 for `open`, then 1, 2, 3 ... with no gaps |
| `t` | seconds since the epoch when the record was written, from the recorder's clock (self-asserted) |
| `key` | Ed25519 public key of the signer, 64 hex chars |
| `prev` | `null` on `open`, otherwise the `hash` of the record before |
| `sig` | Ed25519 signature, 128 hex chars, over the record's canonical bytes |

`open` adds `actor` (the identity the key is bound to, a string chosen by the deployer) and `meta` (a JSON object).

`call` adds:

| field | meaning |
| --- | --- |
| `tool` | tool name |
| `args` | the arguments as JSON, or `null` when redacted |
| `args_sha256` | SHA-256 of the canonical bytes of the arguments (always present) |
| `status` | `ok`, `error` (the tool raised) or `fenced` (a premise changed, the tool was not run) |
| `result` | the result as JSON, or `null` when redacted, on error, or when fenced |
| `result_sha256` | SHA-256 of the canonical bytes of the result, `null` unless `status` is `ok` |
| `error` | the exception type and message on `error`, the changed premises on `fenced`, else `null` |
| `t_start` | when the call started; `t` is when it ended |
| `sources` | list of strings naming where the inputs came from (Custody); may be empty |
| `derived_from` | list of `seq` numbers of earlier calls whose output this call used |
| `replayable` | `true` when the deployer declared the tool safe and deterministic to re-run |

`close` adds `count`, the number of `call` records.

## Canonical bytes and hashes

`canonical(x)` is `json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` encoded as
UTF-8. A record's canonical bytes are `canonical` of the record with `sig` removed. Its `hash` is the SHA-256 hex of those bytes.
The signature is over those same bytes.

## What a verifier checks, and the code it reports

A verifier is given the receipt and a trust list mapping `actor` to public key. Optionally an anchor (a `close` hash the
recorder published somewhere else at close time) and a set of revoked sources.

| code | failure when |
| --- | --- |
| `malformed` | a line is not JSON, or a required field is missing or the wrong type |
| `bad_signature` | a signature does not verify against the record's own `key` |
| `untrusted_key` | the `key` is not the one the trust list gives for the receipt's `actor`, or the actor is not on it |
| `chain_broken` | a `prev` is not the hash of the record before it |
| `sequence` | `seq` is not 0, 1, 2 ... in file order, or `open` is not first |
| `session_mismatch` | a record carries a different `session` from the `open` |
| `unclosed` | the last record is not a `close` |
| `count_mismatch` | `close.count` differs from the number of `call` records |
| `clock_backwards` | a record's `t` is earlier than the record before it, or `t_start` > `t` |
| `digest_mismatch` | an inline `args` or `result` does not hash to its `*_sha256` |
| `anchor_mismatch` | an anchor was given and the `close` hash is not it |

Warning, not failure: `stale`, for every call whose `sources` include a revoked source, and every call that is transitively
`derived_from` one.

Replay is separate from verification. Given tool implementations, a replayer re-runs each `replayable` call with the recorded
`args` and reports `replay_match` or `replay_mismatch` per call, `not_replayable` for the rest. An `ok` call matches when the re-run
returns a result with the same `result_sha256`. An `error` call matches when the re-run raises again with the same `error`
text. A `fenced` call is never re-run.

## Python API the injections are written against

```python
from agent_receipts import Recorder, Signer, verify, replay, seal, record_hash

signer = Signer.from_seed(bytes32)            # or Signer.generate()
rec = Recorder(path, signer=signer, actor="name", clock=callable_returning_float, meta={})
out = rec.call("tool", fn, {"arg": 1}, sources=["file:x"], derived_from=[1], replayable=True)
rec.close()                                   # returns the close record's hash (the anchor)

report = verify(path, trusted={"name": signer.public_hex}, anchor=None, revoked=())
report.ok                                     # True when there is no failure finding
report.codes()                                # set of codes found, {"ok"} when there are none at all
report.stale                                  # sorted list of stale call seqs

rr = replay(path, tools={"tool": fn})         # rr.codes(): {"replay_match", "replay_mismatch", "not_replayable"}

seal(record_dict, signer)                     # sets key and sig in place; for re-signing in the injections
record_hash(record_dict)                      # hash as defined above
```
