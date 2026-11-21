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
