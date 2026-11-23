# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/hsoccer__rum-unobs` at commit `01d74f1f2bf6859622c4878a3e5d1fcc0fada134`
- Triaged: 2026-11-21T18:16:34Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.028 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 1 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **MISSING_INPUT_DOWNLOAD**: `RCM_multi_data.tex` is not in the package; the documentation (README.md) says to download it from https://doi.org/10.1093/ej/uez039, https://doi.org/10.1093/ej/uez039. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `from_tex_to_csv.py:7`, `https://doi.org/10.1093/ej/uez039`, `https://doi.org/10.1093/ej/uez039`

## Notes

- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: collective_choice_data.csv. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `collective_choice_data.csv`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 12 files, 1,697,750 bytes. Languages: python (5).
- Documentation read: README.md. Licences named: none.
- Master scripts: make_lottery_figure.py.
- File reads traced: 2; writes: 3; unresolved paths: 0; missing: rcm_multi_data.tex.
- Links found: 1; checked: no.
