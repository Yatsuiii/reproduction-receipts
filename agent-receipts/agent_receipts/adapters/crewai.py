"""CrewAI: wrap an existing BaseTool, or decorate a function, so the crew's tool calls are recorded.

    lookup = wrap_tool(LookupOrderTool(), rec, sources=["db:orders"])
    agent = Agent(role=..., tools=[lookup])

The wrapper subclasses the tool's own class, so its name, description and args_schema are unchanged, and records each call
of `_run` before CrewAI's own error handling turns an exception into text for the model.
"""
from __future__ import annotations

from ..recorder import Recorder


def wrap_tool(tool, recorder: Recorder, *, sources=(), replayable=False, redact_args=False, redact_result=False):
    if callable(getattr(tool, "func", None)):
        # Tools made with crewai's @tool keep the function in `func`, and their run() calls it directly, not _run().
        # Record at the function so every path through CrewAI is covered exactly once.
        from ..tools import receipted
        wrapped = tool.model_copy()
        wrapped.func = receipted(recorder, name=tool.name, sources=sources, replayable=replayable,
                                 redact_args=redact_args, redact_result=redact_result)(tool.func)
        return wrapped
    cls = type(tool)
    original_run = tool._run

    class Receipted(cls):  # type: ignore[misc, valid-type]
        def _run(self, *args, **kwargs):
            if args:
                raise TypeError("receipted CrewAI tools take keyword arguments only")
            return recorder.call(tool.name, original_run, kwargs, sources=list(sources), replayable=replayable,
                                 redact_args=redact_args, redact_result=redact_result)

    Receipted.__name__ = f"Receipted{cls.__name__}"
    fields = {k: getattr(tool, k) for k in type(tool).model_fields if hasattr(tool, k)}
    return Receipted(**fields)
