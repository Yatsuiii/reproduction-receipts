import asyncio
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent_receipts import Fenced, Recorder, Signer, areplay, replay, verify  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.path = Path(self.td.name) / "r.jsonl"
        self.signer = Signer.from_seed(b"\x07" * 32)
        self.trusted = {"a": self.signer.public_hex}

    def tearDown(self):
        self.td.cleanup()

    def lines(self):
        return [json.loads(x) for x in self.path.read_text().splitlines()]


class Recording(Base):
    def test_error_is_recorded_and_reraised(self):
        with Recorder(self.path, signer=self.signer, actor="a") as rec:
            with self.assertRaises(ZeroDivisionError):
                rec.call("div", lambda x: 1 / x, {"x": 0})
        r = self.lines()[1]
        self.assertEqual((r["status"], r["result"], r["result_sha256"]), ("error", None, None))
        self.assertIn("ZeroDivisionError", r["error"])
        self.assertTrue(verify(self.path, trusted=self.trusted).ok)

    def test_fence_blocks_and_records(self):
        ran = []
        with Recorder(self.path, signer=self.signer, actor="a") as rec:
            with self.assertRaises(Fenced):
                rec.call("send", lambda: ran.append(1), {}, fence=lambda: {("booking", 7): ("v1", "v2")})
        self.assertEqual(ran, [])
        r = self.lines()[1]
        self.assertEqual(r["status"], "fenced")
        self.assertIn("v1", r["error"])
        self.assertTrue(verify(self.path, trusted=self.trusted).ok)
        self.assertEqual(replay(self.path, {"send": lambda: None}).by_seq(), {"1": "not_replayable"})

    def test_fence_with_stalefence_premises(self):
        sys.path.insert(0, str(ROOT.parent / "stalefence"))
        from stalefence.ledger import Premises
        store = {"doc": 1}
        p = Premises()
        p.observe("doc", store["doc"])
        store["doc"] = 2
        with Recorder(self.path, signer=self.signer, actor="a") as rec:
            with self.assertRaises(Fenced):
                rec.call("write", lambda: None, {}, fence=lambda: p.changed(store.get, ["doc"]))
        self.assertEqual(self.lines()[1]["status"], "fenced")

    def test_redaction_keeps_digests(self):
        with Recorder(self.path, signer=self.signer, actor="a") as rec:
            rec.call("secret", lambda k: {"v": k * 2}, {"k": 21}, redact_args=True, redact_result=True, replayable=True)
        r = self.lines()[1]
        self.assertIsNone(r["args"])
        self.assertIsNone(r["result"])
        self.assertEqual(len(r["args_sha256"]), 64)
        self.assertTrue(verify(self.path, trusted=self.trusted).ok)
        self.assertEqual(replay(self.path, {"secret": lambda k: {"v": k * 2}}).by_seq(), {"1": "not_replayable"})

    def test_derived_from_must_be_earlier(self):
        rec = Recorder(self.path, signer=self.signer, actor="a")
        self.addCleanup(lambda: rec._fh.close())
        with self.assertRaises(ValueError):
            rec.call("x", lambda: 1, {}, derived_from=[1])
        rec.call("x", lambda: 1, {})
        rec.call("y", lambda: 2, {}, derived_from=[rec.last_seq])
        rec.close()
        self.assertEqual(self.lines()[2]["derived_from"], [1])

    def test_refuses_to_append_to_existing_receipt(self):
        Recorder(self.path, signer=self.signer, actor="a").close()
        with self.assertRaises(FileExistsError):
            Recorder(self.path, signer=self.signer, actor="a")

    def test_non_json_result_is_a_type_error(self):
        with Recorder(self.path, signer=self.signer, actor="a") as rec:
            with self.assertRaises(TypeError):
                rec.call("x", lambda: object(), {})
        r = self.lines()[1]
        self.assertEqual(r["status"], "error")           # the tool ran, so the receipt says so
        self.assertIn("unrecordable result", r["error"])

    def test_async(self):
        async def tool(n):
            await asyncio.sleep(0)
            return {"n": n}

        async def go():
            rec = Recorder(self.path, signer=self.signer, actor="a")
            await asyncio.gather(*(rec.acall("t", tool, {"n": i}, replayable=True) for i in range(5)))
            return rec.close()

        anchor = asyncio.run(go())
        rep = verify(self.path, trusted=self.trusted, anchor=anchor)
        self.assertTrue(rep.ok, str(rep))
        self.assertEqual(rep.calls, 5)
        self.assertEqual(asyncio.run(areplay(self.path, {"t": tool})).codes(), {"replay_match"})
        self.assertEqual(replay(self.path, {"t": tool}).codes(), {"replay_mismatch"})   # sync replay refuses async tools

    def test_unknown_actor_is_untrusted(self):
        Recorder(self.path, signer=self.signer, actor="a").close()
        rep = verify(self.path, trusted={})
        self.assertFalse(rep.ok)
        self.assertEqual(rep.codes(), {"untrusted_key"})


class Cli(Base):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "agent_receipts", *args], cwd=ROOT, capture_output=True, text=True)

    def test_keygen_verify(self):
        key = Path(self.td.name) / "k"
        pub = self.run_cli("keygen", str(key)).stdout.strip()
        self.assertEqual(len(pub), 64)
        self.assertEqual(oct(key.stat().st_mode & 0o777), "0o600")
        self.assertEqual(self.run_cli("keygen", str(key)).returncode, 2)
        rec = Recorder(self.path, signer=Signer.from_file(key), actor="me")
        rec.call("x", lambda: {"ok": 1}, {})
        anchor = rec.close()
        ok = self.run_cli("verify", str(self.path), "--trust", f"me={pub}", "--anchor", anchor)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        bad = self.run_cli("verify", str(self.path), "--trust", f"me={'0' * 64}")
        self.assertEqual(bad.returncode, 1)
        self.assertIn("untrusted_key", bad.stdout)


class Injections(unittest.TestCase):
    def test_frozen_unchanged(self):
        r = subprocess.run([sys.executable, str(ROOT / "check_frozen.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_anchor_injections_match_expected(self):
        r = subprocess.run([sys.executable, str(ROOT / "run_anchor_injections.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_injections_match_expected(self):
        r = subprocess.run([sys.executable, str(ROOT / "run_injections.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
