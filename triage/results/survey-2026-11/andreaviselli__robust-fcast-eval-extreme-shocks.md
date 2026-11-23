# Triage verdict: RUNNABLE

- Package: `pkgs/andreaviselli__robust-fcast-eval-extreme-shocks` at commit `f8e38a2a1ecc99a9636fb674a59c601c54294a96`
- Triaged: 2026-11-21T18:16:37Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.009 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 0 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `ReplicationCode_Fig_1_Table_3.m`, `ReplicationCode_MC_Calibrated.m`, `ReplicationCode_MC_Table_1_2.m`, `run_mc_spec.m`
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: The Econometrics Toolbox. Each is licensed separately; check the desk's MATLAB has them.

## What triage looked at

- 7 files, 32,295 bytes. Languages: matlab (4).
- Documentation read: README.md. Licences named: MIT.
- Master scripts: none.
- File reads traced: 1; writes: 0; unresolved paths: 0; missing: none.
- Links found: 1; checked: no.
