"""Does CrewAI run a tool more times than its own record of the run shows?

A one-agent Crew runs one planned tool call through CrewAI's own executor. The
model is a scripted stand-in (no API call, $0): turn 1 asks for the tool, turn 2
gives the final answer. The tool counts its own executions in a list.

Three arms, same plan:

    ok          the tool returns normally                      negative control
    always      the tool raises every time
    transient   the tool raises on its first execution only    (a timeout after the side effect)

For each arm we record:

    executions  how many times the tool function body actually ran (counter inside the tool)
    llm_asks    how many times the model asked for the tool (the script asks once)
    steps       tool steps in CrewAI's step_callback, the record the docs point users to
    started     ToolUsageStartedEvent on CrewAI's event bus
    errors      ToolUsageErrorEvent on the event bus

usage: python check.py [-n 10] [--out results.json]      (needs crewai)
"""

import argparse
import json
import os
import sys
from importlib.metadata import version

os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")

from crewai import Agent, Crew, Task  # noqa: E402
from crewai.events import crewai_event_bus  # noqa: E402
from crewai.events.types.tool_usage_events import ToolUsageErrorEvent, ToolUsageStartedEvent  # noqa: E402
from crewai.llms.base_llm import BaseLLM  # noqa: E402
from crewai.tools import tool as crew_tool  # noqa: E402


class ScriptedLLM(BaseLLM):
    """One Action, then the final answer. Counts how often the tool was asked for."""
    turn: int = 0
    asks: int = 0

    def __init__(self, **kw):
        super().__init__(model="scripted", **kw)

    def call(self, messages, tools=None, callbacks=None, available_functions=None, from_task=None,
             from_agent=None, response_model=None, **kw):
        t = self.turn
        self.turn += 1
        if t == 0:
            self.asks += 1
            return 'Thought: charge the card\nAction: charge_card\nAction Input: {"order": "A-100"}'
        return "Thought: I now know the final answer\nFinal Answer: done"

    def supports_function_calling(self):
        return False

    def supports_stop_words(self):
        return False

    def get_context_window_size(self):
        return 8192


def trial(arm: str) -> dict:
    runs: list[str] = []

    @crew_tool("charge_card")
    def charge_card(order: str) -> str:
        """Charge the customer's card for an order."""
        runs.append(order)
        if arm == "always" or (arm == "transient" and len(runs) == 1):
            raise TimeoutError("payment gateway timed out")
        return f"charged {order}"

    started, errors = [], []
    with crewai_event_bus.scoped_handlers():
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def _s(src, ev):
            started.append(ev.tool_name)

        @crewai_event_bus.on(ToolUsageErrorEvent)
        def _e(src, ev):
            errors.append(ev.tool_name)

        steps = []
        llm = ScriptedLLM()
        agent = Agent(role="billing", goal="Charge orders", backstory="Billing desk.", tools=[charge_card],
                      llm=llm, max_iter=5, verbose=False, step_callback=steps.append)
        task = Task(description="Charge order A-100.", expected_output="done", agent=agent)
        Crew(agents=[agent], tasks=[task], verbose=False).kickoff()
        crewai_event_bus.flush() if hasattr(crewai_event_bus, "flush") else None

    tool_steps = [s for s in steps if hasattr(s, "tool") and hasattr(s, "tool_input")]
    return {
        "arm": arm,
        "executions": len(runs),
        "llm_asks": llm.asks,
        "steps": len(tool_steps),
        "step_results": [str(getattr(s, "result", ""))[:120] for s in tool_steps],
        "started": len(started),
        "errors": len(errors),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--out")
    ap.add_argument("--arm", action="append")
    a = ap.parse_args()
    res = {"crewai": version("crewai"), "python": sys.version.split()[0], "n": a.n, "arms": {}}
    for arm in a.arm or ["ok", "always", "transient"]:
        trials = [trial(arm) for _ in range(a.n)]
        res["arms"][arm] = trials
        keys = ("executions", "llm_asks", "steps", "started", "errors")
        summary = {k: sorted({t[k] for t in trials}) for k in keys}
        print(f"{arm:10} " + "  ".join(f"{k}={v}" for k, v in summary.items()), flush=True)
    if a.out:
        with open(a.out, "w") as f:
            json.dump(res, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
