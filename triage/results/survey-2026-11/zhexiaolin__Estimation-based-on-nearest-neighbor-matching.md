# Triage verdict: BLOCKED

- Package: `pkgs/zhexiaolin__Estimation-based-on-nearest-neighbor-matching` at commit `0d0d5539c4b74c667c23bb909d27eebdd495b2c8`
- Triaged: 2026-11-21T18:16:35Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.025 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 5 blockers, 5 deviations, 0 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `result/out.feather` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `produce_tables.R:16`
- **MISSING_INPUT_UNDOCUMENTED**: `result/out_shadish.feather` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `produce_tables_shadish.R:16`
- **MISSING_INPUT_RESTRICTED**: `result/outse.feather` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `produce_tables.R:23`
- **MISSING_INPUT_RESTRICTED**: `result/outse_shadish.feather` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `produce_tables_shadish.R:23`
- **MISSING_INPUT_RESTRICTED**: `data/shadish.txt` is read by the code but is not in the package, and the documentation (README.md) describes it as restricted ("Confidential"). The desk cannot run this without access.
  Evidence: `shadish.R:2`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: numpy; torch; pandas; matplotlib; pyarrow; POT; git+https://github.com/gsbDBI/ds-wgan.git; git+https://github.com/gbaydin/hypergradient-descent.git. A rerun installs whatever is current and must log the versions it got.
  Evidence: `requirements.txt`
- **UNDECLARED_DEPENDENCIES**: Python code imports hypergrad, ot, wgan, which no dependency file names.
  Evidence: `gan_estimation/gan_shadish.py`, `gan_estimation/gan_shadish_baseline.py`
- **UNPINNED_DEPENDENCIES**: R code loads FNN, arrow, dplyr, feather, future, future.apply, optparse, tictoc, xtable with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `check_dependency.R:1`, `check_dependency.R:2`, `check_dependency.R:3`, `check_dependency.R:4`, `check_dependency.R:5`
- **LONG_COMPUTE**: The documentation claims a run time of about 336 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.
- **GPU_REQUIRED**: The package refers to GPUs or CUDA. A CPU rerun may be slower or numerically different and must say so.

## What triage looked at

- 40 files, 88,576,384 bytes. Languages: python (2), r (10), shell (1).
- Documentation read: README.md. Licences named: MIT.
- Master scripts: main.sh.
- File reads traced: 12; writes: 2; unresolved paths: 0; missing: out.feather, out_shadish.feather, outse.feather, outse_shadish.feather, shadish.txt.
- Links found: 4; checked: no.
