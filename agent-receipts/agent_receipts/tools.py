"""Framework-neutral: decorate a tool function so every call through any framework is recorded.

    @receipted(rec, sources=["kb:prod"], replayable=True)
    def search_kb(query: str) -> dict: ...

The wrapper keeps the function's name, docstring, annotations and signature, so frameworks that build a tool schema from the
function (LangChain/LangGraph @tool, OpenAI Agents SDK @function_tool, CrewAI @tool) see the same tool. It sits inside the
framework's own error handling, so a tool that raises is recorded as `error` even when the framework then turns the
exception into a message for the model.
"""
from __future__ import annotations

import functools
import inspect
from typing import Callable, Iterable

from .recorder import Recorder


def _bound_args(sig: inspect.Signature, exclude, args, kwargs) -> dict:
    b = sig.bind(*args, **kwargs)
    b.apply_defaults()
    out = {}
    for k, v in b.arguments.items():
        if k in exclude:
            continue
        p = sig.parameters[k]
        if p.kind is p.VAR_KEYWORD:
            out.update(v)
        elif p.kind is p.VAR_POSITIONAL:
            out[k] = list(v)
        else:
            out[k] = v
    return out


def receipted(recorder: Recorder, *, name: str | None = None, sources: Iterable[str] = (), replayable: bool = False,
              exclude: Iterable[str] = (), redact_args: bool = False, redact_result: bool = False):
    """exclude: parameter names not to record (for example a framework context object that is not JSON)."""
    exclude = frozenset(exclude)
    sources = list(sources)

    def deco(fn: Callable):
        sig = inspect.signature(fn)
        if any(p.kind in (p.VAR_POSITIONAL, p.POSITIONAL_ONLY) for p in sig.parameters.values()):
            raise TypeError(f"{fn.__name__}: *args and positional-only parameters are not supported; use named parameters")
        tool = name or fn.__name__
        kept = {k: v for k, v in sig.parameters.items() if k in exclude}

        def split(args, kwargs):
            recorded = _bound_args(sig, exclude, args, kwargs)
            b = sig.bind(*args, **kwargs)
            hidden = {k: b.arguments[k] for k in kept if k in b.arguments}
            return recorded, hidden

        if inspect.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def awrapper(*args, **kwargs):
                recorded, hidden = split(args, kwargs)
                return await recorder.acall(tool, lambda **a: fn(**a, **hidden), recorded, sources=sources,
                                            replayable=replayable, redact_args=redact_args, redact_result=redact_result)
            awrapper.__receipted__ = True
            return awrapper

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            recorded, hidden = split(args, kwargs)
            return recorder.call(tool, lambda **a: fn(**a, **hidden), recorded, sources=sources, replayable=replayable,
                                 redact_args=redact_args, redact_result=redact_result)
        wrapper.__receipted__ = True
        return wrapper
    return deco
