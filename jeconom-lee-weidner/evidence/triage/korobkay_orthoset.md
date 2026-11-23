# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/korobkay_orthoset` at commit `9e7af8d7a82d0b531304fbebab45f97d70bcf431`
- Triaged: 2026-11-23T17:48:01Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.033 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 1 deviations, 1 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Python code imports matplotlib, numpy, pandas, scipy, sklearn but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `common.py`, `estimate.py`, `figure.py`

## Notes

- **UNRESOLVED_PATHS**: 1 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `figure.py:34`

## What triage looked at

- 6 files, 4,653,276 bytes. Languages: python (3).
- Documentation read: README.md. Licences named: MIT.
- Master scripts: none.
- File reads traced: 1; writes: 0; unresolved paths: 1; missing: none.
- Links found: 0; checked: no.
