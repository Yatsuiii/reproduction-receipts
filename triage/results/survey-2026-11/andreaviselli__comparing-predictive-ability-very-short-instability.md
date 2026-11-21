# Triage verdict: RUNNABLE

- Package: `pkgs/andreaviselli__comparing-predictive-ability-very-short-instability` at commit `09efc854d246d3b068c2e3f21e7ba8093561fede`
- Triaged: 2026-11-21T18:16:37Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.016 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 0 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `ReplicationCode_MC_Table_1.m`, `ReplicationCode_MC_Table_2.m`, `ReplicationCode_MC_Table_3.m`, `ReplicationCode_MC_Table_4.m`, `ReplicationCode_MC_Table_5.m`
- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("proprietary") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.

## What triage looked at

- 15 files, 107,313 bytes. Languages: matlab (11).
- Documentation read: README.md. Licences named: CC0, MIT.
- Master scripts: none.
- File reads traced: 1; writes: 0; unresolved paths: 0; missing: none.
- Links found: 4; checked: no.
