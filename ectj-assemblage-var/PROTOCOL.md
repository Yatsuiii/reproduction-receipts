# Protocol, written before any package code ran

Written 2026-11-25 ~17:10 UTC, after reading the README, `run_all.R`, `install_packages.R` and `requirements.csv`, and before
running any of them. The run is driven by [`spec.json`](spec.json) through [`receiptgen/rerun.py`](../receiptgen/README.md).

Package: [timmy-o-toole/Assemblage_VAR](https://github.com/timmy-o-toole/Assemblage_VAR) at commit
`199c5f8c432c9571e601ce68ada49ab3d1819e55` (12 Nov 2026), the authors' repository for Barrette, Goulet Coulombe and
Reinicke, *The Econometrics Journal*, forthcoming. The README points to a Zenodo deposit for exact replication; this
machine cannot reach Zenodo, so this is the GitHub copy.

Why this one: free software only (R), cleaned data in the repository, a README run time of 5 to 10 minutes, and committed
results to compare against. It was the top free-software candidate for a target journal on the
[candidate list](../candidates/README.md).

## What will run

1. `Rscript install_packages.R`, unchanged. It installs missing CRAN packages at current versions and refuses versions
   older than `requirements.csv`. Versions installed are recorded by the spec's environment command.
2. `Rscript run_all.R`, unchanged, in fast mode (the default).
3. Not run: `RUN_CV=TRUE`, `RUN_IRF_BOOTSTRAP=TRUE`, `RUN_BOOTSTRAP_WEIGHTS=TRUE`, `code/00_prepare_data.R`.

R 4.3.3 from Ubuntu 24.04 is used; the README asks for R 4.3 or newer.

## Comparison rule, fixed now

- `results/summary_numbers.txt`: every number against the committed file, relative tolerance 1e-12, all other text
  identical. A difference is listed with both values as "did not regenerate here, reason unknown".
- `results/point_estimates/*.rds` (six files, rewritten by `01_estimate_weights.R`): byte comparison first. If the bytes
  differ, both files are printed with `dput(..., digits17)` and compared the same way as the text file. An `.rds` header
  records the R version that wrote it, so a byte difference alone means nothing.
- Anything else the run changes in tracked files is listed as a deviation. Figures are git-ignored and not compared.
- The receipt does not say whether the paper is right. It says what the committed materials did on this machine.
