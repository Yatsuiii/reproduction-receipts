"""Agent CLI drivers. Standard library only.

    cli.py <name>

Writes the fixture server into the CLI's own config in a throwaway HOME and
working directory, runs the CLI's own "list MCP servers and their status"
command (which starts each server, handshakes and shuts it down) and waits
for the CLI to exit. No model is called. CLOSED is printed once the CLI has
exited, so the scored read is "is the server still running 10 s after the
CLI that started it is gone".

The CLI binaries come from $CT_CLI_BIN (an npm prefix's node_modules/.bin).
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SPEC = json.loads(os.environ["CT_SPEC"])
BIN = Path(os.environ["CT_CLI_BIN"])
name = sys.argv[1]

home = Path(tempfile.mkdtemp(prefix="ct-home-"))
work = Path(tempfile.mkdtemp(prefix="ct-work-"))
stdio = {"command": SPEC["command"], "args": SPEC["args"]}

if name in ("gemini", "qwen"):
    # folder trust off: both CLIs suppress MCP servers in an untrusted folder
    d = home / (".gemini" if name == "gemini" else ".qwen")
    d.mkdir()
    (d / "settings.json").write_text(json.dumps(
        {"security": {"folderTrust": {"enabled": False}}, "mcpServers": {"fx": stdio}}))
    cmd = [str(BIN / name), "mcp", "list"]
elif name in ("opencode", "kilo"):
    (work / f"{name}.json").write_text(json.dumps(
        {"mcp": {"fx": {"type": "local", "command": [SPEC["command"], *SPEC["args"]]}}}))
    cmd = [str(BIN / name), "mcp", "list"]
else:
    raise SystemExit(f"unknown cli {name}")

env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(home / ".config"),
           XDG_DATA_HOME=str(home / ".local/share"), XDG_CACHE_HOME=str(home / ".cache"),
           NO_COLOR="1", CI="1")
env.pop("CT_SPEC", None)
t0 = time.monotonic()
p = subprocess.run(cmd, cwd=work, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
out = (p.stdout + p.stderr)[-400:]
print("CLOSED " + json.dumps({"cli_seconds": round(time.monotonic() - t0, 2), "exit": p.returncode,
                              "connected_line": "Connected" in out or "connected" in out, "out_tail": out}), flush=True)
sys.stdin.read()
