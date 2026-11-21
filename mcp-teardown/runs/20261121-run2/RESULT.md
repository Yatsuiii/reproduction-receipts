# Run 2, 2026-11-21: 1,000 stdio MCP servers, zero receipts

Armed: negative probe empty, leaky control CONFIRMED (10/10 vs 0/10), clean control 10/10.
Runner as of commit dd1ecb4. Wall clock 2,980 s on 4 vCPU, 4 workers. No paid API or model calls; marginal cash cost $0.

| Verdict | Count |
|---|---:|
| PASS_SCREEN | 731 |
| DEAD | 262 |
| RESIDUE_BOTH_ARMS | 4 |
| UNCONFIRMED | 3 |
| CONFIRMED | **0** |

Of the 738 servers that completed a handshake, 49 had a child process alive just before shutdown. That
is the real denominator: a server with no children cannot leave any behind.

## The seven flagged servers are shared daemons, not leaks

Every flagged residue is a process whose command line names itself a background daemon, started with
its own session so that process-group signals do not reach it, and it exits on stdin EOF in every
trial (pid and group arms alike):

| Server | Residual command (trimmed) | pid arm | group arm |
|---|---|---:|---:|
| qualixar/superlocalmemory | `python -m superlocalmemory.server.unified_daemon --start --port=8765` | 10/10 | 10/10 |
| junyeong-nero/kitsune | `python -m kitsune.bridge` | 10/10 | 10/10 |
| software-mansion/argent | `node .../tool-server.cjs start` | 10/10 | 10/10 |
| imgly/codesign | `node .../runtime/cli/main.js server start` | 10/10 | 10/10 |
| reticlehq/reticle | `node .../reticle.js _daemon --port 4400 --headless` | 8/10 | 8/10 |
| yocontra/pulsar | see `flagged/` | 5/10 | 5/10 |
| nikolai-vysotskyi/trace-mcp | see `flagged/` | 5/10 | 5/10 |

A daemon meant to outlive one MCP session and be shared across sessions is a design choice. Nothing
in this run shows any of them is unintended, so none gets a receipt. Per-target JSON is in `flagged/`.

## What this says

The smithery-cli shape (a grandchild orphaned because only the direct child was signalled) did not
show up in published servers. Most servers here exit on stdin EOF on their own. That bug lived in a
program that *spawns* MCP servers, not in a server. Checking servers was the cheaper list to build
and the wrong place to look.

## Limits

No tool was called; servers that start children only on a tool call were not exercised. 262 servers
never answered initialize in this sandbox (no network, placeholder-free environment, no arguments
beyond registry defaults). A server that clears its children's environment drops the tag, so a leak
there would be missed.
