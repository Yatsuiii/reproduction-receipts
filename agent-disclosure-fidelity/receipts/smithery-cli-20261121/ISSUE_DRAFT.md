**Title:** uplink: a wrapped stdio server outlives `close()`, and `close()` waits the full 10 s

Hi. I ran a teardown check on the uplink path in `smithery mcp add` without being asked, and wanted to share what it showed. I'm not asking for anything; I'd just like to know whether it's useful.

**What I saw.** `createStdioLocalPeer` in `src/lib/uplink.ts` spawns the local server without `detached` (line 591), and `close()` signals only the direct child: `stdin.end()`, wait 5 s, `kill("SIGTERM")`, wait 5 s, `kill("SIGKILL")` (lines 636 to 660). When the configured command is a wrapper like `npx` or `uvx`, the direct child is the wrapper. The wrapper dies and the MCP server under it keeps running, reparented to pid 1. That surviving process still holds the wrapper's inherited stdout, so the `'close'` event `close()` waits on doesn't fire, and `close()` also sits through both 5 s timeouts.

**How I checked.** Commit `407ac3b` (release 1.2.0, still the default branch today). I drove the exported `serveUplink()` through a mock relay via `SMITHERY_UPLINK_BASE_URL`; the mock only accepts the WebSocket upgrade. The local server was a small wrapper script that spawns a stdio MCP server, standing in for `npx`. Each trial ended with SIGTERM to the process, which `serveUplink()` handles itself (line 193). Leftover processes were found by an environment tag inherited by everything spawned, read from `/proc`.

| 10 trials each | MCP server still running after teardown | `close()` returned after |
|---|---|---|
| `407ac3b` as shipped | 10 of 10 (the server itself, ppid 1) | 10.008 to 10.010 s |
| `407ac3b` + process-group patch | 0 of 10 | 6.04 to 6.99 s |

The patch is mine, not upstream: spawn with `detached: true` on POSIX and signal `-pid` instead of `pid`. It's [here](https://github.com/Yatsuiii/reproduction-receipts/blob/main/agent-disclosure-fidelity/patches/constructed-smithery-cli-process-group-teardown.patch) if it helps.

**Limits.** Linux only. The wrapper is my own stand-in for `npx`, not `npx` itself. Windows isn't tested. I couldn't find a documented teardown guarantee for uplink, so this may be intended. The changelog does mention a `cleanupChildProcess` helper for `uplink`, but it isn't in the current tree. I searched this repo's issues for orphan, zombie, child process, uplink, process group, SIGKILL and close hang, and found nothing on this.

**Environment and cost.** Linux 6.18 x86_64, Intel Xeon 2.10 GHz, 4 vCPU, 15.7 GB. Node v22.23.5, pnpm 10.27.0 (your `packageManager` pin), Python 3.13.18. The 20 trials took 139 s and 71 s of wall clock; the whole check including install was about 10 minutes. No paid services were used.

**To reproduce:**

```
git clone https://github.com/Yatsuiii/reproduction-receipts
cd reproduction-receipts/agent-disclosure-fidelity
git clone https://github.com/arcadeai-labs/smithery-cli suts/smithery-cli && git -C suts/smithery-cli checkout 407ac3b33944a585357379bc213fdf1ee55464d7
git clone https://github.com/modelcontextprotocol/typescript-sdk suts/typescript-sdk && git -C suts/typescript-sdk checkout b65426158ed9f29aea8ef3dc09ca22d7d9d6f970
(cd suts/typescript-sdk && npx pnpm@10.26.1 install --frozen-lockfile --ignore-scripts && npx pnpm@10.26.1 rebuild esbuild && npx pnpm@10.26.1 --filter @modelcontextprotocol/core build && npx pnpm@10.26.1 --filter @modelcontextprotocol/server build)
uv venv && . .venv/bin/activate && uv pip install -e ".[dev]"
pytest tests/test_discovery_smithery_cli.py -v
```

All four tests pass here, including a negative control that has to trip before any result counts. Per-trial numbers are in [trials.json](https://github.com/Yatsuiii/reproduction-receipts/blob/main/agent-disclosure-fidelity/receipts/smithery-cli-20261121/trials.json).

Is this useful?

Raghav
