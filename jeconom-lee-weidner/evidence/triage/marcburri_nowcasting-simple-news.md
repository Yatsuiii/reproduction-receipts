# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/marcburri_nowcasting-simple-news` at commit `b50fe9e8330c99fec727e277a2cf016fa918bffb`
- Triaged: 2026-11-23T17:48:01Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.036 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 2 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads dfms, doParallel, dplyr, foreach, forecast, ggplot2, lmtest, lubridate, midasml, midasr, missMDA, quantmod, reshape2, scales, seasonal, stringr, tibble, tidyr, tsbox, tseries, urca, vars, xtable, xts, zoo with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `R/0_AllPackages.R:14`, `R/0_AllPackages.R:15`, `R/0_AllPackages.R:16`, `R/0_AllPackages.R:17`, `R/0_AllPackages.R:18`
- **ABSOLUTE_PATH**: 2 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `R/0_AllPackages.R:615`, `R/0_AllPackages.R:619`

## Notes

- **UNRESOLVED_PATHS**: 1 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `R/3_CollectResults.R:77`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 76 files, 15,333,857 bytes. Languages: r (4).
- Documentation read: README.md. Licences named: none.
- Master scripts: R/0_AllPackages.R.
- File reads traced: 10; writes: 3; unresolved paths: 1; missing: none.
- Links found: 0; checked: no.
