# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/tholden__RobustRealRateRulesReplication` at commit `41d8bf69e4b47dc71dd15aa2929db6eea131ef41`
- Triaged: 2026-11-21T18:16:35Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.049 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 2 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (websave). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `Main.m:81`, `Main.m:83`
- **SOFTWARE_REQUIRED**: Requires Dynare (free) inside MATLAB or Octave, with no version named; a rerun must choose one and log it.
  Evidence: `SmetsWouters2007/Smets_Wouters_2007_45.mod`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `Main.m`, `MakeRelease.m`, `private/DistributionOfCentralTendency.m`, `private/GCVRidgeRegression.m`, `private/GridFMinBound.m`
- **UNRESOLVED_PATHS**: 3 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `private/ObtainHistoricalData.m:19`, `private/ObtainHistoricalData.m:20`, `private/ObtainHistoricalData.m:21`
- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("proprietary") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: Datafeed Toolbox, Econometrics Toolbox, Machine Learning Toolbox, Optimization Toolbox, Parallel Computing Toolbox. Each is licensed separately; check the desk's MATLAB has them.
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE.md`, `SmetsWouters2007/LICENSE.txt`

## What triage looked at

- 32 files, 3,548,682 bytes. Languages: dynare (1), matlab (11).
- Documentation read: LICENSE.md, README.md. Licences named: CC BY-NC, CC0, BSD, GPL.
- Master scripts: Main.m, MakeRelease.m.
- File reads traced: 7; writes: 18; unresolved paths: 3; missing: none.
- Links found: 36; checked: no.
