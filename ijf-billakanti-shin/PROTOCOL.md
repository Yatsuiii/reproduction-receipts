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
