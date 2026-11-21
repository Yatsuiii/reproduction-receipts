"""Score triage.py and two cheap baselines on every frozen case in fixtures/EXPECTED.json and write results/fixtures.json.

Baselines, both deliberately cheap:
  always-runnable   says every package is runnable (what you assume when you skip triage)
  readme-and-code   runnable if the package has a README and at least one code file, else blocked (a ten-second look)
A case passes when the verdict matches and every expected code is present; baselines emit no codes, so they are scored on verdict.

usage: python triage/run_fixtures.py [--out triage/results/fixtures.json]"""
import argparse
import contextlib
import http.server
import json
import shutil
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import triage  # noqa: E402

LANG = set(triage.LANGUAGES)


def readme_and_code(pkg: Path) -> str:
    files = [p for p in pkg.rglob("*") if p.is_file()]
    readme = any(p.name.lower().startswith("readme") for p in files)
    code = any(p.suffix.lower() in LANG for p in files)
    return "runnable" if readme and code else "blocked"


@contextlib.contextmanager
def served(status: int):
    """A local HTTP server that answers every HEAD and GET with `status`."""
    class H(http.server.BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(status); self.end_headers()
        do_GET = do_HEAD
        def log_message(self, *a):
            pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{srv.server_port}"
    finally:
        srv.shutdown(); srv.server_close()


def run_case(c: dict) -> tuple[dict, Path]:
    """Triage one EXPECTED case; returns the result and the package path the baselines should look at."""
    pkg = HERE / "fixtures" / c["fixture"]
    out = str(Path(tempfile.mkdtemp()) / "v.json")
    label = f"fixtures/{c['fixture']}"
    if "serve_status" not in c:
        return triage.run([str(pkg), "--json", out, "--label", label, *c["args"]])["result"], pkg
    with served(c["serve_status"]) as base:
        tmp = Path(tempfile.mkdtemp()) / c["fixture"]
        shutil.copytree(pkg, tmp)
        for f in tmp.rglob("*"):
            if f.is_file() and "{{SERVER}}" in f.read_text(encoding="utf-8", errors="replace"):
                f.write_text(f.read_text(encoding="utf-8").replace("{{SERVER}}", base), encoding="utf-8")
        return triage.run([str(tmp), "--json", out, "--label", label, *c["args"]])["result"], pkg


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "results" / "fixtures.json"))
    a = ap.parse_args(argv)
    exp = json.loads((HERE / "fixtures" / "EXPECTED.json").read_text(encoding="utf-8"))
    rows = []
    for c in exp["cases"]:
        res, pkg = run_case(c)
        codes = sorted({f["code"] for f in res["findings"]})
        missing = sorted(set(c["codes"]) - set(codes))
        rb = readme_and_code(pkg)
        rows.append({"fixture": c["fixture"], "args": c["args"], "serve_status": c.get("serve_status"), "expected": c["verdict"], "expected_codes": c["codes"],
                     "triage": {"verdict": res["verdict"], "codes": codes, "missing_codes": missing,
                                "pass": res["verdict"] == c["verdict"] and not missing},
                     "always-runnable": {"verdict": "runnable", "pass": c["verdict"] == "runnable"},
                     "readme-and-code": {"verdict": rb, "pass": rb == c["verdict"]}})
    n = len(rows)
    summary = {k: f"{sum(r[k]['pass'] for r in rows)}/{n}" for k in ("triage", "always-runnable", "readme-and-code")}
    doc = {"format": "triage-fixture-results/1", "triage_sha256": triage.sha256_file(HERE / "triage.py"),
           "expected_sha256": triage.sha256_file(HERE / "fixtures" / "EXPECTED.json"), "summary": summary, "cases": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary))
    for r in rows:
        if not r["triage"]["pass"]:
            print(f"FAIL {r['fixture']} {r['args']} {r['serve_status'] or ''}: expected {r['expected']} {r['expected_codes']}, got {r['triage']['verdict']} {r['triage']['codes']}")
    return doc


if __name__ == "__main__":
    main()
