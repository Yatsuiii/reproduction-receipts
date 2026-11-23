# Protocol, written before any package code ran

Written 2026-11-23 ~04:10 UTC, after reading the package and before running any of its scripts.

Package: [INFORMSJoC/2024.0863](https://github.com/INFORMSJoC/2024.0863) at commit `325bb7d99908de5df94c9c709bcf37ccbdbff5ae`
(1 Oct 2026), the journal's own code-and-data archive for Yu, Lai, Tian and Liu, "Solving Markov Decision Processes via
Largest-size Average Estimator", INFORMS Journal on Computing, DOI 10.1287/ijoc.2024.0863 (archive DOI
10.1287/ijoc.2024.0863.cd). 16 tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256).

## What will run

1. A fresh virtual environment from the machine's Python, then `pip install -r requirements.txt` exactly as committed. The
   requirements name `numpy`, `numba` and `tqdm` without versions, and the README names no Python version, so this installs
   whatever is current today. The resolved versions get logged. That is a property of the package, not a deviation.
2. The six commands in the README, in README order, each from the repository root of its own fresh clone, unchanged:
   `scripts/value_estimation/intruder_monitor.py`, `inventory_control.py`, `ttt3x3_value_estimation.py`,
   `ttt4x4_value_estimation.py`, then `scripts/policy_performance/ttt4x4_random.py` and `ttt4x4_softmax.py`.
3. A second machine (GitHub-hosted runner) repeats steps 1 and 2 if the first machine's run time allows it.

## Comparison rule, fixed now

- The README says the CSVs under `results/` contain the numerical results of the computational experiments, and that
  rerunning a script overwrites its CSV. Each regenerated CSV is compared with the committed one (read with `git show HEAD:`),
  row by row and column by column, by `compare_csv.py`, committed with this protocol.
- Each numeric cell is put in one class: **exact** (same text), **float-equal** (same value to 1e-12 relative), **close**
  (within 1e-6 relative), or **differs** (anything else, reported with both numbers). Text cells must match exactly. A missing
  or extra row or column is reported as such.
- This machine cannot reach the journal's website, so the paper's printed tables are not compared. The receipt compares the
  committed results files only and says so.
- The scripts seed every replication. A difference is reported as "the committed materials did not regenerate the committed
  value in this environment, reason unknown", never as an error in the paper.
- Any edit to package code, any extra install, and any failed command goes in the deviations list, in order.

## Addendum, 2026-11-23 ~04:10 UTC, after the first command had run 2 minutes

`intruder_monitor.py` printed per-cell times of 1.5, 6.0, 17.3 and 41.9 s for N = 8 to 14 of its first estimator. The cost
grows roughly as N to the 6th (H = 6), which projects to about 3 hours per estimator and setting, and 24 of those, so about
3 days on this 4-core machine. The README gives no run time. I stopped it (its log is kept) and changed the order: the five
other scripts run first, then `intruder_monitor.py` runs unchanged for as long as this machine allows. It writes its CSV
only at the very end, so if it is stopped first, the cells it printed are compared with the committed CSV at the precision
it prints (6 decimals for mean, bias and stdev, 8 for MSE) by `compare_printed.py`. That script was written after the
first stopped run and checked against its log. A printed-precision match is weaker than a CSV match and is reported as
such. Cells it did not reach are reported as not run.
