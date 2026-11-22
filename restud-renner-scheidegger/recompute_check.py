"""Rebuild the paper's Tables 7 and 8 from the files Step 4 recomputed at the *deposited* checkpoints, and compare
them with the same tables built from the committed versions of those files.

Step 4's notebooks 2D_simulation_and_error.ipynb and 4D_simulation_and_error.ipynb re-simulate the deposited
checkpoints with the deposited fixed shock lists (criterion 3) and append a fresh error row to V_func_error_*.txt
(criterion 2). This script reads those recomputed files from a run checkout, and the committed versions with
`git show HEAD:`, and formats both exactly as the paper's notebooks do (one significant decimal).

Usage: python recompute_check.py RUN_CHECKOUT
"""
import subprocess
import sys
from io import StringIO

import numpy as np

CASES = [  # table, row label, data dir, checkpoint, simulation column the notebook uses
    ("Table 7", "Benchmark", "2D/baseline", 5939, 6),
    ("Table 7", "Overreporting", "2D/overreporting", 4379, 6),
    ("Table 8", "Benchmark", "4D/baseline", 3777, 8),
    ("Table 8", "Overreporting", "4D/overreporting", 2999, 8),
]


def cells(err, sim, col):
    d = sim[:, col]
    return [f"{err[-1, 2]:.1e}", f"{err[-1, 3]:.1e}", f"{np.sqrt(np.mean(d ** 2)):.1e}", f"{np.max(d):.1e}"]


def main() -> int:
    run = sys.argv[1]
    base = "figure_replication/Sec_5_overreporting/data"
    bad = 0
    print("| Table | Row | Cell | Committed files | Recomputed | Same |\n|---|---|---|---|---|---|")
    for table, row, sub, it, col in CASES:
        e, s = f"{base}/{sub}/V_func_error_{it}.txt", f"{base}/{sub}/simulation_{it}.txt"
        dep = lambda p: np.atleast_2d(np.loadtxt(StringIO(subprocess.run(
            ["git", "-C", run, "show", f"HEAD:{p}"], capture_output=True, text=True, check=True).stdout)))
        new_e = np.atleast_2d(np.loadtxt(f"{run}/{e}"))
        old_e = dep(e)
        assert new_e.shape[0] == old_e.shape[0] + 1, f"{e}: expected one appended row"
        a = cells(old_e, dep(s), col)
        b = cells(new_e, np.loadtxt(f"{run}/{s}"), col)
        names = ["C2 L2", "C2 Linf", "C3 L2", "C3 Linf"]
        for n, x, y in zip(names, a, b):
            bad += x != y
            print(f"| {table} | {row} | {n} | {x} | {y} | {'yes' if x == y else 'NO'} |")
    print(f"\n{16 - bad}/16 cells the same")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
