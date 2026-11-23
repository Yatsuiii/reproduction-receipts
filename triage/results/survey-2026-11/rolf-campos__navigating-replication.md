# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/rolf-campos__navigating-replication` at commit `e5404a755fb7a30d82a311669bf5ee1451a0a616`
- Triaged: 2026-11-21T18:16:42Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.411 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 3 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **NO_DEPENDENCY_SPEC**: Python code imports IPython, graphviz, matplotlib, numba, numpy, pandas, scipy but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `1_steady_states.ipynb`, `2_ss_graphs.ipynb`, `3_irf_baseline.ipynb`, `4_irf_fiscal_rules.ipynb`, `5_irf_monetary_rules.ipynb`
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `estimation/LP_Estimation.do:5`, `estimation/LP_Estimation.do:7`, `estimation/LP_Estimation.do:8`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `estimation/VAR_Estimation.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `estimation/LP_Estimation.do`
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: VAR Toolbox. Each is licensed separately; check the desk's MATLAB has them.

## What triage looked at

- 74 files, 6,958,362 bytes. Languages: matlab (1), python (61), stata (1).
- Documentation read: README.md, irfs/README.txt.txt, results/README.txt.txt, results_map.md, ss/README.txt.txt. Licences named: MIT.
- Master scripts: none.
- File reads traced: 5; writes: 7; unresolved paths: 0; missing: none.
- Links found: 3; checked: no.
