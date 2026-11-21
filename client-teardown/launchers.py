"""Do real launchers pass SIGTERM on to the server they start?

The `wrapped` scenario uses a stand-in launcher that does not. This checks the
two launchers most MCP configs use, npx and uvx/uv run, against a server that
ignores stdin EOF and exits on SIGTERM:

    npx      npx --package <local tarball> <bin>    (npm exec -> sh -c -> node)
    uv       uv run --no-project python <script>

Each trial starts the launcher, waits for the server to start, sends SIGTERM
to the launcher's pid only (what a client that signals "the child process"
does), waits 3 s and checks whether the server is still running.

    python3 client-teardown/launchers.py [-n 10] [--out launchers.json]
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER = HERE / "fixtures" / "server.mjs"

PY_SERVER = '''import os, signal, sys, time
signal.signal(signal.SIGTERM, lambda *a: os._exit(0))
sys.stdin.read()
while True:
    time.sleep(60)
'''


def alive(tag: str) -> list[int]:
    out = []
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                raw = Path(f"/proc/{pid}/cmdline").read_bytes()
                state = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
            except OSError:
                continue
            if tag.encode() in raw and state != "Z":
                out.append(int(pid))
    return out


def npm_package(work: Path) -> Path:
    pkg = work / "pkg"
    pkg.mkdir()
    (pkg / "package.json").write_text(json.dumps(
        {"name": "ct-fixture-server", "version": "1.0.0", "bin": {"ct-fixture-server": "bin.mjs"}}))
    (pkg / "bin.mjs").write_text(f'#!/usr/bin/env node\nimport "{SERVER}";\n')
    (pkg / "bin.mjs").chmod(0o755)
    subprocess.run(["npm", "pack", "-q", str(pkg)], cwd=work, check=True, capture_output=True)
    return work / "ct-fixture-server-1.0.0.tgz"


def trial(launcher: str, work: Path, tarball: Path) -> dict:
    tag = "ctlaunch-" + uuid.uuid4().hex[:10]
    if launcher == "npx":
        cmd = ["npx", "-y", "--package", str(tarball), "ct-fixture-server", "eof-ignore", tag, str(work)]
    else:
        script = work / "srv.py"
        script.write_text(PY_SERVER)
        cmd = ["uv", "run", "--no-project", "python", str(script), tag]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 30
    server = []
    while time.monotonic() < deadline:
        server = [x for x in alive(tag) if x != p.pid]
        if server:
            break
        time.sleep(0.2)
    time.sleep(0.5)
    os.kill(p.pid, signal.SIGTERM)
    try:
        p.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass
    time.sleep(3)
    left = alive(tag)
    for x in left:
        try:
            os.kill(x, signal.SIGKILL)
        except OSError:
            pass
    p.stdin.close()
    return {"launcher": launcher, "server_started": bool(server), "launcher_exited": p.poll() is not None,
            "server_left_running": bool(left)}


def version(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    except OSError:
        return "missing"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--out")
    a = ap.parse_args()
    work = Path(tempfile.mkdtemp(prefix="ct-launch-"))
    tarball = npm_package(work)
    res = {"npm": version(["npm", "--version"]), "uv": version(["uv", "--version"]),
           "node": version(["node", "--version"]), "trials": []}
    for launcher in ("npx", "uv"):
        ts = [trial(launcher, work, tarball) for _ in range(a.n)]
        res["trials"] += ts
        left = sum(t["server_left_running"] for t in ts)
        started = sum(t["server_started"] for t in ts)
        print(f"{launcher:4} started {started}/{a.n}, server still running after SIGTERM to launcher {left}/{a.n}")
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
