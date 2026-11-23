# Triage verdict: RUNNABLE

- Package: `pkgs/pmichaillat__pricing-fairness` at commit `a8d5d758eef3cffabe154e07b58e3cb150113a50`
- Triaged: 2026-11-21T18:16:39Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.016 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 0 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `figure1.m`, `figure2.m`, `figure3.m`, `figureB1.m`
- **SOFTWARE_REQUIRED**: Requires Dynare (free) inside MATLAB or Octave, version 4.5.7 named in the documentation.
  Evidence: `irfFairnessMonetary.mod`, `irfFairnessTechnology.mod`, `irfTextbookMonetary.mod`, `irfTextbookTechnology.mod`, `passthrough.mod`

## What triage looked at

- 12 files, 64,226 bytes. Languages: dynare (5), matlab (4).
- Documentation read: LICENSE.md, README.md. Licences named: MIT.
- Master scripts: none.
- File reads traced: 0; writes: 35; unresolved paths: 0; missing: none.
- Links found: 5; checked: no.
