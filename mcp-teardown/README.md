# MCP teardown receipts

Same claim as the rest of this repo, pointed at agent tooling: a receipt that a third party can check
without trusting me, naming the artefact that ran, the exact commands, every deviation and every failed run.

This adapter takes the teardown probe from [`agent-disclosure-fidelity`](../agent-disclosure-fidelity/)
(the one that armed the smithery-cli finding at FAIL 10/10 unpatched, PASS 10/10 patched) and runs it
against published stdio MCP servers in bulk.

## The question

When a client shuts a stdio MCP server down the way the MCP lifecycle spec describes (close stdin, wait,
SIGTERM, wait, SIGKILL), are processes the server started still running afterwards?

## Result so far

[Run 2](runs/20261121-run2/RESULT.md): 1,000 servers, 738 live, 49 with a child process, **0 confirmed**.
The seven flagged servers each start an intentional shared daemon. [Run 1](runs/20261121-run1/NOTE.md)
is kept as a failed run (runner bug).

## Pieces

| File | What it does |
|---|---|
| `targets.py` | Builds `targets.jsonl` from the official MCP registry: latest active version, stdio, npm or PyPI, a GitHub repo, no required argument we would have to invent, one server per repo. Records the registry snapshot's sha256. |
| `runner.py` | Arms itself on control fixtures, then installs each target without running install scripts, launches its entry point directly as `nobody` with no network, does a real handshake, applies the spec shutdown, and reads `/proc` for anything still carrying the trial tag. |
| `receipt.py` | Writes one Markdown receipt per CONFIRMED target. Sends nothing. |
| `fixtures/control_server.mjs` | Known-leaky and known-clean control servers. The batch stops if the leaky one is not CONFIRMED or the clean one does not pass 10 of 10. |

## Verdicts

| Verdict | Meaning | Receipt? |
|---|---|---|
| `CONFIRMED` | pid-only shutdown left residue in 10/10, process-group shutdown left none in 10/10, every handshake answered | yes, after a manual prior-art check |
| `RESIDUE_BOTH_ARMS` | residue in 10/10 under both arms (for example the server exits on stdin EOF and its children do not) | not yet: there is no fixed arm to compare against |
| `UNCONFIRMED` | screen showed residue but the 10 + 10 did not meet the bar | no |
| `PASS_SCREEN` | one screening trial, nothing left behind | no |
| `DEAD` | install failed, no entry point, or no answer to initialize | no, but the reason is kept |

## Run it

Linux, root (for `unshare --net` and dropping to `nobody`), Node and `uv` on PATH.

```
python3 mcp-teardown/targets.py --limit 1000
sudo python3 mcp-teardown/runner.py --workers 4 --out /var/tmp/mcpt-results/run1
python3 mcp-teardown/receipt.py --results /var/tmp/mcpt-results/run1 --out mcp-teardown/receipts/run1
```

## What this does not cover

- No tool is called. Servers that only start children when a tool runs are not exercised.
- A server that clears its children's environment drops the tag, so its residue is invisible here.
  That makes the run miss leaks, never invent them.
- Servers that need the network or a real credential to start come out `DEAD`, not clean.
- A residual process may be intended. The receipt says what the process table showed and nothing more.
