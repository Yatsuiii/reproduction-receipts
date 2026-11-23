# Triage verdict: BLOCKED

- Package: `pkgs/gabrielgggg__DeadlyDebtCrises` at commit `62d163e82276e1bc79d00adba0f075ca8b9766dc`
- Triaged: 2026-11-21T18:16:42Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.144 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 1 blockers, 2 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `\t` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `matlab_tables_figures/loadResultsToMatlab.m:8`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **ABSOLUTE_PATH**: 1 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `data/Main.do:10`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `matlab_tables_figures/loadBinary.m`, `matlab_tables_figures/loadResultsToMatlab.m`, `matlab_tables_figures/modelFit.m`, `matlab_tables_figures/modelFromMatrix.m`, `matlab_tables_figures/modelOutcomes.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `data/Main.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: Output.xls. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `Output.xls`
- **UNRESOLVED_PATHS**: 2 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `matlab_tables_figures/loadResultsToMatlab.m:148`, `matlab_tables_figures/loadResultsToMatlab.m:179`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 122 files, 148,985,557 bytes. Languages: fortran (37), matlab (9), shell (4), stata (1).
- Documentation read: README.md. Licences named: none.
- Master scripts: baseline/Makefile, data/Main.do, debt_suspension/Makefile, fixed_L/Makefile, matlab_tables_figures/replicate_tables_and_figures.m, perfect_financial/Makefile, persistent_recession/Makefile.
- File reads traced: 16; writes: 6; unresolved paths: 2; missing: t.
- Links found: 0; checked: no.
