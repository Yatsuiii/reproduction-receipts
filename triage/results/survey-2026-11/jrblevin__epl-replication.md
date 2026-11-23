# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/jrblevin__epl-replication` at commit `ab20cf057c991fbaf5759f46f0caeaba33b4d0a8`
- Triaged: 2026-11-21T18:16:42Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.076 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 3 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **NO_DEPENDENCY_SPEC**: Python code imports pandas but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `application/extract.py`
- **ABSOLUTE_PATH**: 22 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `application/main.m:863`, `application/main.m:867`, `application/main.m:869`, `application/main.m:876`, `application/main.m:885`, `application/main.m:889`, `application/main.m:892`, `application/main.m:905`, `application/main.m:913`, `application/main.m:922`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `application/Gfunc.m`, `application/clogit.m`, `application/epldygam.m`, `application/forwardsim.m`, `application/freqprob.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `application/clubstore_county.do`, `application/population_county.do`, `application/population_zip.do`
- **UNRESOLVED_PATHS**: 1 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `application/main.m:125`

## What triage looked at

- 129 files, 23,596,385 bytes. Languages: matlab (37), python (1), stata (3).
- Documentation read: README.md, application/nhgis0012_csv/nhgis0012_ts_geog2010_zcta_codebook.txt. Licences named: none.
- Master scripts: application/main.m, mc-psd2008/main.m, mc-psd2010/main.m.
- File reads traced: 11; writes: 15; unresolved paths: 1; missing: none.
- Links found: 17; checked: no.
