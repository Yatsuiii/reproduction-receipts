"""OpenAI Agents SDK: build FunctionTools whose calls are recorded.

    search = receipted_function_tool(search_kb, rec, sources=["kb:prod"], replayable=True)
    agent = Agent(name="support", tools=[search, ...])

Wraps the Python function before `function_tool` sees it, so the tool schema is unchanged and the SDK's own failure handler
(which turns an exception into a message for the model) still runs, after the receipt has recorded the exception.
A parameter typed as the SDK's context (RunContextWrapper / ToolContext) is not recorded; name others in `exclude`.
"""
from __future__ import annotations

import inspect

from ..recorder import Recorder
from ..tools import receipted


def _context_params(fn) -> list:
    out = []
    for name, p in inspect.signature(fn).parameters.items():
        ann = p.annotation if isinstance(p.annotation, str) else getattr(p.annotation, "__name__", "")
        if "RunContextWrapper" in str(ann) or "ToolContext" in str(ann):
            out.append(name)
    return out


def receipted_function_tool(fn, recorder: Recorder, *, sources=(), replayable=False, exclude=(), redact_args=False,
                            redact_result=False, **function_tool_kwargs):
    from agents import function_tool
    exclude = list(exclude) + _context_params(fn)
    wrapped = receipted(recorder, name=function_tool_kwargs.get("name_override") or fn.__name__, sources=sources,
                        replayable=replayable, exclude=exclude, redact_args=redact_args,
                        redact_result=redact_result)(fn)
    return function_tool(wrapped, **function_tool_kwargs)
