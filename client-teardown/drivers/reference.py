"""Reference clients that arm the runner. Standard library only.

    reference.py none        close stdin, never signal
    reference.py spec-pid    close stdin, wait 2 s, SIGTERM the pid, wait 2 s, SIGKILL the pid
    reference.py spec-group  the same sequence sent to the server's process group

spec-pid is the MCP lifecycle sequence read literally. spec-group is what the
Python SDK's stdio_client does (mcp/os/posix/utilities.py,
terminate_posix_process_tree).
"""

import json
import os
import signal
import subprocess
import sys
import time

mode = sys.argv[1]
spec = json.loads(os.environ["CT_SPEC"])


def rpc(proc, msg):
    proc.stdin.write((json.dumps(msg) + "\n").encode())
    proc.stdin.flush()
    if "id" in msg:
        return json.loads(proc.stdout.readline())


proc = subprocess.Popen([spec["command"], *spec["args"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        start_new_session=(mode == "spec-group"))
rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
           "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "ref", "version": "0"}}})
rpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
rpc(proc, {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ping", "arguments": {}}})

t0 = time.monotonic()
proc.stdin.close()


def send(sig):
    try:
        if mode == "spec-group":
            os.killpg(proc.pid, sig)
        else:
            proc.send_signal(sig)
    except ProcessLookupError:
        pass


def group_alive():
    try:
        os.killpg(proc.pid, 0)
        return True
    except ProcessLookupError:
        return False


if mode != "none":
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        send(signal.SIGTERM)
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            send(signal.SIGKILL)
            proc.wait()
    if mode == "spec-group" and group_alive():
        # the direct child is gone but others in its group may not be
        deadline = time.monotonic() + 2
        while group_alive() and time.monotonic() < deadline:
            time.sleep(0.05)
        if group_alive():
            send(signal.SIGKILL)

print("CLOSED " + json.dumps({"close_seconds": round(time.monotonic() - t0, 2)}), flush=True)
sys.stdin.read()
