"""LangGraph / LangChain: wrap existing tools so a ToolNode (or any agent that calls them) writes a receipt.

    tools = wrap_tools([read_note, search_kb], rec, policy={"search_kb": {"sources": ["kb:prod"], "replayable": True}})
    graph.add_node("tools", ToolNode(tools))

Supports tools built from a function (@tool, StructuredTool.from_function), which is what ToolNode is normally given. The
original tool's handle_tool_error is kept, so the graph behaves as before; the receipt still records the exception, because
the recorder sits between the tool's function and that handler.
"""
from __future__ import annotations

from ..recorder import Recorder
from ..tools import receipted


def wrap_tool(tool, recorder: Recorder, **policy):
    from langchain_core.tools import StructuredTool
    func, coro = getattr(tool, "func", None), getattr(tool, "coroutine", None)
    if func is None and coro is None:
        raise TypeError(f"{tool.name}: only function-backed tools are supported in v0 (got {type(tool).__name__})")
    deco = receipted(recorder, name=tool.name, **policy)
    return StructuredTool(
        name=tool.name, description=tool.description, args_schema=tool.args_schema,
        func=deco(func) if func else None, coroutine=deco(coro) if coro else None,
        return_direct=tool.return_direct, response_format=tool.response_format,
        handle_tool_error=tool.handle_tool_error, handle_validation_error=tool.handle_validation_error)


def wrap_tools(tools, recorder: Recorder, policy: dict | None = None):
    policy = policy or {}
    return [wrap_tool(t, recorder, **policy.get(t.name, {})) for t in tools]
