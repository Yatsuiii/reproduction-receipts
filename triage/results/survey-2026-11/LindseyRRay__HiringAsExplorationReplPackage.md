# Triage verdict: BLOCKED

- Package: `pkgs/LindseyRRay__HiringAsExplorationReplPackage` at commit `d830a57846520bbaa1dd12a964abed4fc80e5b48`
- Triaged: 2026-11-21T18:16:58Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.109 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 3 blockers, 1 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `$analysis_dir/simulation_results/all.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `HaE_main.do:64`
- **MISSING_INPUT_RESTRICTED**: `$analysis_dir/simulation_results/all_offer.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `HaE_main.do:72`
- **MISSING_INPUT_RESTRICTED**: `$analysis_dir/data_desc.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `HaE_main.do:79`, `HaE_main.do:137`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `HaE_main.do`
- **UNRESOLVED_PATHS**: 9 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `HaE_main.do:288`, `HaE_main.do:312`, `HaE_main.do:519`, `HaE_main.do:553`, `HaE_main.do:574`, `aggregation_helpers.py:13`, `quota_policies.py:84`, `run_simulation_helpers.py:306`, `run_simulations.py:22`

## What triage looked at

- 17 files, 137,775 bytes. Languages: python (12), stata (1).
- Documentation read: README.md. Licences named: MIT.
- Master scripts: none.
- File reads traced: 25; writes: 25; unresolved paths: 9; missing: all.csv, all_offer.csv, data_desc.dta.
- Links found: 0; checked: no.
