# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `/home/claude/receipt2/pkg-inspect` at commit `325bb7d99908de5df94c9c709bcf37ccbdbff5ae`
- Triaged: 2026-11-23T03:56:18Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.191 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 1 deviations, 0 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: numpy; numba; tqdm. A rerun installs whatever is current and must log the versions it got.
  Evidence: `requirements.txt`

## What triage looked at

- 16 files, 220,965 bytes. Languages: python (6).
- Documentation read: README.md. Licences named: MIT.
- Master scripts: none.
- File reads traced: 0; writes: 0; unresolved paths: 0; missing: none.
- Links found: 5; checked: no.
