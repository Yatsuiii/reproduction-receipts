"""Read-only check of the offline anchor verifier against the live public Rekor log. Publishes nothing. Run in CI."""
import json
import os
import sys
import unittest
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent_receipts import rekor  # noqa: E402


@unittest.skipUnless(os.environ.get("REKOR_LIVE"), "set REKOR_LIVE=1 to check formats against the public Rekor log (read only)")
class LiveRekor(unittest.TestCase):
    """Read-only: fetches the log's public key and a recent entry, and checks this package verifies them offline."""
    URL = "https://rekor.sigstore.dev"

    def get(self, path):
        with urllib.request.urlopen(self.URL + path, timeout=30) as r:
            return r.read()

    def test_recent_entries_verify(self):
        pem = self.get("/api/v1/log/publicKey")
        info = json.loads(self.get("/api/v1/log"))
        offset = sum(int(s["treeSize"]) for s in info.get("inactiveShards", []))
        size = int(info["treeSize"])
        for back in (50, 5000):
            (uuid, entry), = json.loads(self.get(f"/api/v1/log/entries?logIndex={offset + size - back}")).items()
            self.assertEqual(rekor.verify_entry(entry, [pem]), [], (offset + size - back, uuid))
            broken = json.loads(json.dumps(entry))
            broken["integratedTime"] += 1
            self.assertIn("anchor_set_invalid", [c for c, _ in rekor.verify_entry(broken, [pem])])


if __name__ == "__main__":
    unittest.main()
