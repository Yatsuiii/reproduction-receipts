// Fixture stdio MCP server for the client teardown check. Not a target.
//
// Written without any SDK so no library version is part of the fixture.
// It answers initialize, tools/list (one tool, `ping`) and tools/call, and
// writes a marker line to $MARKER_DIR when it is initialized, so the runner
// can tell "the client never connected" apart from "the client cleaned up".
//
//   node server.mjs <mode> <tag> <marker_dir>
//
// The tag sits in argv on purpose. Several clients pass the server a reduced
// environment, so an environment tag can be dropped; argv cannot be.
//
// Modes, each one step of the MCP stdio shutdown sequence
// (spec, basic/lifecycle, "stdio" shutdown: close stdin, wait, SIGTERM,
// wait, SIGKILL):
//
//   clean        exits when stdin reaches EOF. Every client must leave
//                nothing behind. This is the negative control.
//   eof-ignore   keeps running after EOF, exits on SIGTERM. A client that
//                only closes stdin leaves it running (spec step 2).
//   term-ignore  keeps running after EOF and ignores SIGTERM. A client that
//                never sends SIGKILL leaves it running (spec step 3).
//
// The wrapped shape (a launcher such as npx or uvx between the client and
// the server) is wrapper.mjs around eof-ignore.

import { createInterface } from 'node:readline';
import { appendFileSync } from 'node:fs';
import { join } from 'node:path';

const [, , mode, tag, markerDir] = process.argv;
if (!['clean', 'eof-ignore', 'term-ignore'].includes(mode) || !tag || !markerDir) {
    process.stderr.write('usage: node server.mjs clean|eof-ignore|term-ignore <tag> <marker_dir>\n');
    process.exit(2);
}

const mark = what => {
    try { appendFileSync(join(markerDir, `${tag}.log`), `${what} ${process.pid} ${Date.now()}\n`); } catch {}
};
mark('start');

if (mode !== 'clean') {
    // Keep the event loop alive after EOF, the way a server with an open
    // upstream connection, a watcher or a timer does.
    setInterval(() => {}, 60_000);
}
if (mode === 'term-ignore') {
    process.on('SIGTERM', () => mark('sigterm-ignored'));
} else {
    process.on('SIGTERM', () => { mark('sigterm'); process.exit(0); });
}

const send = msg => process.stdout.write(JSON.stringify(msg) + '\n');

const rl = createInterface({ input: process.stdin });
rl.on('line', line => {
    let msg;
    try { msg = JSON.parse(line); } catch { return; }
    if (msg.method === 'initialize') {
        mark('initialize');
        send({ jsonrpc: '2.0', id: msg.id, result: {
            protocolVersion: msg.params?.protocolVersion ?? '2025-06-18',
            capabilities: { tools: {} },
            serverInfo: { name: `teardown-fixture-${mode}`, version: '1.0.0' },
        } });
    } else if (msg.method === 'tools/list') {
        mark('tools/list');
        send({ jsonrpc: '2.0', id: msg.id, result: { tools: [{
            name: 'ping',
            description: 'Return pong.',
            inputSchema: { type: 'object', properties: {} },
        }] } });
    } else if (msg.method === 'tools/call') {
        mark('tools/call');
        send({ jsonrpc: '2.0', id: msg.id, result: { content: [{ type: 'text', text: 'pong' }], isError: false } });
    } else if (msg.method === 'ping') {
        send({ jsonrpc: '2.0', id: msg.id, result: {} });
    } else if (msg.id !== undefined && msg.method) {
        send({ jsonrpc: '2.0', id: msg.id, error: { code: -32601, message: 'method not found' } });
    }
});
rl.on('close', () => {
    mark('eof');
    if (mode === 'clean') process.exit(0);
});
