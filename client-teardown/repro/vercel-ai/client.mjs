const { createMCPClient } = await import(process.env.AI_SDK_MCP + '/dist/index.js');
const { Experimental_StdioMCPTransport } = await import(process.env.AI_SDK_MCP + '/dist/mcp-stdio/index.js');

const client = await createMCPClient({ transport: new Experimental_StdioMCPTransport({ command: 'node', args: [new URL('./server.mjs', import.meta.url).pathname] }) });
await client.tools();
await client.close(); console.log('closed');

