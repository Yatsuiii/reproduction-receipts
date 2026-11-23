# Triage verdict: BLOCKED

- Package: `pkgs/mbholm__Transmission-of-Monetary-Policy-under-the-Microscope` at commit `c7677d15754508208d41f83e547fa64018a841d5`
- Triaged: 2026-11-21T18:16:40Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.031 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 1 blockers, 1 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `$w5_data/mp_shocks_norway_w_lags.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Stata/vPUB_prep_data.do:23`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.

## Notes

- **README_NOT_TEXT**: The README is not plain text (Readme.pdf). Triage cannot read it, so the data availability statement, licence and run time below were not checked against it. Read it by hand.
  Evidence: `Readme.pdf`
- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `Matlab/Fig_MPC_by_liquid.m`, `Matlab/Fig_direct_indirect_IRFs.m`, `Matlab/Fig_macro_IRFs.m`, `Matlab/Fig_micro_IRFs.m`, `Matlab/Fig_micro_macro_IRFs.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `Stata/vPUB_lottery.do`, `Stata/vPUB_main.do`, `Stata/vPUB_micro_all_rta.do`, `Stata/vPUB_micro_all_rti_bal.do`, `Stata/vPUB_micro_direct_indirect.do`
- **UNRESOLVED_PATHS**: 24 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Stata/vPUB_main.do:99`, `Stata/vPUB_main.do:115`, `Stata/vPUB_main.do:116`, `Stata/vPUB_main.do:117`, `Stata/vPUB_main.do:122`, `Stata/vPUB_main.do:123`, `Stata/vPUB_main.do:124`, `Stata/vPUB_main.do:140`, `Stata/vPUB_main.do:141`, `Stata/vPUB_main.do:147`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 99 files, 10,204,770 bytes. Languages: matlab (16), stata (12).
- Documentation read: none. Licences named: none.
- Master scripts: Matlab/runall.m.
- File reads traced: 76; writes: 32; unresolved paths: 24; missing: mp_shocks_norway_w_lags.dta.
- Links found: 0; checked: no.
