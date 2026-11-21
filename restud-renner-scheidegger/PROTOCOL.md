# Protocol, written before any package code ran

Written 2026-11-21 ~18:00 UTC, after reading the package and before running any of its scripts.

Package: GaussianProcessesForDynamicEcon/DynamicIncentiveProblems at commit 374fe17a6a21bb137c469260a7e1f72f2c6246ed,
the authors' replication package for Renner and Scheidegger, "Machine Learning for Dynamic Incentive Problems",
Review of Economic Studies (2026).

## What will run

1. `1_install.sh` exactly as committed (conda env `rep`, Python 3.9.23, `pip install -r requirements.txt`).
2. `2_replicate_original.sh` exactly as committed. The README says this regenerates every paper figure and table from
   the deposited checkpoints in about 15 minutes, and that it does not run simulations or solvers.
3. `4_validate_BE.sh` with one change: `N_PROCS=16` set to `N_PROCS=4`, because this machine has 4 cores. The README
   allows this ("Adjust N_RESTARTS, N_ITS, and N_PROCS at the top of the script if needed") and says MPI rank count
   changes random draws, so Step 4 numbers are not expected to be bit-identical to the deposit.
4. Not run: Step 3 (about 17 h at 16 processes, so roughly 70 h on 4 cores) and Step 5 (cluster, about 346 h).
   This receipt therefore says nothing about whether the solver reproduces the deposited checkpoints from scratch.

## Comparison rule, fixed now

- Step 2: every number in the generated `.tex` tables is compared with the same cell of the paper's tables in
  `figure_replication/figure_and_table_paper/`, rounded to the precision the paper prints (two significant figures for
  the error tables, two decimals for Table 5). Match = same value at that precision. Anything else is reported as
  "did not reproduce the printed value", with both numbers.
- Figures: generated PDFs are not compared by bytes (PDF metadata differs). They are listed with hashes only, and a
  visual difference is not reported as a numerical disagreement.
- Step 4: same cell comparison, but a difference is reported as expected-by-design (different rank count), not as a
  failure, unless the order of magnitude differs.
- Any edit to package code, any extra install, and any failed command goes in the deviations list, in order.
