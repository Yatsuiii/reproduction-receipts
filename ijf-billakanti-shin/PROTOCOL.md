# Protocol, written before any package code ran

Written 2026-11-26 ~16:40 UTC, after reading the README, `docs/verification.md` and `scripts/run_replication.py`. The run
is driven by [`spec.json`](spec.json) through [`receiptgen/rerun.py`](../receiptgen/README.md) on a GitHub-hosted
`ubuntu-24.04` runner (x86-64), because this container cannot reach FRED or the New York Fed.

Package: [mcmcs/At-Risk-Public](https://github.com/mcmcs/At-Risk-Public) at commit `4ec0c1de156a19cd0fa318dd4a885d253fbb27ed` (13 Nov 2026), for Rahul
Billakanti and Minchul Shin, "At-Risk Transformation for U.S. Recession Prediction", conditionally accepted by the
*International Journal of Forecasting* (per the package README).

## Why this package

Its README says the tested platform is macOS on Apple Silicon and that "Linux and Windows have not been verified". This run
is that check on Linux. Windows is not attempted: the run script calls `.venv/bin/python`, a Unix path.

## What will run, unchanged

1. Setup: install `uv` from PyPI and `poppler-utils` from Ubuntu (versions recorded); `uv sync --locked` in
   `program_v04` (CPython 3.13 fetched by uv); `xlrd==2.0.2` as the README says.
2. `scripts/download_inputs.py` then `scripts/verify_inputs.py`: the 308 public inputs, checked against the package's
   own checksums.
3. `python3 scripts/run_replication.py`: the README's single command. It estimates every model, builds the artifacts and
   runs `scripts/compare_reference.py` over all 50 registered outputs. Its `run_report.json` is printed into the log.

## Comparison rule, fixed now

The package's own rule, not mine: floating-point values within absolute tolerance `5e-12`, exact match for identifiers,
dates, counts and categories, LaTeX tables equal after the fingerprint comment, figures pixel-equal at 144 dpi. The receipt
reports what `compare_reference.py` said for the 50 outputs. A value outside tolerance is reported as "did not regenerate
here within the package's tolerance, reason unknown", with its size. A difference on another CPU and BLAS is not a claim
that anything in the paper is wrong.

If the run passes the 6-hour runner cap, the receipt says so and reports how far it got.

## Addendum, 2026-11-26 ~22:25 UTC, after run 1

Run 1 ([receipt](runs/github-45856264501-linux/RECEIPT.md)) did not finish: the full run was stopped at 5 h 10 min, the limit I
set under the runner's 6-hour cap. By then it had computed every main-paper bundle and generated Tables 1-7 and Figures 1-3,
and was partway through the appendix. The outputs were in the run's temporary checkout and were not kept, so nothing was
compared. The README estimates 2.5 to 4 hours on Apple Silicon; on this 4-core x86 runner the extended model bundle alone
took 6,931 s.

Run 2 ([`spec2.json`](spec2.json)) runs only the README's main-paper command, `program_v04.main.run_main`, which run 1's log
shows takes about 2.8 hours here. The package's comparison script needs all 50 outputs, so for run 2 the seven regenerated
main-table CSVs are copied over the committed reference CSVs and compared with them, number by number, at relative tolerance
1e-12. Anything that differs is reported with its size against the package's own absolute tolerance of 5e-12 as well.
LaTeX tables and figures are not compared. The appendix needs a machine that stays up longer than 6 hours.
