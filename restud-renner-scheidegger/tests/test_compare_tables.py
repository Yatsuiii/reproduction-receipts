"""Failure injections for compare_tables.py: a changed digit, a changed exponent and a missing table must all fail."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "compare_tables.py"
PAPER = r"Criterion 2 & {$1.2\cdot 10^{-6}$} & {$4.1\cdot 10^{-6}$} \\ max & 0.11 & 0.13"


def run(ref_text, cand_text):
    with tempfile.TemporaryDirectory() as d:
        ref, cand = Path(d, "ref"), Path(d, "cand")
        ref.mkdir(); cand.mkdir()
        (ref / "T.tex").write_text(ref_text)
        if cand_text is not None:
            (cand / "T.tex").write_text(cand_text)
        return subprocess.run([sys.executable, str(SCRIPT), str(ref), str(cand)], capture_output=True, text=True).returncode


class T(unittest.TestCase):
    def test_identical_passes(self):
        self.assertEqual(run(PAPER, PAPER), 0)

    def test_other_notation_same_value_passes(self):
        self.assertEqual(run(PAPER, r"Criterion 2 & 1.2e-06 & 4.1e-06 max 0.11 0.13"), 0)

    def test_changed_mantissa_fails(self):
        self.assertEqual(run(PAPER, PAPER.replace("4.1", "4.2")), 1)

    def test_changed_exponent_fails(self):
        self.assertEqual(run(PAPER, PAPER.replace("{-6}$} &", "{-5}$} &", 1)), 1)

    def test_changed_decimal_fails(self):
        self.assertEqual(run(PAPER, PAPER.replace("0.13", "0.14")), 1)

    def test_missing_table_fails(self):
        self.assertEqual(run(PAPER, None), 1)


if __name__ == "__main__":
    unittest.main()
