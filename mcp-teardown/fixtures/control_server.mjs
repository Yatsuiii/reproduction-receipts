// Control fixture for the MCP teardown batch runner. Not a target.
//
// A minimal stdio MCP server, written without any SDK so the control does not
// depend on a library version. It answers initialize and tools/list, and starts
// one helper child process, the way real servers start a browser, a language
// server or a worker.
//
//   node control_server.mjs leaky   the helper is left running when this
//                                   process is terminated (known-broken arm)
//   node control_server.mjs clean   on stdin EOF or SIGTERM the helper is
//                                   killed before exit (known-fixed arm)
//
// The batch refuses to report anything unless "leaky" FAILs and "clean" PASSes
// under the same shutdown sequence the targets get.

import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';

const mode = process.argv[2];
if (mode !== 'leaky' && mode !== 'clean') {
    throw new Error('usage: node control_server.mjs leaky|clean');
}

const helper = spawn(process.execPath, ['-e', 'setInterval(() => {}, 60000)'], {
    stdio: 'ignore',
});

// Keep the event loop alive so EOF alone does not end the process: real servers
// with an open upstream connection or a timer behave this way.
setInterval(() => {}, 60000);

function shutdown() {
    if (mode === 'clean') {
        try { helper.kill('SIGKILL'); } catch {}
    }
    process.exit(0);
}

if (mode === 'clean') {
    process.on('SIGTERM', shutdown);
}

const send = msg => process.stdout.write(JSON.stringify(msg) + '\n');

const rl = createInterface({ input: process.stdin });
rl.on('line', line => {
    let msg;
    try { msg = JSON.parse(line); } catch { return; }
    if (msg.method === 'initialize') {
        send({ jsonrpc: '2.0', id: msg.id, result: {
            protocolVersion: msg.params?.protocolVersion ?? '2025-06-18',
            capabilities: { tools: {} },
            serverInfo: { name: `teardown-control-${mode}`, version: '1.0.0' },
        } });
    } else if (msg.method === 'tools/list') {
        send({ jsonrpc: '2.0', id: msg.id, result: { tools: [] } });
    } else if (msg.id !== undefined && msg.method) {
        send({ jsonrpc: '2.0', id: msg.id, error: { code: -32601, message: 'method not found' } });
    }
});
// The leaky arm ignores EOF (it keeps running until signalled); the clean arm
// treats EOF as the spec's first shutdown step.
rl.on('close', () => { if (mode === 'clean') shutdown(); });
