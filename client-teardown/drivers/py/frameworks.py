"""Python framework drivers. Run with the framework's own venv:

    <venv>/bin/python frameworks.py <name>

Each driver uses the framework's documented public API to connect to the
stdio server in $CT_SPEC, list tools, call `ping`, and close the session the
way the framework's docs say to. Then it prints CLOSED and stays alive, as a
long-running host would, until the runner closes its stdin.
"""

import asyncio
import json
import os
import sys
import threading
import time

SPEC = json.loads(os.environ["CT_SPEC"])
CMD, ARGS = SPEC["command"], SPEC["args"]


def closed(**extra):
    print("CLOSED " + json.dumps(extra), flush=True)
    sys.stdin.read()
    os._exit(0)


def params():
    from mcp import StdioServerParameters
    return StdioServerParameters(command=CMD, args=ARGS)


# --- the official SDK itself ---------------------------------------------
async def mcp_sdk():
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client
    async with stdio_client(params()) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            await s.list_tools()
            await s.call_tool("ping", {})
            t0 = time.monotonic()
    return t0


# --- LangChain MCP adapters: stateless, each call opens and closes a session
async def langchain():
    from langchain_mcp_adapters.client import MultiServerMCPClient
    client = MultiServerMCPClient({"fx": {"command": CMD, "args": ARGS, "transport": "stdio"}})
    tools = await client.get_tools()
    await tools[0].ainvoke({})
    return time.monotonic()


async def langchain_session():
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain_mcp_adapters.tools import load_mcp_tools
    client = MultiServerMCPClient({"fx": {"command": CMD, "args": ARGS, "transport": "stdio"}})
    async with client.session("fx") as s:
        tools = await load_mcp_tools(s)
        await tools[0].ainvoke({})
        t0 = time.monotonic()
    return t0


# --- CrewAI: crewai-tools MCPServerAdapter (sync, background thread) ------
def crewai_adapter():
    from crewai_tools import MCPServerAdapter
    adapter = MCPServerAdapter(params())
    tools = adapter.tools
    tools[0].run()
    t0 = time.monotonic()
    adapter.stop()
    closed(close_seconds=round(time.monotonic() - t0, 2))


# --- CrewAI native MCP client --------------------------------------------
async def crewai_native():
    from crewai.mcp.client import MCPClient
    from crewai.mcp.transports.stdio import StdioTransport
    client = MCPClient(StdioTransport(command=CMD, args=ARGS))
    await client.connect()
    await client.list_tools()
    await client.call_tool("ping", {})
    t0 = time.monotonic()
    await client.disconnect()
    return t0


# --- LlamaIndex ----------------------------------------------------------
async def llamaindex():
    from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
    client = BasicMCPClient(CMD, args=ARGS)
    tools = await McpToolSpec(client=client).to_tool_list_async()
    await tools[0].acall()
    return time.monotonic()


# --- Agno ----------------------------------------------------------------
async def agno():
    from agno.tools.mcp import MCPTools
    from mcp import StdioServerParameters
    t = MCPTools(server_params=StdioServerParameters(command=CMD, args=ARGS), transport="stdio")
    await t.connect()
    await t.session.call_tool("ping", {})
    t0 = time.monotonic()
    await t.close()
    return t0


# --- OpenAI Agents SDK ---------------------------------------------------
async def openai_agents():
    from agents.mcp import MCPServerStdio
    server = MCPServerStdio(params={"command": CMD, "args": ARGS})
    await server.connect()
    await server.list_tools()
    await server.call_tool("ping", {})
    t0 = time.monotonic()
    await server.cleanup()
    return t0


# --- smolagents ----------------------------------------------------------
def smolagents():
    from smolagents import MCPClient
    client = MCPClient(params(), structured_output=False)
    tools = client.get_tools()
    tools[0]()
    t0 = time.monotonic()
    client.disconnect()
    closed(close_seconds=round(time.monotonic() - t0, 2))


# --- FastMCP client ------------------------------------------------------
async def fastmcp():
    from fastmcp import Client
    from fastmcp.client.transports import StdioTransport
    async with Client(StdioTransport(command=CMD, args=ARGS)) as c:
        await c.list_tools()
        await c.call_tool("ping", {})
        t0 = time.monotonic()
    return t0


# --- Semantic Kernel -----------------------------------------------------
async def semantic_kernel():
    from semantic_kernel.connectors.mcp import MCPStdioPlugin
    p = MCPStdioPlugin(name="fx", command=CMD, args=ARGS)
    await p.connect()
    await p.session.call_tool("ping", {})
    t0 = time.monotonic()
    await p.close()
    return t0


# --- Google ADK ----------------------------------------------------------
async def adk():
    from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
    ts = McpToolset(connection_params=StdioConnectionParams(server_params=params(), timeout=20))
    tools = await ts.get_tools()
    assert tools
    t0 = time.monotonic()
    await ts.close()
    return t0


# --- Pydantic AI ---------------------------------------------------------
async def pydantic_ai():
    # V2 API: MCPToolset on a FastMCP stdio transport (pydantic_ai/mcp.py docstring)
    from fastmcp.client.transports import StdioTransport
    from pydantic_ai.mcp import MCPToolset
    toolset = MCPToolset(StdioTransport(command=CMD, args=ARGS))
    async with toolset:
        await toolset.client.list_tools()
        await toolset.client.call_tool("ping", {})
        t0 = time.monotonic()
    return t0


async def pydantic_ai_nokeepalive():
    # Control for the keep_alive cause: the same as pydantic_ai() with keep_alive=False
    from fastmcp.client.transports import StdioTransport
    from pydantic_ai.mcp import MCPToolset
    toolset = MCPToolset(StdioTransport(command=CMD, args=ARGS, keep_alive=False))
    async with toolset:
        await toolset.client.call_tool("ping", {})
        t0 = time.monotonic()
    return t0


async def pydantic_ai_config():
    # load_mcp_toolsets: the documented config-file path (docs/mcp/client.md)
    import tempfile
    from pydantic_ai.mcp import load_mcp_toolsets
    cfg = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump({"mcpServers": {"fx": {"command": CMD, "args": ARGS}}}, cfg)
    cfg.close()
    (toolset,) = load_mcp_toolsets(cfg.name)
    async with toolset:
        await toolset.wrapped.client.call_tool("ping", {})
        t0 = time.monotonic()
    return t0


async def pydantic_ai_agent():
    # An agent run with no explicit context manager: "the toolset will be opened
    # and closed automatically as needed" (docs/mcp/client.md). FunctionModel is
    # Pydantic AI's own scripted model, so no API is called.
    from fastmcp.client.transports import StdioTransport
    from pydantic_ai import Agent
    from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
    from pydantic_ai.mcp import MCPToolset
    from pydantic_ai.models.function import FunctionModel

    def script(messages, info):
        if len(messages) == 1:
            return ModelResponse(parts=[ToolCallPart(tool_name="ping", args={})])
        return ModelResponse(parts=[TextPart("done")])

    toolset = MCPToolset(StdioTransport(command=CMD, args=ARGS))
    agent = Agent(FunctionModel(script), toolsets=[toolset])
    r = await agent.run("ping it")
    assert r.output == "done"
    return time.monotonic()


# --- CAMEL ---------------------------------------------------------------
async def camel():
    from camel.toolkits import MCPToolkit
    tk = MCPToolkit(config_dict={"mcpServers": {"fx": {"command": CMD, "args": ARGS}}})
    await tk.connect()
    assert tk.get_tools()
    t0 = time.monotonic()
    await tk.disconnect()
    return t0


# --- mcp-use (Python) ----------------------------------------------------
async def mcp_use():
    from mcp_use import MCPClient
    client = MCPClient.from_dict({"mcpServers": {"fx": {"command": CMD, "args": ARGS}}})
    await client.create_all_sessions()
    s = client.get_session("fx")
    await s.call_tool("ping", {})
    t0 = time.monotonic()
    await client.close_all_sessions()
    return t0


# --- AutoGen -------------------------------------------------------------
async def autogen():
    from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
    wb = McpWorkbench(StdioServerParams(command=CMD, args=ARGS))
    await wb.start()
    await wb.list_tools()
    await wb.call_tool("ping", {})
    t0 = time.monotonic()
    await wb.stop()
    return t0


SYNC = {"crewai-adapter": crewai_adapter, "smolagents": smolagents}
ASYNC = {
    "mcp-sdk": mcp_sdk, "langchain": langchain, "langchain-session": langchain_session,
    "crewai-native": crewai_native, "llamaindex": llamaindex, "agno": agno,
    "openai-agents": openai_agents, "fastmcp": fastmcp, "semantic-kernel": semantic_kernel,
    "adk": adk, "pydantic-ai": pydantic_ai, "pydantic-ai-config": pydantic_ai_config,
    "pydantic-ai-agent": pydantic_ai_agent, "pydantic-ai-nokeepalive": pydantic_ai_nokeepalive, "camel": camel, "mcp-use": mcp_use, "autogen": autogen,
}

if __name__ == "__main__":
    name = sys.argv[1]
    if name in SYNC:
        SYNC[name]()
    else:
        # Keep the event loop running after close, as a host does: a client that
        # leans on loop shutdown to clean up does not get that for free here.
        async def main():
            t0 = await ASYNC[name]()
            print("CLOSED " + json.dumps({"close_seconds": round(time.monotonic() - t0, 2)}), flush=True)
            await asyncio.get_running_loop().run_in_executor(None, sys.stdin.read)
        asyncio.run(main())
        os._exit(0)
