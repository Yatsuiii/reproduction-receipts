# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/yonathanarbel_generative-reasonable-person` at commit `00c0e042932ca3f0301e03bac7620d5523a7bb03`
- Triaged: 2026-11-23T17:48:03Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.471 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 2 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNDECLARED_DEPENDENCIES**: Python code imports graphviz, matplotlib, vl_convert, which no dependency file names.
  Evidence: `Common/Scripts/__init__.py`, `Common/Scripts/srct_diagram.py`, `Common/Scripts/style.py`, `Common/__init__.py`, `Jaeger/Scripts/analysis.py`
- **ABSOLUTE_PATH**: 2 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `Common/Scripts/srct_diagram.py:478`, `Common/Scripts/srct_diagram.py:507`

## Notes

- **UNRESOLVED_PATHS**: 2 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Sommers/Scripts/data_generation.py:99`, `SommersFurth/Scripts/data_generation.py:214`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 47 files, 15,039,061 bytes. Languages: python (17).
- Documentation read: PROVENANCE.md, README.md. Licences named: none.
- Master scripts: reproduce.py.
- File reads traced: 8; writes: 9; unresolved paths: 2; missing: none.
- Links found: 2; checked: no.
