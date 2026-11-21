"""Cost of recording, next to the cheap baseline (a plain JSONL append of the same call). Writes results/overhead.json.
usage: python agent-receipts/bench_overhead.py [N]"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def tool(query):
    return {"query": query, "hits": ["kb/refunds.md", "kb/billing.md"], "score": 0.91}


def one_backend(n):
    from agent_receipts import Recorder, Signer, verify, ed25519
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "plain.jsonl"
        t = time.perf_counter()
        with open(log, "w") as fh:
            for i in range(n):
                args = {"query": f"q{i}"}
                t0 = time.time()
                res = tool(**args)
                fh.write(json.dumps({"tool": "search", "args": args, "result": res, "t_start": t0, "t": time.time()}) + "\n")
                fh.flush()
        plain = (time.perf_counter() - t) / n

        p = Path(td) / "r.jsonl"
        s = Signer.generate()
        t = time.perf_counter()
        rec = Recorder(p, signer=s, actor="bench")
        for i in range(n):
            rec.call("search", tool, {"query": f"q{i}"}, replayable=True)
        rec.close()
        signed = (time.perf_counter() - t) / n
        t = time.perf_counter()
        ok = verify(p, trusted={"bench": s.public_hex}).ok
        ver = (time.perf_counter() - t) / n
        return {"backend": "cryptography" if ed25519.HAVE_CRYPTOGRAPHY else "pure-python", "n": n,
                "plain_log_us_per_call": round(plain * 1e6, 1), "receipt_us_per_call": round(signed * 1e6, 1),
                "verify_us_per_record": round(ver * 1e6, 1), "verified": ok,
                "plain_bytes_per_call": round(log.stat().st_size / n), "receipt_bytes_per_call": round(p.stat().st_size / n)}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    if os.environ.get("_BENCH_CHILD"):
        print(json.dumps(one_backend(n)))
        return 0
    rows = []
    for pure in ("", "1"):
        env = dict(os.environ, _BENCH_CHILD="1", AGENT_RECEIPTS_PURE=pure)
        out = subprocess.run([sys.executable, __file__, str(n)], env=env, capture_output=True, text=True, check=True)
        rows.append(json.loads(out.stdout))
    import platform
    res = {"format": "agent-receipts-overhead/1", "python": sys.version.split()[0], "machine": platform.machine(),
           "cpu_count": os.cpu_count(), "note": "one machine, one run, wall clock; a tool that does real I/O dwarfs these numbers",
           "rows": rows}
    (HERE / "results" / "overhead.json").write_text(json.dumps(res, indent=1) + "\n", newline="\n")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
