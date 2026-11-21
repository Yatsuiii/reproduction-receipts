# Triage verdict: BLOCKED

- Package: `https://github.com/mbholm/MPC-Heterogeneity-and-Household-Balance-Sheets` at commit `c9c41c7169c92fba0e4181aa1ad62a88e09d6373`
- Triaged: 2026-11-21T12:12:30Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.038 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 3 blockers, 1 deviations, 6 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `$data/consumption_w_housing_wealth.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `stata/codes/TAB6.do:145`
- **MISSING_INPUT_UNDOCUMENTED**: `$data/FHMN_cons.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `stata/codes/TAB6.do:137`
- **MISSING_INPUT_UNDOCUMENTED**: `$data/lnr_mlnr_flnr_updated2013.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `stata/codes/prep_family.do:41`, `stata/codes/prep_family.do:59`, `stata/codes/prep_family.do:90`, `stata/codes/prep_family.do:96`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.

## Notes

- **README_NOT_TEXT**: The README is not plain text (Readme.lyx, Readme.pdf). Triage cannot read it, so the data availability statement, licence and run time below were not checked against it. Read it by hand.
  Evidence: `Readme.lyx`, `Readme.pdf`
- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `matlab/figure_codes/FIG2.m`, `matlab/figure_codes/FIG3.m`, `matlab/figure_codes/FIG4.m`, `matlab/figure_codes/FIGA2.m`, `matlab/figure_codes/FIGA3.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `stata/codes/FIG1.do`, `stata/codes/FIG2.do`, `stata/codes/FIG3.do`, `stata/codes/FIGA1.do`, `stata/codes/FIGA3.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: FIG4.mat. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `FIG4.mat`
- **UNRESOLVED_PATHS**: 11 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `matlab/figure_codes/FIG3.m:16`, `matlab/figure_codes/FIG3.m:19`, `matlab/figure_codes/FIGA4.m:14`, `matlab/figure_codes/FIGA7.m:19`, `matlab/figure_codes/FIGA7.m:20`, `matlab/figure_codes/FIGA7.m:21`, `matlab/figure_codes/FIGA8.m:16`, `matlab/figure_codes/FIGA8.m:19`, `matlab/figure_codes/FIGA8.m:65`, `matlab/figure_codes/FIGA8.m:66`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 122 files, 2,766,216 bytes. Languages: matlab (15), stata (26).
- Documentation read: none. Licences named: none.
- Master scripts: matlab/figure_codes/runall.m, stata/codes/runall.do.
- File reads traced: 63; writes: 31; unresolved paths: 11; missing: consumption_w_housing_wealth.dta, fhmn_cons.dta, lnr_mlnr_flnr_updated2013.dta.
- Links found: 0; checked: yes.
