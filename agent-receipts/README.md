# agent-receipts

A receipt for what an AI agent's tool calls actually did, that someone who was not there can check.

Wrap each tool call. Every call becomes one record: the tool, the exact arguments, the result or the error, when it ran, where
its inputs came from, and which earlier calls it used. Each record is signed with the agent's Ed25519 key and names the hash
of the record before it. A third party with the receipt file and the public key can then check, offline, that nothing was
edited, removed, reordered or added, that the receipt was not cut short, and that it was signed by the key the deployer
vouched for. Calls declared safe to re-run can be replayed against the tools to see whether they still give the same answer.

v0.1. Stdlib only (Ed25519 is implemented in pure Python, and `cryptography` is used instead when it is installed). Python 3.10+.
No server, no service, nothing leaves the machine.

## Quickstart (5 minutes)

Every command here was run as written, in a fresh virtualenv.

```sh
pip install "git+https://github.com/Yatsuiii/reproduction-receipts#subdirectory=agent-receipts"
receipt keygen agent.key                 # private seed, written 0600; prints the public key
```

Save as `quickstart.py` and run it:

```python
from agent_receipts import Recorder, Signer, receipted

rec = Recorder("run.jsonl", signer=Signer.from_file("agent.key"), actor="me@example.test")

@receipted(rec, sources=["kb:demo"], replayable=True)
def search(query: str) -> dict:
    return {"query": query, "hits": ["kb/refunds.md"]}

@receipted(rec)
def send_reply(to: str, body: str) -> dict:
    return {"queued": True}

search("refund window")
send_reply("c@example.test", "Refunds within 30 days.")
print("anchor:", rec.close())
```

Check it the way a third party would, then tamper with it:

```sh
echo "me@example.test=$(receipt pubkey agent.key)" > public_key.txt
receipt verify run.jsonl                  # VALID, exit 0
sed -i 's/30 days/365 days/' run.jsonl
receipt verify run.jsonl                  # INVALID: bad_signature, digest_mismatch, chain_broken; exit 1
```

`receipt verify` picks up `public_key.txt` and `anchor.txt` next to the receipt, and says so in its output. The public key
only means something if it reached the verifier separately from the receipt.

To stop whoever holds the key from rewriting the receipt later, anchor it in Sigstore's public Rekor log
([below](#anchoring-in-a-public-log)):

```sh
receipt log-key > rekor.pub               # once; keep it, this is the key you pin
receipt anchor run.jsonl --key agent.key  # public and permanent; writes run.jsonl.anchor.json
receipt verify run.jsonl --log-key rekor.pub --require-anchor
```

These three commands have not been run against the live log yet (see the anchoring section for why); everything above them has.

Two ideas come from earlier work in this repository:

- From [Custody](../custody/): every call carries its `sources`, and `derived_from` links it to the calls whose output it used.
  `verify(..., revoked=["kb:prod"])` marks every call that used a revoked source, directly or through a chain of calls, as
  `stale`.
- From [Stalefence](../stalefence/): `call(..., fence=...)` checks the premises the action depends on before running it. If one
  changed, the tool is not run, a `fenced` record is written, and `Fenced` is raised. It takes stalefence's
  `Premises.changed(...)` directly (tested in `tests/test_recorder.py`).

Failures are recorded, not dropped: a tool that raises gets an `error` record, a tool whose result cannot be stored gets one too
(it ran, so the receipt says so), and a fenced call gets a `fenced` record.

## Anchoring in a public log

v0 had one blind spot: whoever holds the signing key can rewrite the whole receipt and re-sign it. `receipt anchor` closes most
of it. It publishes the SHA-512 of the receipt's close record to [Sigstore's Rekor](https://docs.sigstore.dev/logging/overview/)
transparency log, signed with the receipt's own key (Ed25519ph, the form Rekor accepts for Ed25519 keys). The log's response
(a signed entry timestamp and a Merkle inclusion proof) is saved next to the receipt. A verifier then checks it with no network,
against the log's public key pinned once. Spec: [ANCHOR.md](ANCHOR.md).

The tamper cases were frozen before the code ([anchor_injections/](anchor_injections/), [results](results/anchor_injections.md)):

| verifier | attacks caught (of 11) | of those needing the signing key (of 4) |
| --- | --- | --- |
| v0, no anchor (baseline) | 0 | 0 |
| with a Rekor anchor | 10 | 3 |

What it catches: rewriting after anchoring (the logged hash no longer matches), patching the logged hash in the bundle (the
log's signatures break), re-anchoring a rewrite later (the log's timestamp is days after the receipt closed), an entry from a
log you did not pin, a flipped proof or signature byte, someone else's anchor attached to your receipt, and a missing anchor
when one is required.

What it still misses: a key holder who rewrites, moves every timestamp forward to match, and anchors the rewrite as a new
entry. The log then holds both versions, but an offline verifier is shown only one. Catching that needs an online search of
the log for every entry made with the key, which this does not do yet.

How far this has been tested, plainly:

- The tamper cases run against a local stand-in for Rekor ([fakelog.py](anchor_injections/fakelog.py)), because the
  network policy of the machine this was built on blocks `rekor.sigstore.dev`.
- CI checks the offline verifier against real entries fetched read-only from the live log
  ([tests/test_rekor_live.py](tests/test_rekor_live.py)): signed entry timestamp, inclusion proof and checkpoint. That tests
  the log's formats, not the upload.
- The upload (`receipt anchor`) has not been run against the live log. It publishes a permanent public entry, so it sits in a
  manual workflow ([anchor-demo.yml](../.github/workflows/anchor-demo.yml)) that runs only when started by hand.
- Ed25519ph matches the RFC 8032 test vector. P-256 verification is pure Python and cross-checked against `cryptography`.

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

## Framework adapters: LangGraph, OpenAI Agents SDK, CrewAI

Any tool function can be wrapped with `@receipted(rec, sources=[...], replayable=...)`. The wrapper keeps the function's name,
docstring and signature, so a framework builds the same tool schema from it, and it sits inside the framework's own error
handling, so a tool that raises is recorded as `error` even when the framework turns the exception into text for the model.
Thin helpers per framework, in `agent_receipts/adapters/`:

| framework | helper |
| --- | --- |
| LangGraph / LangChain | `wrap_tools(tools, rec, policy)`, then `ToolNode(tools)` as usual |
| OpenAI Agents SDK | `receipted_function_tool(fn, rec, ...)` in place of `function_tool(fn)` |
| CrewAI | `wrap_tool(tool, rec, ...)` for a BaseTool or an `@tool` tool |

Each has a worked example in [`examples/frameworks/`](examples/frameworks/). The same plan of four tool calls, one of which
fails, runs through each framework's own runtime: a LangGraph `StateGraph` with `ToolNode`, `Runner.run` in the Agents SDK,
and a CrewAI `Crew`. A scripted stand-in replaces the model in each, so nothing calls an API and every run costs $0. The tamper
cases, the expected verdicts, and a written guess of which frameworks mark the failure in their own record were frozen in
[`adapter_injections/`](adapter_injections/) before any adapter code existed. The baseline is each framework's own record of
the run: LangGraph's messages, the Agents SDK's `new_items`, and CrewAI's step callback.

| | LangGraph 1.2.24 | Agents SDK 0.20.0 | CrewAI 1.15.44 |
| --- | --- | --- | --- |
| failed call recorded as `error` in the receipt | yes | yes | yes |
| framework's own record marks the failure as an error | yes (`ToolMessage.status`) | no, only an error string | no, only an error string |
| tool executions in the receipt / in the framework's own record | 4 / 4 | 4 / 4 | **9 / 4** |
| tamper cases caught: receipt / framework's own record | 4 / 0 of 4 | 4 / 0 of 4 | 4 / 0 of 4 |

Results: [LangGraph](results/langgraph_example.json), [Agents SDK](results/openai_agents_example.json),
[CrewAI](results/crewai_example.json). The guesses about which framework marks its own failures were all right.

Two things the examples found:

- **CrewAI re-ran the failing tool six times on its own, and its own record shows one call.** A counter inside the tool
  confirmed six real executions, so the receipt is right and the frozen expectation (4 calls) was wrong about the framework.
  This is left as a departure, explained in [results/departures.md](results/departures.md). For a lookup that is harmless. For
  a tool that charges a card or sends an email, it would be six charges or six emails, with one visible in the framework's
  record.
- **LangGraph's default `ToolNode` stops the graph on a plain exception.** That default run is kept in
  [`examples/frameworks/out/langgraph/default_handler/`](examples/frameworks/out/langgraph/default_handler/): the receipt is
  `unclosed` but still holds the failed call. The main run sets `handle_tool_errors=True`.

What these examples do not show: behaviour with a real model choosing the calls, streaming, parallel tool calls, or
framework features beyond plain function tools (LangChain tools without a function behind them, Agents SDK hosted tools,
handoffs, CrewAI delegation).

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
- **Anything without an anchor, against the key holder.** The operator holding the key can rewrite and re-sign. Anchor the
  receipt in Rekor, or hand the close hash to someone they cannot reach. Even anchored, a rewrite with every timestamp moved
  and a fresh anchor is caught only by an online search of the log (above).
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
with `cryptography` and `mcp` installed, including the MCP example. A second job installs the three frameworks at the pinned
versions above and runs their examples. Both jobs verify the committed example receipts with the CLI.

## Not in v0

An adapter for Google ADK (a plain tool function already works with `@receipted`), an anchor service, key rotation, and
receipts that span more than one agent process.
