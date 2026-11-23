# Triage verdict: BLOCKED

- Package: `pkgs/akhederlarian__pre-trends-TTBs` at commit `e2077db1470536a50411c2acf253e5381e717f76`
- Triaged: 2026-11-21T18:16:34Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.012 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 1 blockers, 0 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **NO_CODE**: No code files were found, so there is nothing to run. The package may hold data or results only.

## Notes

- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("proprietary") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 9 files, 5,787,234 bytes. Languages: none.
- Documentation read: README.md, datasets/readme.md. Licences named: none.
- Master scripts: none.
- File reads traced: 0; writes: 0; unresolved paths: 0; missing: none.
- Links found: 7; checked: no.
