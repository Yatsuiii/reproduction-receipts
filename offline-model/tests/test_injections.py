"""Each case in injections/EXPECTED.json, built in a throwaway git checkout with fake weights and the stub runtime.

Runs the real harness.py and verify.py as subprocesses. Cases that need the network off run inside `unshare -n`
(directly as root, or through passwordless sudo, dropping back to the calling user). They are skipped, loudly, where
neither is available."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
EXPECTED = json.loads((SRC / "injections/EXPECTED.json").read_text(encoding="utf-8"))["cases"]
COPY = ["task", "injections", "FROZEN.json", "harness.py", "verify.py", "tests/stub_runtime.py"]


def netns_prefix():
    if not shutil.which("unshare"):
        return None
    if os.geteuid() == 0:
        r = subprocess.run(["unshare", "-n", "true"], capture_output=True)
        return ["unshare", "-n"] if r.returncode == 0 else None
    if subprocess.run(["sudo", "-n", "unshare", "-n", "true"], capture_output=True).returncode == 0:
        return ["sudo", "-n", "unshare", "-n", "setpriv", f"--reuid={os.getuid()}", f"--regid={os.getgid()}",
                "--clear-groups", "env", f"HOME={os.environ.get('HOME', '/tmp')}"]
    return None


NETNS = netns_prefix()


def has_only_lo() -> bool:
    import socket
    return sorted(n for _, n in socket.if_nameindex()) == ["lo"]


class Checkout:
    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="offline-inj-"))
        self.repo = self.tmp / "repo"
        self.om = self.repo / "offline-model"
        for rel in COPY:
            src, dst = SRC / rel, self.om / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst) if src.is_dir() else shutil.copyfile(src, dst)
        self.weights = self.tmp / "weights"
        self.weights.mkdir()
        (self.weights / "model.safetensors").write_bytes(b"\x00fake weights\x01" * 64)
        (self.weights / "config.json").write_text('{"fake": true}\n')
        import hashlib
        files = {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
                 for p in self.weights.iterdir()}
        (self.om / "MODEL.json").write_text(json.dumps({"repo": "stub/stub", "revision": "0" * 40, "licence": "test",
                                                        "files": files}, indent=1))
        self.git("init", "-q")
        self.git("add", "-A")
        self.commit("fixture")

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                       check=True, capture_output=True)

    def commit(self, msg):
        self.git("commit", "-q", "-m", msg)

    def harness(self, out: str, mode="ok", offline=True, extra=()):
        cmd = [sys.executable, "-I", str(self.om / "harness.py"), "--weights", str(self.weights),
               "--out", str(self.tmp / out), "--runtime", str(self.om / "tests/stub_runtime.py"), *extra]
        if offline:
            cmd = NETNS + ["env", "OFFLINE_STUB_MODE=" + mode] + cmd
        else:
            cmd = ["env", "OFFLINE_STUB_MODE=" + mode] + cmd
        p = subprocess.run(cmd, capture_output=True, text=True)
        rec = json.loads((self.tmp / out / "run.json").read_text()) if (self.tmp / out / "run.json").exists() else None
        return p, rec

    def verify(self, *args):
        p = subprocess.run([sys.executable, "-I", str(self.om / "verify.py"), *args], capture_output=True, text=True)
        return p

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


@unittest.skipIf(NETNS is None, "SKIPPED: no unshare -n available; offline cases cannot be built on this machine")
class Offline(unittest.TestCase):
    def setUp(self):
        self.c = Checkout()

    def tearDown(self):
        self.c.close()

    def ok_run(self, out="a", mode="ok"):
        p, rec = self.c.harness(out, mode)
        self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
        self.assertEqual(rec["status"], "ok")
        return self.c.tmp / out

    def test_clean_run_passes(self):
        d = self.ok_run()
        p = self.c.verify("run", str(d))
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_network_connect_attempt(self):
        p, rec = self.c.harness("a", "connect")
        self.assertEqual(p.returncode, 4, p.stderr)
        self.assertEqual(rec["status"], "failed")
        self.assertIn("203.0.113.7", json.dumps(rec["blocked_network_attempts"]))

    def test_dns_lookup_attempt(self):
        p, rec = self.c.harness("a", "dns")
        self.assertEqual(p.returncode, 4, p.stderr)
        self.assertIn("telemetry.example.com", json.dumps(rec["blocked_network_attempts"]))

    def test_weights_tampered(self):
        w = self.c.weights / "model.safetensors"
        b = bytearray(w.read_bytes()); b[5] ^= 1; w.write_bytes(bytes(b))
        p, rec = self.c.harness("a")
        self.assertEqual(p.returncode, 2)
        self.assertIn("model.safetensors", rec["reason"])
        self.assertEqual(rec["reason"].count("MODEL.json pins"), 1)
        self.assertNotIn("runtime", rec)

    def test_weights_missing(self):
        (self.c.weights / "config.json").unlink()
        p, rec = self.c.harness("a")
        self.assertEqual(p.returncode, 2)
        self.assertIn("config.json", rec["reason"])
        self.assertEqual(rec["blocked_network_attempts"], [])

    def test_weights_extra_file(self):
        (self.c.weights / "sneaky.bin").write_bytes(b"x")
        p, rec = self.c.harness("a")
        self.assertEqual(p.returncode, 2)
        self.assertIn("sneaky.bin", rec["reason"])

    def test_task_tampered(self):
        f = self.c.om / "task/items.jsonl"
        f.write_text(f.read_text().replace('"label": "NO"', '"label": "YES"', 1))
        self.c.git("add", "-A"); self.c.commit("tamper")
        p, rec = self.c.harness("a")
        self.assertEqual(p.returncode, 2)
        self.assertIn("task/items.jsonl", rec["reason"])

    def test_dirty_checkout(self):
        (self.c.om / "verify.py").write_text("# edited\n" + (self.c.om / "verify.py").read_text())
        p, rec = self.c.harness("a")
        self.assertEqual(p.returncode, 5)
        p, rec = self.c.harness("b", extra=["--allow-dirty"])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(rec["checkout"]["dirty"])
        self.assertIn("# edited", rec["checkout"]["diff"])

    def test_predictions_edited(self):
        d = self.ok_run()
        f = d / "predictions.csv"
        lines = f.read_text().splitlines(keepends=True)
        lines[1] = lines[1].replace(",NO\n", ",YES\n") if lines[1].endswith(",NO\n") else lines[1].replace(",YES\n", ",NO\n")
        f.write_text("".join(lines))
        p = self.c.verify("run", str(d))
        self.assertEqual(p.returncode, 1)
        self.assertIn("predictions.csv is", p.stdout)

    def test_accuracy_misreported(self):
        d = self.ok_run()
        rec = json.loads((d / "run.json").read_text())
        rec["result"]["correct"] += 1
        rec["result"]["accuracy"] = round(rec["result"]["correct"] / rec["result"]["items"], 6)
        (d / "run.json").write_text(json.dumps(rec))
        p = self.c.verify("run", str(d))
        self.assertEqual(p.returncode, 1)
        self.assertIn("recomputed", p.stdout)

    def test_label_edited(self):
        d = self.ok_run()
        f = self.c.om / "task/items.jsonl"
        f.write_text(f.read_text().replace('"label": "NO"', '"label": "YES"', 1))
        p = self.c.verify("run", str(d))
        self.assertEqual(p.returncode, 1)
        self.assertIn("task file task/items.jsonl", p.stdout)

    def test_runs_disagree(self):
        a, b = self.ok_run("a"), self.ok_run("b", "flip:p03")
        p = self.c.verify("compare", str(a), str(b))
        self.assertEqual(p.returncode, 1)
        self.assertIn("p03", p.stdout)

    def test_logits_drift_within_tolerance(self):
        a, b = self.ok_run("a"), self.ok_run("b", "drift:1e-5")
        p = self.c.verify("compare", str(a), str(b))
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("logits.csv byte-identical: False", p.stdout)
        self.assertIn("largest margin difference", p.stdout)

    def test_failed_run_hidden(self):
        self.ok_run("a")
        self.c.harness("b", "connect")
        led = self.c.tmp / "RUNS.json"
        led.write_text(json.dumps({"runs": [{"id": "a", "dir": "a", "status": "ok"},
                                            {"id": "b", "dir": "b", "status": "failed"}]}))
        self.assertEqual(self.c.verify("ledger", str(led)).returncode, 0)
        shutil.rmtree(self.c.tmp / "b")
        p = self.c.verify("ledger", str(led))
        self.assertEqual(p.returncode, 1)
        self.assertIn("run.json is gone", p.stdout)


class Online(unittest.TestCase):
    @unittest.skipIf(has_only_lo(), "SKIPPED: this machine has no network interface, so network_present cannot be built")
    def test_network_present(self):
        c = Checkout()
        try:
            p, rec = c.harness("a", offline=False)
            self.assertEqual(p.returncode, 3, p.stderr)
            self.assertIn("interfaces", rec["reason"] + json.dumps(rec["network"]))
            self.assertNotIn("runtime", rec)
        finally:
            c.close()


class Coverage(unittest.TestCase):
    def test_every_injection_has_a_test(self):
        names = {n[5:] for n in dir(Offline) if n.startswith("test_")} | {"network_present"}
        self.assertEqual(sorted(set(EXPECTED) - names), [])


if __name__ == "__main__":
    unittest.main()
