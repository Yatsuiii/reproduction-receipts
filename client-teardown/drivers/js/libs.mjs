// JS library drivers. Each uses the library's documented public API:
// connect, list tools, call `ping`, close. Resolved from CT_NODE_PATH.
//   node libs.mjs <name>
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { spec, closed, timed } from './common.mjs';

const req = createRequire(process.env.CT_NODE_PATH + '/');
const imp = async name => {
    try { return await import(pathToFileURL(req.resolve(name)).href); }
    catch (e) {
        // ESM-only package: no "require" condition, so resolve its "import" export by hand
        const [scope, pkg, ...rest] = name.startsWith('@') ? name.split('/') : [null, ...name.split('/')];
        const base = join(process.env.CT_NODE_PATH, ...(scope ? [scope, pkg] : [pkg]));
        const exp = JSON.parse(readFileSync(join(base, 'package.json'), 'utf8')).exports;
        const entry = exp[rest.length ? './' + rest.join('/') : '.'];
        const pick = e => typeof e === 'string' ? e : pick(e.node ?? e.import ?? e.default);
        const target = pick(entry);
        return import(pathToFileURL(join(base, target)).href);
    }
};
const { command, args } = spec;

const drivers = {
    // Vercel AI SDK: createMCPClient + its own StdioMCPTransport (packages/mcp/src/tool/mcp-stdio)
    async 'ai-sdk'() {
        const { createMCPClient } = await imp('@ai-sdk/mcp');
        const { Experimental_StdioMCPTransport } = await imp('@ai-sdk/mcp/mcp-stdio');
        const client = await createMCPClient({ transport: new Experimental_StdioMCPTransport({ command, args, stderr: 'ignore' }) });
        const tools = await client.tools();
        await tools.ping.execute({}, { toolCallId: 'x', messages: [] });
        return timed(() => client.close());
    },
    async mastra() {
        const { MCPClient } = await imp('@mastra/mcp');
        const mcp = new MCPClient({ servers: { fx: { command, args } } });
        const tools = await mcp.listTools();
        const t = Object.values(tools)[0];
        await t.execute({}, {});
        return timed(() => mcp.disconnect());
    },
    async 'mcp-use'() {
        const { MCPClient } = await imp('@mcp-use/client');
        const client = MCPClient.fromDict({ mcpServers: { fx: { command, args } } });
        await client.createAllSessions();
        const s = client.getSession('fx');
        await s.connector.callTool('ping', {});
        return timed(() => client.closeAllSessions());
    },
    async 'openai-agents'() {
        const { MCPServerStdio } = await imp('@openai/agents-core');
        const server = new MCPServerStdio({ command, args });
        await server.connect();
        await server.listTools();
        await server.callTool('ping', {});
        return timed(() => server.close());
    },
    async langchain() {
        const { MultiServerMCPClient } = await imp('@langchain/mcp-adapters');
        const client = new MultiServerMCPClient({ mcpServers: { fx: { transport: 'stdio', command, args } } });
        const tools = await client.getTools();
        await tools[0].invoke({});
        return timed(() => client.close());
    },
    // official v2 client package, which several apps import directly
    async 'ts-client-v2'() {
        const { Client } = await imp('@modelcontextprotocol/client');
        const { StdioClientTransport } = await imp('@modelcontextprotocol/client/stdio');
        const transport = new StdioClientTransport({ command, args, stderr: 'ignore' });
        const client = new Client({ name: 'ct-driver', version: '0' });
        await client.connect(transport);
        await client.listTools();
        await client.callTool({ name: 'ping', arguments: {} });
        return timed(() => client.close());
    },
};

const s = await drivers[process.argv[2]]();
await closed({ close_seconds: s });
