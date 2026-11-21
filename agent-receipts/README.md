# agent-receipts

A receipt for what an AI agent's tool calls actually did, that someone who was not there can check.

Wrap each tool call. Every call becomes one record: the tool, the exact arguments, the result or the error, when it ran, where
its inputs came from, and which earlier calls it used. Each record is signed with the agent's Ed25519 key and names the hash
of the record before it. A third party with the receipt file and the public key can then check, offline, that nothing was
edited, removed, reordered or added, that the receipt was not cut short, and that it was signed by the key the deployer
vouched for. Calls declared safe to re-run can be replayed against the tools to see whether they still give the same answer.

v0. Stdlib only (Ed25519 is implemented in pure Python, and `cryptography` is used instead when it is installed). Python 3.10+.
No server, no service, nothing leaves the machine.

```python
from agent_receipts import Recorder, Signer, verify

rec = Recorder("run.jsonl", signer=Signer.from_file("agent.key"), actor="billing-agent@acme")
note = rec.call("read_file", read_file, {"path": "policy.txt"}, sources=["file:policy.txt"], replayable=True)
rec.call("send_email", send_email, {"to": "c@x.test", "body": "..."}, derived_from=[rec.last_seq])
anchor = rec.close()            # publish this hash somewhere the agent's operator cannot rewrite

verify("run.jsonl", trusted={"billing-agent@acme": PUBLIC_KEY_HEX}, anchor=anchor).ok
```

```sh
python -m agent_receipts keygen agent.key        # prints the public key; the seed file is written 0600
python -m agent_receipts verify run.jsonl --trust billing-agent@acme=PUBHEX --anchor HASH [--revoke SOURCE]
```

Two ideas come from earlier work in this repository:

- From [Custody](../custody/): every call carries its `sources`, and `derived_from` links it to the calls whose output it used.
  `verify(..., revoked=["kb:prod"])` marks every call that used a revoked source, directly or through a chain of calls, as
  `stale`.
- From [Stalefence](../stalefence/): `call(..., fence=...)` checks the premises the action depends on before running it. If one
  changed, the tool is not run, a `fenced` record is written, and `Fenced` is raised. It takes stalefence's
  `Premises.changed(...)` directly (tested in `tests/test_recorder.py`).

Failures are recorded, not dropped: a tool that raises gets an `error` record, a tool whose result cannot be stored gets one too
(it ran, so the receipt says so), and a fenced call gets a `fenced` record.

## Worked example: an MCP client

[`examples/mcp/`](examples/mcp/) runs a real MCP server (mcp 2.3.0, stdio) and a client whose session is wrapped in
`RecordedSession`. The agent's plan is a fixed script of five tool calls, not a model, so the run is free and repeatable; the
receipt sits at the tool-call boundary, which is the same whichever chose the calls.

```sh
pip install "mcp>=2,<3"
python agent-receipts/examples/mcp/run.py
```

What the committed run in [`examples/mcp/out/`](examples/mcp/out/) shows ([summary](results/mcp_example.json)):

| check | result |
| --- | --- |
| verify with the trust list and the anchor | valid, 5 calls, including the failed `lookup_order` as `error` |
| replay against the same server | 4 replayable calls match; `send_reply` is not replayable by declaration |
| replay against the server with its knowledge base changed (`KB_VERSION=2`) | `search_kb` mismatches, the rest match |
| revoke the source `kb:support-kb` | `search_kb` and the reply derived from it are marked stale |
| change "refund approved" to "refund denied" in the reply's arguments | invalid: `bad_signature`, `digest_mismatch`, `chain_broken` |

Wall clock 2.3 s, cost $0. Check the committed receipt yourself:

```sh
cd agent-receipts
python -m agent_receipts verify examples/mcp/out/receipt.jsonl --trust "$(cat examples/mcp/out/public_key.txt)" --anchor "$(cat examples/mcp/out/anchor.txt)"
```

The first run of this example found a bug in the adapter: mcp 2.x renamed `isError` to `is_error`, the adapter only checked
the old name, and the failed lookup was recorded as `ok`. That run's summary is kept in
[`results/mcp_example.run1.json`](results/mcp_example.run1.json). The adapter now checks both, with a test for each.

## Results, next to the cheap baselines

[`run_injections.py`](run_injections.py) records one clean session, then applies 14 attacks and 2 non-attack checks (revoked
source, changed tool). The verdict each verifier had to give was written and frozen before the implementation existed. Two
cheap baselines get the same attacks: a plain JSONL tool log, which is what most agent stacks write today, and an unsigned hash
chain. Against the baselines the attacker also repairs whatever the format lets anyone repair, such as recomputing an unsigned
chain. [Full table](results/injections.md).

| verifier | attacks caught |
| --- | --- |
| plain JSONL log | 1 / 14 (only a line that is not JSON) |
| unsigned hash chain | 5 / 14 (one of those is a flaw in the simulated attacker, see below) |
| agent-receipts | 13 / 14 |

The one it misses is the one it has to miss. Whoever holds the signing key can rewrite the whole receipt and re-sign it
(`holder_rewrite`). Only an anchor, the close hash published at close time somewhere the key holder cannot change, catches that
(`holder_rewrite_with_anchor`). With an anchor, the unsigned hash chain catches it too. What the signature adds over a chain
with an anchor is binding the receipt to a key someone vouched for, and catching edits when no anchor was published.

One result departs from the frozen expectations and is left in. The unsigned chain caught `reorder` through `clock_backwards`
because the simulated attacker rewrote sequence numbers and hashes but not timestamps. A real attacker would rewrite those
too, so the baseline's 5 is really 4. [Departures](results/departures.md).

Cost of recording ([`bench_overhead.py`](bench_overhead.py), [results](results/overhead.json), one machine, 500 calls): about
146 µs per call with `cryptography` and 3.2 ms per call in pure Python, against about 4 µs for a plain JSONL append. A receipt
record is about 4 times the size of the plain log line, because it stores digests, the key and the signature.

## What a receipt does not prove

- **That the tool did what the record says.** The record is what the wrapper saw cross the tool boundary in the agent's own
  process. If the host running the agent is compromised, it can sign a lie. A receipt proves the key holder said this, in this
  order, and did not change it afterwards.
- **Anything without the anchor, against the key holder.** The operator holding the key can rewrite and re-sign. Publish the
  close hash somewhere they cannot edit: a ticket, an email to the reviewer, a git commit.
- **Who a person is.** Identity is a key. The `actor` name means only what the trust list says it means; getting the right
  public key to the verifier is the deployer's job.
- **When things happened.** Timestamps are the recorder's own clock. The verifier checks they never go backwards, nothing more.
  There is no trusted timestamping.
- **Calls that were never wrapped.** A tool called around the recorder leaves no record. Completeness holds only for calls
  that went through it.
- **That a replay match means the result is right.** Replay shows the tool still answers the same way. It is only meaningful
  for calls the deployer declared deterministic and safe to re-run; side-effecting calls are never re-run.
- **Side-channel safety of the pure-Python signer.** It is checked against the RFC 8032 vectors and against `cryptography`,
  but it is not constant-time. Verification is fine anywhere. For signing in production, install `cryptography`.
- **Truncation of an unclosed receipt.** If the agent crashes before `close()`, the verifier reports `unclosed`. It cannot tell a
  crash from someone cutting the file.

## How it was built

Same rules as the rest of this repository.

1. **Failure injections first.** [`FORMAT.md`](FORMAT.md) (the format and every verifier code) and
   [`injections/`](injections/) (the clean session, the 16 mutations, and the verdict each verifier must give) were committed
   before `agent_receipts/` existed. See the commit history of this folder.
2. **Frozen.** [`FROZEN.json`](FROZEN.json) pins those files by SHA-256. `scripts/hooks/pre-commit` runs
   [`check_frozen.py`](check_frozen.py) and blocks a commit that changes one without updating the registry, and every change is
   logged in [`FROZEN_CHANGES.md`](FROZEN_CHANGES.md). Install with `git config core.hooksPath scripts/hooks`.
3. **A cheap baseline next to every number**, as above.
4. **Failures left visible**: the departure from the frozen expectations and the adapter bug found by the first example run
   are kept, not fitted away.

CI (`.github/workflows/agent-receipts.yml`) runs the tests twice: once with nothing installed (pure-Python Ed25519), and once
with `cryptography` and `mcp` installed, including the MCP example. It then verifies the committed example receipt with the CLI.

## Not in v0

Adapters for Google ADK and other frameworks (any async `call_tool(name, arguments)` already works through `RecordedSession`),
an anchor service, key rotation, and receipts that span more than one agent process.
