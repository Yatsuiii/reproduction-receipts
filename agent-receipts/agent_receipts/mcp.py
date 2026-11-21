"""MCP adapter: record every tool call an MCP client session makes.

    async with ClientSession(read, write) as session:
        await session.initialize()
        rs = RecordedSession(session, recorder, policy={"search_kb": {"replayable": True, "sources": ["kb:prod"]}})
        result = await rs.call_tool("search_kb", {"query": "refunds"})

Works with any object that has `async call_tool(name, arguments)` returning an MCP CallToolResult (pydantic) or plain JSON,
so it does not import `mcp` itself. A result with isError / is_error set is recorded with status `error` (the failure stays visible) and
then returned to the caller unchanged, as MCP would.
"""
from __future__ import annotations

from typing import Iterable

from .recorder import Recorder, to_json


class MCPToolError(Exception):
    pass


def _is_error(result) -> bool:
    # mcp 1.x exposes isError, mcp 2.x is_error. Checking only one of them recorded failed calls as ok (results/mcp_example.run1.json).
    if isinstance(result, dict):
        return bool(result.get("isError") or result.get("is_error"))
    return bool(getattr(result, "is_error", False) or getattr(result, "isError", False))


def _error_text(result) -> str:
    data = to_json(result)
    parts = [c.get("text", "") for c in data.get("content", []) if isinstance(c, dict)]
    return " ".join(p for p in parts if p) or "isError=true"


class RecordedSession:
    def __init__(self, session, recorder: Recorder, policy: dict | None = None):
        """policy: tool name -> {"replayable": bool, "sources": [...], "redact_args": bool, "redact_result": bool}.
        Tools not in the policy are recorded as not replayable, with no sources."""
        self.session, self.recorder, self.policy = session, recorder, policy or {}

    @property
    def last_seq(self) -> int:
        return self.recorder.last_seq

    async def call_tool(self, name: str, arguments: dict | None = None, *, sources: Iterable[str] = (),
                        derived_from: Iterable[int] = (), fence=None):
        pol = self.policy.get(name, {})
        holder = {}

        async def run(**args):
            res = await self.session.call_tool(name, args)
            holder["res"] = res
            if _is_error(res):
                raise MCPToolError(_error_text(res))
            return res

        try:
            return await self.recorder.acall(
                name, run, arguments or {}, sources=list(pol.get("sources", [])) + list(sources),
                derived_from=derived_from, replayable=pol.get("replayable", False), fence=fence,
                redact_args=pol.get("redact_args", False), redact_result=pol.get("redact_result", False))
        except MCPToolError:
            return holder["res"]

    def replay_tools(self) -> dict:
        """Tool implementations for areplay(): each re-calls this session. Errors come back as MCPToolError, as recorded."""
        def make(name):
            async def fn(**args):
                res = await self.session.call_tool(name, args)
                if _is_error(res):
                    raise MCPToolError(_error_text(res))
                return res
            return fn
        return {name: make(name) for name in self.policy}
