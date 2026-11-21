import hashlib
import json
import os
import random
import sys
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "anchor_injections"))
from agent_receipts import ed25519, p256, rekor  # noqa: E402


class Ed25519ph(unittest.TestCase):
    def test_rfc8032_vector(self):   # RFC 8032 section 7.3, Ed25519ph "abc"
        sk = bytes.fromhex("833fe62409237b9d62ec77587520911e9a759cec1d19755b7da901b96dca3d42")
        pk = bytes.fromhex("ec172b93ad5e563bf4932c70e1245034c35467ef2efd4d64ebf819683467e2bf")
        sig = bytes.fromhex("98a70222f0b8121aa9d30f813d683f809e462b469c7ff87639499bb94e6dae41"
                            "31f85042463c2a355a2003d062adf5aaa10b8c61e636062aaad11c2a26083406")
        self.assertEqual(ed25519.public_key(sk, pure=True), pk)
        self.assertEqual(ed25519.sign_ph(sk, b"abc"), sig)
        self.assertTrue(ed25519.verify_ph(pk, b"abc", sig))
        self.assertFalse(ed25519.verify_ph(pk, b"abd", sig))
        self.assertFalse(ed25519.verify(pk, b"abc", sig, pure=True))   # not interchangeable with plain Ed25519


class P256(unittest.TestCase):
    def test_roundtrip_and_reject(self):
        d, pem = p256.generate()
        s = p256.sign(d, b"hello")
        self.assertTrue(p256.verify(pem, b"hello", s))
        self.assertFalse(p256.verify(pem, b"hellp", s))
        _, other = p256.generate()
        self.assertFalse(p256.verify(other, b"hello", s))

    def test_matches_cryptography(self):
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import ec
        except ImportError:
            self.skipTest("cryptography not installed")
        k = ec.generate_private_key(ec.SECP256R1())
        pem = k.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
        for i in range(5):
            msg = os.urandom(i * 13)
            self.assertTrue(p256.verify(pem, msg, k.sign(msg, ec.ECDSA(hashes.SHA256()))))
        d, mine = p256.generate()
        pub = serialization.load_pem_public_key(mine)
        pub.verify(p256.sign(d, b"x"), b"x", ec.ECDSA(hashes.SHA256()))   # raises if wrong


class Inclusion(unittest.TestCase):
    def test_every_leaf_of_many_trees(self):
        import fakelog
        rng = random.Random(7)
        for n in list(range(1, 34)) + [rng.randint(34, 300) for _ in range(5)]:
            leaves = [fakelog.leaf_hash(bytes([i % 256, i // 256])) for i in range(n)]
            root = fakelog.mth(leaves)
            for m in range(n):
                self.assertEqual(rekor.inclusion_root(m, n, leaves[m], fakelog.path(m, leaves)), root, (n, m))
            if n > 1:
                self.assertNotEqual(rekor.inclusion_root(0, n, leaves[1], fakelog.path(0, leaves)), root)


class Cli(unittest.TestCase):
    def test_receipt_verify_with_log_anchor(self):
        import subprocess
        import tempfile
        from agent_receipts import Recorder, Signer
        from fakelog import FakeRekor
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            s = Signer.generate()
            rec = Recorder(td / "run.jsonl", signer=s, actor="me")
            rec.call("x", lambda: {"ok": 1}, {})
            rec.close()
            close = json.loads((td / "run.jsonl").read_text().splitlines()[-1])
            log = FakeRekor()
            bundle = log.bundle(log.add(rekor.proposed_entry(close, s), int(close["t"]) + 1))
            (td / "run.jsonl.anchor.json").write_text(json.dumps(bundle))
            (td / "log.pub").write_bytes(log.pub_pem)
            (td / "public_key.txt").write_text(f"me={s.public_hex}\n")
            run = lambda *a: subprocess.run([sys.executable, "-m", "agent_receipts", *a], cwd=ROOT, capture_output=True,
                                            text=True)
            ok = run("verify", str(td / "run.jsonl"), "--log-key", str(td / "log.pub"), "--require-anchor")
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            self.assertEqual(run("verify", str(td / "run.jsonl")).returncode, 2)          # bundle present, no log key
            _, other = p256.generate()
            (td / "other.pub").write_bytes(other)
            bad = run("verify", str(td / "run.jsonl"), "--log-key", str(td / "other.pub"))
            self.assertEqual(bad.returncode, 1)
            self.assertIn("anchor_untrusted_log", bad.stdout)


if __name__ == "__main__":
    unittest.main()
