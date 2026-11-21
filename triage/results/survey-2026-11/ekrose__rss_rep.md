# Triage verdict: BLOCKED

- Package: `pkgs/ekrose__rss_rep` at commit `fa5cc286e09c6e744e09d07e93b66590edfbcea3`
- Triaged: 2026-11-21T18:16:36Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.329 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 5 blockers, 1 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `/scratch/public/ncrime/analysis_11_01_2021.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `code/fake_data_formats.py:18`
- **MISSING_INPUT_RESTRICTED**: `aoc_data/offense_newonly_2020-09-08.pkl` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `build code/build_final.py:783`
- **MISSING_INPUT_RESTRICTED**: `data/schoolExit.pkl.gz` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `build code/build_final.py:982`
- **MISSING_INPUT_RESTRICTED**: `temp/teach_mean_resids_covmale.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `code/teacher_chars.do:98`
- **MISSING_INPUT_RESTRICTED**: `temp/teach_mean_resids_covwhite.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `code/teacher_chars.do:75`

## Deviations a rerun would have to log

- **STATA_NETWORK_INSTALL**: Do-files install `pkg', tuples from the network at run time, with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.
  Evidence: `code/estimate_variance_robustness.do:21`, `code/set_options.do:34`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata (version 10.1, 11 named in code); the desk says it has it.
  Evidence: `code/covariate_correlation_part1.do`, `code/entry_ivs_part1.do`, `code/entry_ivs_part2.do`, `code/entry_ivs_part3.do`, `code/estimate_heterog_variance.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: data/teacher_covars.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `data/teacher_covars.dta`
- **UNRESOLVED_PATHS**: 44 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `build code/build_final.py:29`, `build code/build_final.py:131`, `build code/build_final.py:206`, `build code/build_final.py:386`, `build code/build_final.py:406`, `build code/build_final.py:430`, `build code/build_final.py:535`, `build code/build_final.py:538`, `build code/build_final.py:587`, `build code/build_final.py:590`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.

## What triage looked at

- 54 files, 59,953,600 bytes. Languages: python (19), shell (3), stata (15).
- Documentation read: README.md. Licences named: BSD.
- Master scripts: none.
- File reads traced: 105; writes: 77; unresolved paths: 44; missing: analysis_11_01_2021.dta, offense_newonly_2020-09-08.pkl, schoolexit.pkl.gz, teach_mean_resids_covmale.dta, teach_mean_resids_covwhite.dta.
- Links found: 4; checked: no.
