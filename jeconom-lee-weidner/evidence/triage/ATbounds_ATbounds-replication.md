# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/ATbounds_ATbounds-replication` at commit `67c2c4d403d3dfbbfa4cfb25f72fe88d7d0f00da`
- Triaged: 2026-11-23T17:48:00Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.02 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 9 deviations, 1 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads ATbounds, FNN, ggplot2, lmtest, sandwich, xtable with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `Examples/NSW_main_text.R:24`, `Examples/NSW_main_text.R:25`, `Examples/Table2_RHC.R:18`, `Examples/Table2_RHC.R:19`, `Examples/Table2_RHC.R:20`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/nsw_treated.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/NSW_main_text.R:67`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/nsw_control.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/NSW_main_text.R:71`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/nswre74_treated.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/NSW_main_text.R:85`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/nswre74_control.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/NSW_main_text.R:89`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/nswre74_treated.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/Table3_NSW.R:118`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/nswre74_control.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/Table3_NSW.R:122`
- **RUNTIME_DOWNLOAD**: Code downloads http://users.nber.org/~rdehejia/data/psid2_controls.txt at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `Examples/Table3_NSW.R:147`
- **ABSOLUTE_PATH**: 14 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `Examples/Table2_RHC.R:148`, `Examples/Table2_RHC.R:149`, `Examples/Table2_RHC.R:151`, `Examples/Table2_RHC.R:173`, `Examples/Table3_NSW.R:74`, `Examples/Table3_NSW.R:75`, `Examples/Table3_NSW.R:77`, `Examples/Table3_NSW.R:92`, `MC/AppendixTable_MonteCarloInference.R:174`, `MC/AppendixTable_MonteCarloInference.R:177`

## Notes

- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE`

## What triage looked at

- 15 files, 78,799 bytes. Languages: r (6).
- Documentation read: README.md. Licences named: CC BY-NC, GPL.
- Master scripts: none.
- File reads traced: 7; writes: 5; unresolved paths: 0; missing: none.
- Links found: 7; checked: no.
