// @modelcontextprotocol/sdk 1.x, resolved from CT_NODE_PATH (one install per
// pinned version). CT_CLOSE picks the app's close call:
//   transport-then-client   Roo Code / Cline McpHub.deleteConnection
//   client                  Client.close() only (Continue, gemini-cli, ...)
import { createRequire } from 'node:module';
import { spec, closed, timed } from './common.mjs';
const req = createRequire(process.env.CT_NODE_PATH + '/');
const { Client } = req('@modelcontextprotocol/sdk/client/index.js');
const { StdioClientTransport } = req('@modelcontextprotocol/sdk/client/stdio.js');
const transport = new StdioClientTransport({ command: spec.command, args: spec.args, stderr: 'ignore' });
const client = new Client({ name: 'ct-driver', version: '0' });
await client.connect(transport);
await client.listTools();
await client.callTool({ name: 'ping', arguments: {} });
const mode = process.env.CT_CLOSE || 'client';
const s = await timed(async () => {
    if (mode === 'transport-then-client') { await transport.close(); await client.close(); }
    else await client.close();
});
await closed({ close_seconds: s, sdk: req('@modelcontextprotocol/sdk/package.json').version });
