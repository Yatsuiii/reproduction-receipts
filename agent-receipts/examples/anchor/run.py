"""Anchor a receipt and check that the anchor catches the key holder rewriting it.

  python agent-receipts/examples/anchor/run.py            # local Rekor stand-in, no network, nothing published
  python agent-receipts/examples/anchor/run.py --live     # the public Rekor log: the entry is public and permanent

Writes OUT (default examples/anchor/out-local/ or out-live/): the receipt, its anchor bundle, the log key used, the
holder's rewrite, and summary.json."""
import copy
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parents[1]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG / "anchor_injections"))

from agent_receipts import Recorder, Signer, record_hash, rekor, seal, verify  # noqa: E402
from agent_receipts.canon import sha256_json  # noqa: E402

ACTOR = "support-agent@example.test"


def main() -> int:
    live = "--live" in sys.argv
    out = HERE / ("out-live" if live else "out-local")
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    t0 = time.perf_counter()
    signer = Signer.generate()
    receipt = out / "receipt.jsonl"
    rec = Recorder(receipt, signer=signer, actor=ACTOR, meta={"demo": "anchor"})
    rec.call("lookup_order", lambda order_id: {"id": order_id, "total": 49.0}, {"order_id": "A-100"})
    rec.call("send_reply", lambda to, body: {"queued": True}, {"to": "c@example.test", "body": "Refund approved."})
    rec.close()

    if live:
        with urllib.request.urlopen(rekor.DEFAULT_LOG + "/api/v1/log/publicKey", timeout=30) as r:
            log_pem = r.read()
        bundle = rekor.upload(receipt, signer)
    else:
        from fakelog import FakeRekor
        log = FakeRekor()
        log_pem = log.pub_pem
        close = json.loads(receipt.read_text().splitlines()[-1])
        bundle = log.bundle(log.add(rekor.proposed_entry(close, signer), int(time.time())))
        rekor.bundle_path(receipt).write_text(json.dumps(bundle, indent=1) + "\n")
    (out / "log.pub").write_bytes(log_pem)
    (out / "public_key.txt").write_text(f"{ACTOR}={signer.public_hex}\n")
    trusted = {ACTOR: signer.public_hex}
    good = verify(receipt, trusted=trusted, anchor_bundle=bundle, log_keys=[log_pem], require_anchor=True)

    rs = [json.loads(x) for x in receipt.read_text().splitlines()]
    rw = copy.deepcopy(rs)
    rw[2]["args"]["body"] = "Refund denied."
    rw[2]["args_sha256"] = sha256_json(rw[2]["args"])
    for i, r in enumerate(rw):
        r["prev"] = None if i == 0 else record_hash(rw[i - 1])
        seal(r, signer)
    rewrite = out / "rewritten.jsonl"
    rewrite.write_text("".join(json.dumps(r) + "\n" for r in rw))
    no_anchor = verify(rewrite, trusted=trusted)
    anchored = verify(rewrite, trusted=trusted, anchor_bundle=bundle, log_keys=[log_pem], require_anchor=True)

    summary = {"format": "agent-receipts-anchor-example/1", "log": rekor.DEFAULT_LOG if live else "local stand-in",
               "logIndex": bundle["entry"]["logIndex"], "uuid": bundle["uuid"],
               "receipt_with_anchor": {"ok": good.ok, "codes": sorted(good.codes())},
               "holder_rewrite_without_anchor": {"ok": no_anchor.ok, "codes": sorted(no_anchor.codes())},
               "holder_rewrite_with_anchor": {"ok": anchored.ok, "codes": sorted(anchored.codes())},
               "wall_seconds": round(time.perf_counter() - t0, 2), "cost_usd": 0}
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))
    return 0 if good.ok and no_anchor.ok and not anchored.ok else 1


if __name__ == "__main__":
    sys.exit(main())
