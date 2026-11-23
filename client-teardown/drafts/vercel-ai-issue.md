<!-- DRAFT for review. Not posted. Target: vercel/ai -->

# `@ai-sdk/mcp` stdio transport: `close()` skips the stdin close and the SIGKILL steps of the stdio shutdown

## Summary

`StdioMCPTransport.close()` (`packages/mcp/src/tool/mcp-stdio/mcp-stdio-transport.ts`) aborts the spawn signal and returns:

```ts
async close(): Promise<void> {
  this.abortController.abort();
  this.process = undefined;
  this.readBuffer.clear();
}
```

Aborting sends SIGTERM to the child once. The server's stdin is never closed first, so every server, including a well-behaved one that would exit cleanly on EOF, is shut down by SIGTERM without a chance to finish its own shutdown path. And nothing follows the SIGTERM up. If the server ignores or delays SIGTERM (a signal handler that waits on work, a stuck event loop), it keeps running after `client.close()` resolves, and the transport has already dropped its handle, so nothing can stop it later. The child's pipes also keep the host's event loop alive, so a script that ends with `await client.close()` never exits.

The MCP lifecycle spec describes the stdio shutdown as: close the server's stdin, wait for it to exit, send SIGTERM if it hasn't, then SIGKILL if it still hasn't. `close()` skips the first step and the last one. The official TypeScript SDK's `StdioClientTransport` has done the full sequence since 1.24.0.

## Reproduction

@ai-sdk/mcp 2.0.102, Node 22.23.5, Linux.

```js
// server.mjs: answers MCP over stdio, ignores stdin EOF and SIGTERM
import { createInterface } from 'node:readline';
setInterval(() => {}, 60_000);
process.on('SIGTERM', () => {});
createInterface({ input: process.stdin }).on('line', line => {
  const msg = JSON.parse(line);
  const reply = r => process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: msg.id, result: r }) + '\n');
  if (msg.method === 'initialize') reply({ protocolVersion: msg.params.protocolVersion, capabilities: { tools: {} }, serverInfo: { name: 'x', version: '1' } });
  else if (msg.method === 'tools/list') reply({ tools: [] });
});
```

```js
import { createMCPClient } from '@ai-sdk/mcp';
import { Experimental_StdioMCPTransport } from '@ai-sdk/mcp/mcp-stdio';

const client = await createMCPClient({ transport: new Experimental_StdioMCPTransport({ command: 'node', args: ['server.mjs'] }) });
await client.tools();
await client.close();
// The script should exit here. It doesn't, and `pgrep -f server.mjs` still finds the server.
```

## Measured

10 trials per cell. "Residue" means the server was still running 10 s after `close()` resolved, with the host process still alive.

| server behaviour | @ai-sdk/mcp 2.0.102 | with the patch below |
|---|---|---|
| exits on stdin EOF: first shutdown event the server sees | **SIGTERM, 10/10** (never sees EOF) | stdin EOF, 10/10 |
| exits on stdin EOF | clean 10/10 | clean 10/10 |
| ignores EOF, exits on SIGTERM | clean 10/10 | clean 10/10 |
| ignores EOF and SIGTERM | **residue 10/10** | clean 10/10 |
| same server, host script with nothing after `close()` | **host still running at 12 s, 10/10** | host exits, 10/10 |

The same harness gives clean 10/10 on the "ignores EOF and SIGTERM" row for `@modelcontextprotocol/sdk` 1.25 to 1.32, `@modelcontextprotocol/client` 2.4, Mastra, LangChain.js, mcp-use and the OpenAI Agents SDK.

I know the docs describe the stdio transport as meant for local development, and point to the official SDK's
`StdioClientTransport` as an alternative. It is still the built-in option
(`@ai-sdk/mcp/mcp-stdio`, with its own reference page), and the local-dev case (a script or dev server that should exit when it
is done) is exactly where the hang shows up.

## Possible fix

Do the spec's sequence in `close()`, with the same 2 s steps the official SDK uses. I have a patch with two unit tests (exit on EOF sends no signal; a server that never exits gets SIGTERM at 2 s and SIGKILL at 4 s). The `mcp-stdio` tests pass with it (22 passed including the two new ones, 3 skipped), and `ultracite check` is clean. Happy to open a PR if that's welcome.

One thing it does not change: if the server is started through a launcher such as `npx`, signalling the launcher's pid does not reach the server (npm 10.9.9 does not pass SIGTERM on, measured 10/10). The official SDK has the same limit. Killing the process group would cover that; I left it out to keep this change small.

Full harness, controls and raw trials: https://github.com/yatsuiii/reproduction-receipts/tree/claude/project-thread-757w48/client-teardown
