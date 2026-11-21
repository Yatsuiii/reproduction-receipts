// Stand-in for a launcher between the client and the server (npx, uvx,
// `python -m`, a shell script): it starts the real server as a child with
// inherited stdio and stays alive until that child exits. Node's default
// SIGTERM handling ends this process without passing the signal on, so a
// client that signals only the pid it spawned leaves the inner server
// running. A client that signals the process group does not.
//
//   node wrapper.mjs <command> <args...>
//
// Whether real launchers forward signals is measured separately
// (launchers.py); this fixture is the non-forwarding case.

import { spawn } from 'node:child_process';

const [, , command, ...args] = process.argv;
const child = spawn(command, args, { stdio: 'inherit' });
child.on('exit', code => process.exit(code ?? 0));
