"""Pydantic AI: do stdio servers pile up when a toolset is built per request?

A web handler often builds its MCPToolset inside the request. Each request here
builds a fresh toolset, enters it, calls `ping`, leaves it, and drops it. After
three requests, count the fixture servers still running (argv tag, /proc).
The fixture is the `clean` server, which exits as soon as its stdin closes.

    <venv>/bin/python pydantic_ai_accumulate.py [-n 10] [--requests 3]

Prints one line per trial and a JSON summary.
"""

import argparse
import asyncio
import gc
import json
import os
import signal
import uuid
from pathlib import Path

SERVER = str(Path(__file__).resolve().parents[2] / "fixtures" / "server.mjs")


def running(tag: str) -> list[int]:
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


async def trial(requests: int) -> int:
    from fastmcp.client.transports import StdioTransport
    from pydantic_ai.mcp import MCPToolset

    tag = "ctacc-" + uuid.uuid4().hex[:10]
    for _ in range(requests):
        toolset = MCPToolset(StdioTransport(command="node", args=[SERVER, "clean", tag, "/tmp"]))
        async with toolset:
            await toolset.client.call_tool("ping", {})
        del toolset
        gc.collect()
    await asyncio.sleep(5)
    left = running(tag)
    for pid in left:
        os.kill(pid, signal.SIGKILL)
    return len(left)


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--requests", type=int, default=3)
    a = ap.parse_args()
    counts = []
    for i in range(a.n):
        c = await trial(a.requests)
        counts.append(c)
        print(f"trial {i + 1}: {a.requests} requests, {c} servers still running 5 s after the last one", flush=True)
    from importlib.metadata import version
    print(json.dumps({"pydantic_ai_slim": version("pydantic-ai-slim"), "fastmcp": version("fastmcp-slim"),
                      "requests": a.requests, "still_running": counts}))


if __name__ == "__main__":
    asyncio.run(main())
    os._exit(0)
