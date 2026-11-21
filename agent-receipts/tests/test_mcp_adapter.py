import asyncio
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent_receipts import Recorder, Signer, areplay, verify  # noqa: E402
from agent_receipts.mcp import RecordedSession  # noqa: E402


class FakeSession:
    """Stands in for mcp.ClientSession: async call_tool returning a CallToolResult-shaped dict."""

    def __init__(self, error_key="isError"):
        self.error_key = error_key

    async def call_tool(self, name, arguments):
        if name == "fail":
            return {"content": [{"type": "text", "text": "boom"}], self.error_key: True}
        return {"content": [{"type": "text", "text": json.dumps(arguments)}], self.error_key: False}


class Adapter(unittest.TestCase):
    def go(self, error_key):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "r.jsonl"
            s = Signer.generate()

            async def run():
                rs = RecordedSession(FakeSession(error_key), Recorder(p, signer=s, actor="a"),
                                     {"echo": {"replayable": True, "sources": ["x"]}, "fail": {"replayable": True}})
                ok = await rs.call_tool("echo", {"v": 1})
                bad = await rs.call_tool("fail", {})
                anchor = rs.recorder.close()
                rr = await areplay(p, RecordedSession(FakeSession(error_key), None, rs.policy).replay_tools())
                return ok, bad, anchor, rr

            ok, bad, anchor, rr = asyncio.run(run())
            recs = [json.loads(x) for x in p.read_text().splitlines()]
            self.assertTrue(bad[error_key])                       # caller still gets MCP's own error result
            self.assertEqual([r.get("status") for r in recs[1:3]], ["ok", "error"])
            self.assertIn("boom", recs[2]["error"])
            self.assertEqual(recs[1]["sources"], ["x"])
            self.assertTrue(verify(p, trusted={"a": s.public_hex}, anchor=anchor).ok)
            self.assertEqual(rr.codes(), {"replay_match"})

    def test_mcp1_isError(self):
        self.go("isError")

    def test_mcp2_is_error(self):
        self.go("is_error")

    @unittest.skipUnless(importlib.util.find_spec("mcp"), "mcp not installed")
    def test_worked_example(self):
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run([sys.executable, str(ROOT / "examples" / "mcp" / "run.py"), td], capture_output=True,
                               text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
