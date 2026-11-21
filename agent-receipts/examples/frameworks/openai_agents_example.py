"""OpenAI Agents SDK worked example. Runner.run drives an Agent whose model is a scripted stand-in (no API call, tracing off):
each turn it asks for the next planned tool call, then says done. The SDK's own tool runtime executes the receipted
FunctionTools, including its default failure handler, which turns the failing lookup into a message for the model.

usage: python agent-receipts/examples/frameworks/openai_agents_example.py [OUT_DIR]   (needs openai-agents)"""
import asyncio
import json
import shutil
import sys
from importlib.metadata import version
from pathlib import Path

from common import ACTOR, FUNCS, PLAN, POLICY, score, write

from agent_receipts import Recorder, Signer
from agent_receipts.adapters.openai_agents import receipted_function_tool
from agents import Agent, RunConfig, Runner, set_tracing_disabled
from agents.items import ModelResponse, ToolCallItem, ToolCallOutputItem
from agents.models.interface import Model
from agents.usage import Usage
from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText


class ScriptedModel(Model):
    """Stands in for an LLM: returns the next planned tool call each turn, then a final message."""

    def __init__(self):
        self.turn = 0

    async def get_response(self, system_instructions, input, model_settings, tools, output_schema, handoffs, tracing,
                           **kw):
        t, self.turn = self.turn, self.turn + 1
        if t < len(PLAN):
            p = PLAN[t]
            out = [ResponseFunctionToolCall(type="function_call", call_id=f"call_{t}", name=p["tool"],
                                            arguments=json.dumps(p["args"]), id=f"fc_{t}", status="completed")]
        else:
            out = [ResponseOutputMessage(id="msg_done", type="message", role="assistant", status="completed",
                                         content=[ResponseOutputText(type="output_text", text="done", annotations=[])])]
        return ModelResponse(output=out, usage=Usage(), response_id=None)

    def stream_response(self, *a, **kw):
        raise NotImplementedError


def main() -> int:
    default = len(sys.argv) < 2
    out = Path(__file__).resolve().parent / "out" / "openai_agents" if default else Path(sys.argv[1])
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    set_tracing_disabled(True)
    signer = Signer.generate()
    rec = Recorder(out / "receipt.jsonl", signer=signer, actor=ACTOR, meta={"framework": "openai-agents"})
    tools = [receipted_function_tool(f, rec, **POLICY[n]) for n, f in FUNCS.items()]
    agent = Agent(name="support", instructions="Handle the refund request.", tools=tools, model=ScriptedModel())
    result = asyncio.run(Runner.run(agent, "Refund A-100 and A-404?", max_turns=10,
                                    run_config=RunConfig(tracing_disabled=True)))
    anchor = rec.close()

    calls = {}
    native = []
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            raw = item.raw_item
            calls[raw.call_id] = raw
        elif isinstance(item, ToolCallOutputItem):
            raw_out = item.raw_item
            cid = raw_out["call_id"] if isinstance(raw_out, dict) else raw_out.call_id
            call = calls[cid]
            native.append({"tool": call.name, "args": json.loads(call.arguments), "output": str(item.output),
                           # the SDK's record has no error flag on a tool output; only the text says so
                           "is_error": bool(isinstance(raw_out, dict) and raw_out.get("status") == "error")})
    finished = result.final_output == "done"
    (out / "public_key.txt").write_text(f"{ACTOR}={signer.public_hex}\n")
    (out / "anchor.txt").write_text(anchor + "\n")
    summary = score("openai_agents", out / "receipt.jsonl", native, signer.public_hex, anchor, finished,
                    {"openai-agents": version("openai-agents"), "openai": version("openai")})
    return write("openai_agents", out, summary, default)


if __name__ == "__main__":
    sys.exit(main())
