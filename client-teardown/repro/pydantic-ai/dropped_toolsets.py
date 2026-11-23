import asyncio, gc, subprocess, sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from pydantic_ai.mcp import MCPToolset, load_mcp_toolsets
S="/home/claude/reproduction-receipts/client-teardown/fixtures/server.mjs"
def args(tag): return [S,"clean",tag,"/tmp"]
def count(tag): return subprocess.run(["pgrep","-fc",tag],capture_output=True,text=True).stdout.strip()
async def main():
    for _ in range(3):
        c=Client(StdioTransport(command="node",args=args("drA")))
        async with c: await c.list_tools()
        del c
    gc.collect(); await asyncio.sleep(2); print("client", count("drA"))
    for _ in range(3):
        t=MCPToolset(StdioTransport(command="node",args=args("drB")))
        async with t: await t.client.list_tools()
        del t
    gc.collect(); await asyncio.sleep(2); print("toolset", count("drB"))
    import json,tempfile,os
    cfg=tempfile.mktemp(suffix=".json"); json.dump({"mcpServers":{"x":{"command":"node","args":args("drC")}}},open(cfg,"w"))
    for _ in range(3):
        ts=load_mcp_toolsets(cfg)
        async with ts[0]: pass
        del ts
    gc.collect(); await asyncio.sleep(2); print("config", count("drC"))
    subprocess.run(["pkill","-9","-f","dr[ABC]"])
asyncio.run(main())
