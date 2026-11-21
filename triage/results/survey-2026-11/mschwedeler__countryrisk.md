# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/mschwedeler__countryrisk` at commit `17caff81a4ee30e83cf3d70211871aff2c7fbffe`
- Triaged: 2026-11-21T18:16:57Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.136 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 2 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **ABSOLUTE_PATH**: 1 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `analysis/code/python/helpers.py:157`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `analysis/code/stata/figure5.do`, `analysis/code/stata/figure6.do`, `analysis/code/stata/table10.do`, `analysis/code/stata/table3.do`, `analysis/code/stata/table4.do`
- **UNRESOLVED_PATHS**: 94 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `analysis/code/stata/figure5.do:6`, `analysis/code/stata/figure5.do:23`, `analysis/code/stata/figure6.do:7`, `analysis/code/stata/figure6.do:18`, `analysis/code/stata/figure6.do:21`, `analysis/code/stata/table10.do:3`, `analysis/code/stata/table3.do:3`, `analysis/code/stata/table4.do:3`, `analysis/code/stata/table4.do:35`, `analysis/code/stata/table5.do:3`
- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("proprietary") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 43 files, 272,312 bytes. Languages: python (10), stata (27).
- Documentation read: README.md. Licences named: none.
- Master scripts: analysis/make.py, data/make.py.
- File reads traced: 94; writes: 56; unresolved paths: 94; missing: none.
- Links found: 13; checked: no.
