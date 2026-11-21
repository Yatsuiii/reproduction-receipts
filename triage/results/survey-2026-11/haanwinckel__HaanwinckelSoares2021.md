# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/haanwinckel__HaanwinckelSoares2021` at commit `297d90a561bf2d6001fefe9cd4f03a20496c2b33`
- Triaged: 2026-11-21T18:16:58Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.08 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 2 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `Stata/census_dataCleaning.do:7`, `Stata/census_dataCleaning.do:8`, `Stata/census_dataCleaning.do:14`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `Matlab/CounterfactualMaker.m`, `Matlab/Model.m`, `Matlab/ModelEstimator.m`, `Matlab/binarySearch.m`, `Matlab/collectResultsEstimation.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `Stata/Sim_spillover_design.do`, `Stata/census_collapse.do`, `Stata/census_dataCleaning.do`, `Stata/census_regressions.do`, `Stata/getMoments.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: ../CleanData/moments_regions.mat, census_collapsed_data.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `../CleanData/moments_regions.mat`, `census_collapsed_data.dta`
- **UNRESOLVED_PATHS**: 12 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Matlab/outputSimulations.m:6`, `Matlab/outputSimulations.m:16`, `Stata/census_collapse.do:13`, `Stata/census_collapse.do:82`, `Stata/census_dataCleaning.do:38`, `Stata/census_dataCleaning.do:185`, `Stata/getMoments.do:5`, `Stata/getMoments.do:7`, `Stata/getMoments.do:11`, `Stata/getMoments.do:13`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.

## What triage looked at

- 775 files, 195,282,258 bytes. Languages: matlab (22), stata (7).
- Documentation read: readme.txt. Licences named: CC BY.
- Master scripts: Matlab/makeCounterfactuals.m, Matlab/makeTablesFromModelStats.m, Stata/runAll.do.
- File reads traced: 28; writes: 15; unresolved paths: 12; missing: none.
- Links found: 8; checked: no.
