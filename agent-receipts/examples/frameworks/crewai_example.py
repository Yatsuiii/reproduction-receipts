"""CrewAI worked example. A one-agent Crew runs the plan through CrewAI's own executor and tool runtime. The agent's LLM is a
scripted stand-in (no API call): it answers in CrewAI's text format with the next planned Action, then a Final Answer.
CrewAI's step callback is the framework's own record of each tool call (the baseline).

usage: python agent-receipts/examples/frameworks/crewai_example.py [OUT_DIR]   (needs crewai)"""
import json
import os
import shutil
import sys
from importlib.metadata import version
from pathlib import Path

os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")

from common import ACTOR, FUNCS, PLAN, POLICY, score, write  # noqa: E402

from agent_receipts import Recorder, Signer  # noqa: E402
from agent_receipts.adapters.crewai import wrap_tool  # noqa: E402
from crewai import Agent, Crew, Task  # noqa: E402
from crewai.llms.base_llm import BaseLLM  # noqa: E402
from crewai.tools import tool as crew_tool  # noqa: E402


class ScriptedLLM(BaseLLM):
    """Stands in for an LLM: one planned Action per call, then the final answer."""
    turn: int = 0

    def __init__(self, **kw):
        super().__init__(model="scripted", **kw)

    def call(self, messages, tools=None, callbacks=None, available_functions=None, from_task=None, from_agent=None,
             response_model=None, **kw):
        t = self.turn
        self.turn += 1
        if t < len(PLAN):
            p = PLAN[t]
            return f"Thought: next step\nAction: {p['tool']}\nAction Input: {json.dumps(p['args'])}"
        return "Thought: I now know the final answer\nFinal Answer: done"

    def supports_function_calling(self):
        return False

    def supports_stop_words(self):
        return False

    def get_context_window_size(self):
        return 8192


def main() -> int:
    default = len(sys.argv) < 2
    out = Path(__file__).resolve().parent / "out" / "crewai" if default else Path(sys.argv[1])
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    signer = Signer.generate()
    rec = Recorder(out / "receipt.jsonl", signer=signer, actor=ACTOR, meta={"framework": "crewai"})
    tools = [wrap_tool(crew_tool(n)(f), rec, **POLICY[n]) for n, f in FUNCS.items()]

    steps = []
    agent = Agent(role="support", goal="Handle refund requests", backstory="Support desk.", tools=tools,
                  llm=ScriptedLLM(), max_iter=10, verbose=False, step_callback=steps.append)
    task = Task(description="Refund A-100 and A-404?", expected_output="done", agent=agent)
    result = Crew(agents=[agent], tasks=[task], verbose=False).kickoff()
    anchor = rec.close()

    native = []
    for s in steps:
        if hasattr(s, "tool") and hasattr(s, "tool_input"):
            args = s.tool_input if isinstance(s.tool_input, dict) else json.loads(s.tool_input)
            text = str(getattr(s, "result", ""))
            native.append({"tool": s.tool, "args": args, "output": text,
                           "is_error": bool(getattr(s, "is_error", False))})
    finished = str(result).strip() == "done"
    (out / "public_key.txt").write_text(f"{ACTOR}={signer.public_hex}\n")
    (out / "anchor.txt").write_text(anchor + "\n")
    summary = score("crewai", out / "receipt.jsonl", native, signer.public_hex, anchor, finished,
                    {"crewai": version("crewai")})
    return write("crewai", out, summary, default)


if __name__ == "__main__":
    sys.exit(main())
