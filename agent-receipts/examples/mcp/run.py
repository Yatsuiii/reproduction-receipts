"""Worked example: record an MCP client's tool calls, verify the receipt as a third party, replay it against the same server
and against a changed one, revoke a source, and tamper with it.

No model is in the loop: the agent's plan is a fixed script of tool calls, so the run is free and repeatable. The receipt is
written at the tool-call boundary, which is the same whether a model or a script chose the calls.

usage: python agent-receipts/examples/mcp/run.py [OUT_DIR]     (needs: pip install "mcp>=2,<3")
Writes OUT_DIR (default examples/mcp/out/: receipt, public key, anchor, verify and replay output). With the default OUT_DIR it
also writes results/mcp_example.json."""
import asyncio
import json
import os
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parents[1]
sys.path.insert(0, str(PKG))

from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

from agent_receipts import Recorder, Signer, areplay, verify  # noqa: E402
from agent_receipts.mcp import RecordedSession  # noqa: E402

ACTOR = "support-agent@example.test"
POLICY = {
    "read_note": {"replayable": True, "sources": ["file:policy.txt"]},
    "search_kb": {"replayable": True, "sources": ["kb:support-kb"]},
    "lookup_order": {"replayable": True, "sources": ["db:orders"]},
    "send_reply": {"replayable": False},
}


def params(kb_version="1"):
    return StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")],
                                 env={**os.environ, "KB_VERSION": kb_version})


SERVER_LOG = open(os.devnull, "w")   # the server prints a traceback for the deliberately failing lookup


async def agent(receipt: Path, signer: Signer) -> str:
    async with stdio_client(params(), errlog=SERVER_LOG) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            rec = Recorder(receipt, signer=signer, actor=ACTOR, meta={"task": "customer asks for a refund on A-100 and A-404",
                                                                     "server": "support-kb", "kb_version": "1"})
            rs = RecordedSession(session, rec, POLICY)
            await rs.call_tool("read_note", {"name": "policy.txt"})
            note = rs.last_seq
            await rs.call_tool("search_kb", {"query": "refund window"})
            kb = rs.last_seq
            await rs.call_tool("lookup_order", {"order_id": "A-100"})
            order = rs.last_seq
            await rs.call_tool("lookup_order", {"order_id": "A-404"})        # fails; the failure stays in the receipt
            await rs.call_tool("send_reply", {"to": "customer@example.test",
                                              "body": "A-100 is inside the 30-day window; refund approved. "
                                                      "We could not find A-404."},
                               derived_from=[note, kb, order])
            return rec.close()


async def replay_against(receipt: Path, kb_version: str):
    async with stdio_client(params(kb_version), errlog=SERVER_LOG) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = RecordedSession(session, None, POLICY).replay_tools()
            return await areplay(receipt, tools)


def main() -> int:
    t0 = time.perf_counter()
    default = len(sys.argv) < 2
    out = HERE / "out" if default else Path(sys.argv[1])
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    receipt = out / "receipt.jsonl"
    signer = Signer.generate()             # a fresh key each run; only the public key is written out
    anchor = asyncio.run(agent(receipt, signer))
    (out / "public_key.txt").write_text(f"{ACTOR}={signer.public_hex}\n")
    (out / "anchor.txt").write_text(anchor + "\n")

    trusted = {ACTOR: signer.public_hex}
    rep = verify(receipt, trusted=trusted, anchor=anchor)
    same = asyncio.run(replay_against(receipt, "1"))
    drift = asyncio.run(replay_against(receipt, "2"))
    stale = verify(receipt, trusted=trusted, anchor=anchor, revoked=["kb:support-kb"])

    tampered = out / "tampered.jsonl"
    lines = receipt.read_text().splitlines()
    rec5 = json.loads(lines[5])
    rec5["args"]["body"] = rec5["args"]["body"].replace("refund approved", "refund denied")
    lines[5] = json.dumps(rec5, sort_keys=True, separators=(",", ":"))
    tampered.write_text("\n".join(lines) + "\n")
    tam = verify(tampered, trusted=trusted, anchor=anchor)

    for name, obj in [("verify", rep), ("replay_same_server", same), ("replay_kb_v2", drift),
                      ("verify_revoked_kb", stale), ("verify_tampered", tam)]:
        (out / f"{name}.txt").write_text(str(obj).replace(str(out) + os.sep, "") + "\n")

    summary = {
        "format": "agent-receipts-mcp-example/1",
        "python": sys.version.split()[0],
        "calls": rep.calls,
        "statuses": [json.loads(x).get("status") for x in receipt.read_text().splitlines()[1:-1]],
        "verify": {"ok": rep.ok, "codes": sorted(rep.codes())},
        "replay_same_server": same.by_seq(),
        "replay_kb_v2": drift.by_seq(),
        "revoked_kb_stale_seqs": stale.stale,
        "tampered": {"ok": tam.ok, "codes": sorted(tam.codes())},
        "receipt_bytes": receipt.stat().st_size,
        "wall_seconds": round(time.perf_counter() - t0, 2),
        "cost_usd": 0,
    }
    if default:
        (PKG / "results" / "mcp_example.json").write_text(json.dumps(summary, indent=1) + "\n", newline="\n")
    print(json.dumps(summary, indent=1))
    want_ok = (rep.ok and not tam.ok and summary["statuses"] == ["ok", "ok", "ok", "error", "ok"] and set(same.codes()) <= {"replay_match", "not_replayable"}
               and "replay_mismatch" in drift.codes() and stale.stale)
    return 0 if want_ok else 1


if __name__ == "__main__":
    sys.exit(main())
