# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/mdcattaneo_replication-CFS_2026_AOS` at commit `f1808a74465422911ca5f7e53ad4dd8cd8178737`
- Triaged: 2026-11-23T17:48:02Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.066 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 1 deviations, 1 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Python code imports numpy, scipy, sweep_definitions but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `estimate.py`, `main.py`

## Notes

- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 3 files, 36,130 bytes. Languages: python (2).
- Documentation read: README.md. Licences named: none.
- Master scripts: main.py.
- File reads traced: 0; writes: 0; unresolved paths: 0; missing: none.
- Links found: 3; checked: no.
