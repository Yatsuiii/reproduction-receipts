"""Runs every frozen failure injection in fixtures/EXPECTED.json, plus loader and link-check cases. Stdlib unittest only:
python -m unittest discover -s triage/tests"""
import http.server
import json
import shutil
import sys
import tempfile
import threading
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import check_frozen  # noqa: E402
import run_fixtures  # noqa: E402
import triage  # noqa: E402

EXPECTED = json.loads((HERE / "fixtures" / "EXPECTED.json").read_text(encoding="utf-8"))


def verdict(path, args=()):
    return triage.run([str(path), "--json", str(Path(tempfile.mkdtemp()) / "v.json"), *args])["result"]


class FrozenInjections(unittest.TestCase):
    def test_registry_matches(self):
        self.assertEqual(check_frozen.main([]), 0)

    def test_expected_cases(self):
        for case in EXPECTED["cases"]:
            with self.subTest(fixture=case["fixture"], args=case["args"], status=case.get("serve_status")):
                res, _ = run_fixtures.run_case(case)
                codes = {f["code"] for f in res["findings"]}
                self.assertEqual(res["verdict"], case["verdict"], [(f["code"], f["severity"]) for f in res["findings"]])
                self.assertTrue(set(case["codes"]) <= codes, f"missing {set(case['codes']) - codes}; got {codes}")


class Loading(unittest.TestCase):
    def test_zip_with_wrapper_folder(self):
        d = Path(tempfile.mkdtemp())
        z = d / "pkg.zip"
        with zipfile.ZipFile(z, "w") as zf:
            for f in (HERE / "fixtures" / "clean_python").rglob("*"):
                if f.is_file():
                    zf.write(f, "pkg/" + f.relative_to(HERE / "fixtures" / "clean_python").as_posix())
        doc = triage.run([str(z), "--json", str(d / "v.json")])
        self.assertEqual(doc["source"]["kind"], "zip")
        self.assertEqual(doc["result"]["verdict"], "runnable")

    def test_zip_slip_refused(self):
        d = Path(tempfile.mkdtemp())
        z = d / "evil.zip"
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr("../escape.txt", "x")
        with self.assertRaises(ValueError):
            triage.run([str(z), "--json", str(d / "v.json")])


class Links(unittest.TestCase):
    def test_http_404_blocks_documented_download(self):
        class H(http.server.BaseHTTPRequestHandler):
            def do_HEAD(self):
                self.send_response(404); self.end_headers()
            do_GET = do_HEAD
            def log_message(self, *a):
                pass
        srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            d = Path(tempfile.mkdtemp()) / "pkg"
            shutil.copytree(HERE / "fixtures" / "external_download", d)
            readme = d / "README.md"
            readme.write_text(readme.read_text().replace("http://127.0.0.1:9", f"http://127.0.0.1:{srv.server_port}"))
            res = verdict(d, ["--check-links"])
            dead = [f for f in res["findings"] if f["code"] == "DEAD_DATA_LINK"]
            self.assertEqual(res["verdict"], "blocked")
            self.assertIn("404", dead[0]["message"])
        finally:
            srv.shutdown(); srv.server_close()


if __name__ == "__main__":
    unittest.main()
