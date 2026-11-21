"""LangGraph worked example. A StateGraph runs the plan: a scripted agent node emits one tool call per turn (no model), and
langgraph's own ToolNode executes the wrapped tools.

ToolNode's default error handler re-raises a plain ValueError, which stops the graph. That default run is done first and kept
(out/langgraph/default_handler/): the receipt is left unclosed but still records the failed call. The main run sets
handle_tool_errors=True, so the error goes back to the agent as a ToolMessage and the plan finishes.

usage: python agent-receipts/examples/frameworks/langgraph_example.py [OUT_DIR]   (needs langgraph)"""
import json
import shutil
import sys
from importlib.metadata import version
from pathlib import Path

from common import ACTOR, FUNCS, PLAN, POLICY, score, write

from agent_receipts import Recorder, Signer, verify
from agent_receipts.adapters.langgraph import wrap_tools
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool as lc_tool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def main() -> int:
    default = len(sys.argv) < 2
    out = Path(__file__).resolve().parent / "out" / "langgraph" if default else Path(sys.argv[1])
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    signer = Signer.generate()

    def build(rec, handle):
        tools = wrap_tools([lc_tool(f) for f in FUNCS.values()], rec, POLICY)
        g = StateGraph(MessagesState)
        g.add_node("agent", agent)
        g.add_node("tools", ToolNode(tools) if handle is None else ToolNode(tools, handle_tool_errors=handle))
        g.add_edge(START, "agent")
        g.add_conditional_edges("agent", tools_condition)
        g.add_edge("tools", "agent")
        return g.compile()

    def agent(state):
        step = sum(isinstance(m, AIMessage) for m in state["messages"])
        if step < len(PLAN):
            p = PLAN[step]
            return {"messages": [AIMessage(content="", tool_calls=[{"name": p["tool"], "args": p["args"],
                                                                    "id": f"call_{step}"}])]}
        return {"messages": [AIMessage(content="done")]}

    (out / "default_handler").mkdir()
    rec0 = Recorder(out / "default_handler" / "receipt.jsonl", signer=signer, actor=ACTOR,
                    meta={"framework": "langgraph", "tool_node": "default handle_tool_errors"})
    try:
        build(rec0, None).invoke({"messages": [("user", "Refund A-100 and A-404?")]})
        default_outcome = "finished"
    except ValueError as e:
        default_outcome = f"graph raised {type(e).__name__}: {e}"
    rec0._fh.close()                      # the process would normally just die here; the receipt is left unclosed
    rep0 = verify(out / "default_handler" / "receipt.jsonl", trusted={ACTOR: signer.public_hex})
    default_run = {"outcome": default_outcome, "verify_codes": sorted(rep0.codes()),
                   "statuses": [r["status"] for r in map(json.loads, (out / "default_handler" / "receipt.jsonl")
                                                         .read_text().splitlines()) if r["type"] == "call"]}

    rec = Recorder(out / "receipt.jsonl", signer=signer, actor=ACTOR,
                   meta={"framework": "langgraph", "tool_node": "handle_tool_errors=True"})
    final = build(rec, True).invoke({"messages": [("user", "Refund A-100 and A-404?")]})
    anchor = rec.close()

    msgs = final["messages"]
    calls = {tc["id"]: tc for m in msgs if isinstance(m, AIMessage) for tc in m.tool_calls}
    native = [{"tool": m.name, "args": calls[m.tool_call_id]["args"], "output": m.content,
               "is_error": getattr(m, "status", "success") == "error"} for m in msgs if isinstance(m, ToolMessage)]
    finished = isinstance(msgs[-1], AIMessage) and msgs[-1].content == "done"
    (out / "public_key.txt").write_text(f"{ACTOR}={signer.public_hex}\n")
    (out / "anchor.txt").write_text(anchor + "\n")
    summary = score("langgraph", out / "receipt.jsonl", native, signer.public_hex, anchor, finished,
                    {"langgraph": version("langgraph"), "langchain-core": version("langchain-core")})
    summary["default_handler_run"] = default_run
    return write("langgraph", out, summary, default)


if __name__ == "__main__":
    sys.exit(main())
