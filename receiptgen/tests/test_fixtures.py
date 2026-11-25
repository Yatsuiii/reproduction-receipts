import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


class Fixtures(unittest.TestCase):
    def test_all_fixtures_and_text_rules(self):
        r = subprocess.run([sys.executable, str(HERE / "run_fixtures.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_frozen(self):
        r = subprocess.run([sys.executable, str(HERE / "check_frozen.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
