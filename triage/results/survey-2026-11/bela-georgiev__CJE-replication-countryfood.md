# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/bela-georgiev__CJE-replication-countryfood` at commit `2b6e11b81503067210839f6b6a4493c5614d3af1`
- Triaged: 2026-11-21T18:16:34Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.066 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 2 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **STATA_NETWORK_INSTALL**: Do-files install julia from the network at run time, with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.
  Evidence: `stata data files/ado/plus/b/boottest.ado:134`
- **NO_RUN_ORDER**: 4 scripts, no master script, and the README does not name an order. A rerun must choose one and log it.
  Evidence: `most_tables_figures.do`, `raw data/cleaning.do`, `table5_panelb.do`, `table6.do`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata (version 11, 6, 7, 7.0, 8, 8.0 named in code); the desk says it has it.
  Evidence: `most_tables_figures.do`, `raw data/cleaning.do`, `stata data files/ado/plus/a/artest.ado`, `stata data files/ado/plus/b/boottest.ado`, `stata data files/ado/plus/b/boottest_1.ado`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: PATH\quanty_clean_cat.dta, \PATH\nwtprice_clean.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `PATH\quanty_clean_cat.dta`, `\PATH\nwtprice_clean.dta`
- **UNRESOLVED_PATHS**: 22 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `stata data files/ado/plus/o/outreg2.ado:2610`, `stata data files/ado/plus/o/outreg2.ado:2833`, `stata data files/ado/plus/o/outreg2.ado:2863`, `stata data files/ado/plus/o/outreg2.ado:2887`, `stata data files/ado/plus/o/outreg2.ado:2909`, `stata data files/ado/plus/o/outreg2.ado:2931`, `stata data files/ado/plus/o/outreg2.ado:3669`, `stata data files/ado/plus/o/outreg2.ado:3682`, `stata data files/ado/plus/o/outreg2.ado:3694`, `stata data files/ado/plus/o/outreg2.ado:3702`
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE`

## What triage looked at

- 48 files, 24,366,365 bytes. Languages: stata (10).
- Documentation read: README.md. Licences named: CC BY-NC.
- Master scripts: none.
- File reads traced: 30; writes: 91; unresolved paths: 22; missing: none.
- Links found: 3; checked: no.
