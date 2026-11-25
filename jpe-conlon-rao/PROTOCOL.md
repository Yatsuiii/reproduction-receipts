# Protocol, written before any package code ran

Written 2026-11-25 ~17:00 UTC, after reading the README, `run_estimation.sh`, `run_counterfactuals.sh`, `run_slow.sh`,
`cleaning_code/lp2023_config.py` and the input and output paths of each script named below, and before running any of
them. The run is driven by [`spec.json`](spec.json) through [`receiptgen/rerun.py`](../receiptgen/README.md).

Package: [chrisconlon/Liquor_Replication_JPE](https://github.com/chrisconlon/Liquor_Replication_JPE) at commit
`97567b1968f44980a47a7b72c1928a5e01255a67` (19 Mar 2026), the authors' package for Conlon and Rao, *Journal of Political
Economy*, forthcoming. MIT licence. Python only for the steps run here.

Why this one: the top candidate on the [candidate list](../candidates/README.md) whose main results can be recomputed on
free software from data in the repository, in a target journal with a data editor.

## What will run, in order

1. `python3 -m venv venv && venv/bin/pip install -r requirements.txt` (unpinned minimum versions; what resolved is recorded).
2. `1_descriptive_tables.py` (Tables 1 and 2). Table 2 reads the committed `slow_paper_mc.parquet`, so on this step it is
   formatted from a committed file, not recomputed.
3. `12_panel_regressions.py` (Appendix Tables A9 and A10, from public data in `raw_data/`).
4. `estimate_demand_MAIN.py ../estimation_outputs/slow_paper.pickle`, the README's main RCNL specification, exactly as in
   `run_estimation.sh` (no `--starting`; `run_slow.sh` names `starting_values_june.npy`, which is not in the repository, so
   that script is not used). README time: 10+ hours on an M2 laptop (15 hours in `run_estimation.sh`).
5. `post_estimation.py` on that pickle (marginal costs, `slow_paper_mc.parquet`).
6. `4_parameter_tables.py` (Tables 3 and 4) from the pickle of step 4.
7. `3a_compute_counterfactual.py --all`, `3b_collate_cf.py`, `3c_compute_counterfactual_both_tax.py`,
   `6_counterfactual_plots.py` (Tables 6 to 8, Figures 7 and 8). README time for 3a: about 4.5 hours.

Each step runs in the same checkout, one after another, so later steps use this run's pickle and marginal costs, never the
committed ones (except Table 2 in step 2, as noted).

## Comparison rule, fixed now

- Every `.tex` table: every number against the committed file, relative tolerance 1e-12, all other text identical. The
  tables print three decimals, so this is a match at printed precision. Each difference is listed with both values as
  "did not regenerate here, reason unknown".
- `slow_paper_mc.parquet` and `results/all_*.parquet`: byte comparison, then, if the bytes differ, both files printed to
  CSV with 17 significant digits and compared the same way. A nonlinear estimation run on another CPU and library
  versions is not expected to agree to 1e-12 in every cell; such differences are reported with their size, not hidden.
- Figures 7 and 8: hashed, not compared.
- A failed step is reported with its log, and the steps after it still run and are reported as they go.
- The receipt does not say whether the paper is right. It says what the committed materials did on this machine.

## Addendum, 2026-11-25 ~17:30 UTC, after run 1 and before run 2

Run 1 stopped at the main estimation within seconds; what it showed is in [`run1/NOTE.md`](run1/NOTE.md). Run 2
([`spec2.json`](spec2.json)) changes three things and nothing else, each logged as a deviation in its receipt:

1. Install with `pip install --uploaded-prior-to 2026-03-20T00:00:00Z -r requirements.txt`, so versions are those current
   at the package commit date. This is the least arbitrary choice for unpinned requirements.
2. `mkdir -p checks` before the scripts run.
3. The README's stage order (Stage 2 estimation first, then Stage 3 from 3.1), so every table reads this run's estimates.

The comparison rule is unchanged. In addition, `estimation_outputs/*.parquet` and `results/*.parquet` are declared committed
intermediates: an output whose step read one of them before this run regenerated it is not counted as reproduced.
