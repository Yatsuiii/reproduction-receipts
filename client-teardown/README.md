# Client teardown receipts

Same claim as the rest of this repo, pointed at the programs that *launch* MCP servers: agent frameworks, SDKs
and agent CLIs. The [1,000-server sweep](../mcp-teardown/) found nothing on the server side and said the
smithery-cli shape lives in clients. This is that check.

## The question

When a client closes a stdio MCP server through its own documented API, is anything that server started
still running 10 seconds later, with the host still alive?

## Result

Run 1, 21 Nov 2026: 37 drivers covering 27 of the most-used projects run directly, plus 8 checked through their pinned SDK or source only,
4 scenarios each, 10 trials per cell. Reference controls armed in 120 of 120 trials.

**Two confirmed findings**, both FAIL 10/10, a passing negative control, and a patch that turns them clean 10/10:

| project | stars | what happens | patch | upstream report |
|---|---:|---|---|---|
| Pydantic AI 2.71.0 | 21k | Leaving `async with toolset`, or an `agent.run()` without one, does not stop the stdio server, though the docs say it does. A toolset built per request leaves one more server running per request (3 of 3 left, 10/10 trials). Cause: FastMCP's `keep_alive=True` default. | [patch](patches/pydantic-ai-close-stdio-on-exit.patch), `tests/test_mcp.py` passes | none found; [draft](drafts/pydantic-ai-issue.md) |
| Vercel AI SDK, `@ai-sdk/mcp` 2.0.102 | 28k | `close()` sends one SIGTERM and stops. A server that ignores SIGTERM keeps running, and a script that ends with `await client.close()` never exits (10/10). | [patch](patches/ai-sdk-mcp-stdio-close-sequence.patch), unit tests pass | none found; [draft](drafts/vercel-ai-issue.md) |

Neither draft has been posted anywhere.

**Everything else came out clean** on the three cells the MCP spec covers (exit on EOF, SIGTERM, SIGKILL),
except Roo Code's pinned SDK, below. Full table: [`runs/20261121-run1/TABLE.md`](runs/20261121-run1/TABLE.md).

## Scenarios

| scenario | fixture behaviour | a client must | contract |
|---|---|---|---|
| `clean` | exits on stdin EOF | close stdin | negative control: every target must be clean |
| `eof-ignore` | ignores EOF, exits on SIGTERM | send SIGTERM | MCP lifecycle spec, stdio shutdown step 2 |
| `term-ignore` | ignores EOF and SIGTERM | send SIGKILL | spec step 3 |
| `wrapped` | `wrapper.mjs` (does not pass signals on) running `eof-ignore` | signal the process group | not in the spec; the Python SDK and Zed do it, the TS SDK has an open issue (#2023) |

Residue is any process whose argv carries the trial tag ([`runner.py`](runner.py)). Each driver uses the
target's own public API (connect, list tools, call `ping`, close), prints `CLOSED`, and stays alive like a real
host. CLIs run their own `mcp list` command, which starts, handshakes and stops each server, with no model call.

Arming ([`drivers/reference.py`](drivers/reference.py)): a client that never signals must leave residue in the
three non-clean scenarios, a client that does the spec sequence on the pid must be clean except `wrapped`, and
one that does it on the process group must be clean everywhere. All 12 cells matched in all 10 trials.

## What the `wrapped` column means, and why nothing there is drafted

Most clients signal only the pid they started, so `wrapped` leaves residue for the TypeScript SDK (every
version tested), gemini-cli, Mastra, LangChain.js, mcp-use, OpenAI Agents JS, the Go SDK, mcp-go and rmcp
(Goose's spawn settings included). Clean: the Python SDK and everything built on it, opencode and Kilo.

Real launchers differ ([`launchers.py`](launchers.py), 10 trials each): **npx (npm 10.9.9) does not pass
SIGTERM on, 10/10; `uv run` does, 10/10.** So the shape is real for npx-launched servers. But it needs a server
that also ignores stdin EOF, and the 1,000-server sweep suggests that is rare. The spec only asks for the child
process to be signalled, and the TS SDK's version of this is already filed. That makes it contract-unclear,
not a bug report, and it is left here as a measured fact. One side effect worth knowing: under that shape
`qwen mcp list` never exits (killed at 120 s in 10/10 trials) while gemini-cli, which it forks, exits normally.

## Roo Code

Roo Code pins `@modelcontextprotocol/sdk` 1.12.0, whose `close()` never sends SIGKILL (`term-ignore` residue
10/10; fixed upstream in 1.24.0). The repository is archived, so there is no one to report it to.

## Coverage

Ranked by GitHub stars on 21 Nov 2026. Pinned commits: [`runs/20261121-run1/pins.txt`](runs/20261121-run1/pins.txt).

| project | stars | how it was checked |
|---|---:|---|
| opencode | 228k | real CLI 1.19.6, `opencode mcp list` |
| n8n | 212k | pins TS SDK 1.32.0; covered by the `ts-sdk-1.32.x` cells, not run directly |
| VS Code | 196k | source only: `mcpStdioStateHandler.ts` does the spec sequence with `killTree` |
| Dify | 162k | no stdio client (remote MCP only), out of scope |
| LangChain | 150k | `langchain-mcp-adapters` 0.3.2 (two paths), `@langchain/mcp-adapters` 2.0.3 |
| Codex | 136k | source only: its own launcher terminates and kills the process group |
| gemini-cli | 109k | real CLI 0.70.0, `gemini mcp list` |
| Zed | 95k | source only: `setsid` at spawn, `killpg(SIGKILL)` on drop |
| Cline | 72k | pins TS SDK 1.30.0; covered by the 1.29 and 1.32 cells |
| AutoGen | 62k | `autogen-ext` 0.7.5 `McpWorkbench` |
| CrewAI | 61k | crewai 1.15.44, `MCPServerAdapter` and native `MCPClient` |
| Goose | 57k | rmcp 3.9.0 with Goose's spawn settings (process group, `PR_SET_PDEATHSIG`) |
| Cherry Studio | 54k | pins `@modelcontextprotocol/client` 2.3.0; covered by the 2.4.0 cell |
| LlamaIndex | 53k | `llama-index-tools-mcp` 0.7.0 |
| Agno | 43k | agno 3.2.1 `MCPTools` |
| Continue | 36k | pins TS SDK 1.24.1 to 1.29.0; covered by the SDK cells |
| Qwen Code | 31k | real CLI 0.28.3, `qwen mcp list` |
| OpenAI Agents (Python, JS) | 31k, 4k | `openai-agents` 0.25.0, `@openai/agents-core` 0.22.0 |
| smolagents | 30k | smolagents 1.26.0 `MCPClient` |
| Mastra | 30k | `@mastra/mcp` 2.10.0 |
| Crush | 29k | Go SDK 1.8.0 cell; source shows it adds `Setpgid` and its own group kill |
| FastMCP | 29k | fastmcp 4.2.4 `Client` |
| Semantic Kernel | 29k | semantic-kernel 1.36.0 `MCPStdioPlugin` |
| Vercel AI SDK | 28k | `@ai-sdk/mcp` 2.0.102 |
| Kilo Code | 28k | real CLI 7.8.32, `kilo mcp list` |
| MCP Python SDK | 25k | mcp 2.3.0 |
| Roo Code | 24k | archived; pins TS SDK 1.12.0, which was run |
| Google ADK | 22k | google-adk 2.15.0 `McpToolset` |
| Pydantic AI | 21k | pydantic-ai-slim 2.71.0, three paths plus a `keep_alive=False` control |
| CAMEL | 18k | camel-ai 0.2.90 `MCPToolkit` |
| MCP TypeScript SDK | 14k | 1.12.0, 1.25.2, 1.29.0, 1.32.1, 1.32.2; client 2.4.0 |
| mcp-use | 11k | Python 1.7.1, `@mcp-use/client` 2.4.6 |
| mcp-go, Go SDK, Rust SDK | 9k, 5k, 4k | mcp-go 1.6.0, go-sdk 1.8.0, rmcp 3.9.0 |

## Deviations

- smolagents, CAMEL and AutoGen fail to import against `mcp` 2.x, which a fresh install resolves to. They were
  run with `mcp<2` (1.30.0). smolagents also needed `websockets` installed by hand. Agno needed `fastmcp<5`,
  which it asks for at runtime but does not install.
- The first batch crashed when one driver's `CLOSED` line had trailing output; the runner now parses the
  first JSON value and the JS targets were re-run.
- The first `cli-qwen` run captured output through a pipe, which a leftover server can inherit and so hang the
  driver itself. The driver now writes to a file and the whole target was re-run. The `wrapped` hang showed up
  in both runs, so it is qwen's. The first run is kept as
  [`runs/20261121-run1/cli-qwen.pipe-artifact.json`](runs/20261121-run1/cli-qwen.pipe-artifact.json).
- Projects marked "covered by" were not run themselves. The cell is the SDK version their lockfile pins
  (or the nearest tested one), read together with their close call in source.
- Patched runs use the published package with the patched file swapped in: the built `dist/` for
  `@ai-sdk/mcp` (built from the pinned commit), and `mcp.py` for Pydantic AI (identical to the file at the pinned commit).

## Environment and cost

Linux 6.18 x86_64, 4 vCPU cloud container, Node 22.23.5, Python 3.12 (frameworks) and 3.13 (runner), Go,
Rust 1.97. No model or paid API calls; marginal cost $0. Wall clock: about 2.5 hours for run 1 at up to 9
targets in parallel, most of it the fixed 10 s settle per trial.

## Not covered

- Only the close path the docs show. Crash paths, cancellation and error-during-connect are not exercised.
- Desktop apps (VS Code, Zed, Cline, Cherry Studio) were not driven; their rows are source reads or SDK cells.
- Windows and macOS were not run. The probe reads `/proc`.

## Run it

```
python3 client-teardown/runner.py --arm -n 10 --out /tmp/ct/arm
python3 client-teardown/runner.py --target js-ai-sdk --target py-pydantic-ai -n 10 --out /tmp/ct/targets
python3 client-teardown/summarize.py /tmp/ct
```

Each target in [`targets.json`](targets.json) names its driver and the environment it ran in. The environments
(one venv per Python framework, one npm prefix per JS pin) are listed in the coverage table.
