# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/ballesterogh_algorithmic-collusion-IJIO-replication-code` at commit `47173bbf52621c19a40d061dfe4dee2d3bd5678f`
- Triaged: 2026-11-23T17:48:00Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.045 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 2 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Julia code without a Manifest.toml: package versions are not pinned.
  Evidence: `code/init_deterministic.jl`, `code/init_stochastic.jl`, `code/main.jl`, `code/qlearning_deterministic.jl`, `code/qlearning_stochastic.jl`
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `code/main.jl:3`, `figures_tables_appendix/table_D3_B.jl:6`, `figures_tables_appendix/table_D3_C.jl:6`

## Notes

- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("upon request") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 58 files, 634,175 bytes. Languages: julia (36).
- Documentation read: README.md. Licences named: none.
- Master scripts: code/main.jl.
- File reads traced: 50; writes: 19; unresolved paths: 0; missing: none.
- Links found: 2; checked: no.
