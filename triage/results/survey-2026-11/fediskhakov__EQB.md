# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/fediskhakov__EQB` at commit `33c68b4f7de035c1a86ee5450146905800a0a966`
- Triaged: 2026-11-21T18:16:39Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.077 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 2 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Python code imports numpy, pandas but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `data/sumstats.ipynb`
- **ABSOLUTE_PATH**: 2 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `autotrade/dktax.m:136`, `autotrade/dktax.m:332`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `autotrade/data.m`, `autotrade/dktax.m`, `autotrade/dpsolver.m`, `autotrade/equilibrium.m`, `autotrade/estim.m`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: results/estimation/estimation_data.mat, results/estimation/mle_step1.mat. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `results/estimation/estimation_data.mat`, `results/estimation/mle_step1.mat`
- **UNRESOLVED_PATHS**: 6 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `autotrade/data.m:242`, `autotrade/data.m:257`, `autotrade/data.m:265`, `autotrade/data.m:268`, `autotrade/data.m:273`, `autotrade/dktax.m:370`
- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("Nielsen") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE`

## What triage looked at

- 141 files, 41,449,093 bytes. Languages: matlab (49), python (1).
- Documentation read: README.md. Licences named: CC BY-NC, GPL.
- Master scripts: run_all.m.
- File reads traced: 17; writes: 25; unresolved paths: 6; missing: none.
- Links found: 14; checked: no.
