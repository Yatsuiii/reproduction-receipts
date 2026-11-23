# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/mdcattaneo_replication-CJN_2026_ET` at commit `a503428b60cdd1eee466d07b04463c366d1956dc`
- Triaged: 2026-11-23T17:48:02Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.033 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 1 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads Rcpp with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `function_logit_boot.R:12`, `function_logit_mse.R:10`, `function_plr_boot.R:1`, `mse_plr.R:3`

## Notes

- **UNRESOLVED_PATHS**: 4 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `make_table_logit.R:43`, `make_table_plr.R:43`, `plot_coverage_logit.R:72`, `plot_coverage_plr.R:72`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 17 files, 94,170 bytes. Languages: c++ (2), r (14).
- Documentation read: README.md. Licences named: none.
- Master scripts: make_table_logit.R, make_table_plr.R.
- File reads traced: 7; writes: 2; unresolved paths: 4; missing: none.
- Links found: 1; checked: no.
