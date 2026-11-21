"""Run each framework's worked example (into a temp dir) when that framework is installed; skip otherwise.
Also unit-tests the framework-neutral @receipted decorator, which needs nothing installed."""
import asyncio
import importlib.util
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent_receipts import Recorder, Signer, receipted, verify  # noqa: E402

EX = ROOT / "examples" / "frameworks"


class Decorator(unittest.TestCase):
    def test_keeps_signature_and_records(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "r.jsonl"
            s = Signer.generate()
            rec = Recorder(p, signer=s, actor="a")

            @receipted(rec, sources=["kb"], replayable=True, exclude=["ctx"])
            def search(ctx, query: str, k: int = 3) -> dict:
                """Search."""
                return {"q": query, "k": k, "ctx": ctx}

            @receipted(rec)
            async def boom(x: int) -> dict:
                raise RuntimeError("nope")

            self.assertEqual(list(inspect.signature(search).parameters), ["ctx", "query", "k"])
            self.assertEqual(search.__doc__, "Search.")
            self.assertTrue(inspect.iscoroutinefunction(boom))
            self.assertEqual(search("C", "refund"), {"q": "refund", "k": 3, "ctx": "C"})
            with self.assertRaises(RuntimeError):
                asyncio.run(boom(x=1))
            rec.close()
            calls = [json.loads(x) for x in p.read_text().splitlines()][1:-1]
            self.assertEqual(calls[0]["args"], {"query": "refund", "k": 3})       # ctx not recorded
            self.assertEqual(calls[0]["sources"], ["kb"])
            self.assertEqual(calls[1]["status"], "error")
            self.assertTrue(verify(p, trusted={"a": s.public_hex}).ok)

    def test_rejects_var_args(self):
        rec = Recorder(Path(tempfile.mkdtemp()) / "r.jsonl", signer=Signer.generate(), actor="a")
        self.addCleanup(rec.close)
        with self.assertRaises(TypeError):
            receipted(rec)(lambda *a: a)


def _example(name, module):
    @unittest.skipUnless(importlib.util.find_spec(module), f"{module} not installed")
    def test(self):
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run([sys.executable, str(EX / f"{name}_example.py"), td], capture_output=True, text=True,
                               timeout=300, cwd=EX)
            self.assertEqual(r.returncode, 0, r.stdout[-3000:] + r.stderr[-3000:])
    return test


class Examples(unittest.TestCase):
    test_langgraph = _example("langgraph", "langgraph")
    test_openai_agents = _example("openai_agents", "agents")
    test_crewai = _example("crewai", "crewai")


if __name__ == "__main__":
    unittest.main()
