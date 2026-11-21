# Triage verdict: BLOCKED

- Package: `https://github.com/timhdesilva/replication_qje2025` at commit `7d944b14fb5fd38f5848d62cf1caf3af0b5fa0ef`
- Triaged: 2026-11-21T12:12:22Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.376 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 13 blockers, 4 deviations, 6 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `R:\\madipge-ato-d-clientreg-demogs-06-21\\ato_cr_demogs_0621.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/datalab/01_build.py:45`
- **MISSING_INPUT_UNDOCUMENTED**: `R:\\madipge-ato-c-spine-conc\\ato_v5_spine.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/datalab/01_build.py:286`
- **MISSING_INPUT_UNDOCUMENTED**: `R:\\madip-ge-030103d-census2016-census2016dwelling-2016\madip-ge-030103d-census2016-census2016dwelling-2016\census_2016_dwelling.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/datalab/01_build.py:318`
- **MISSING_INPUT_UNDOCUMENTED**: `R:\\madip-ge-030101d-census2016-census2016person-2016\madip-ge-030101d-census2016-census2016person-2016\census_2016_person.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/datalab/01_build.py:314`
- **MISSING_INPUT_UNDOCUMENTED**: `R:\\madipge-cen16-c-spine-conc\census_2016_v5_spine.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/datalab/01_build.py:293`
- **MISSING_INPUT_UNDOCUMENTED**: `Cleaned/ComparePolicies.pcl` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `model/POST_results_existing.py:22`
- **MISSING_INPUT_UNDOCUMENTED**: `help_2004.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/alife_fullsample/02_moments_panel.py:42`
- **MISSING_INPUT_UNDOCUMENTED**: `help_2005.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/alife_fullsample/02_moments_panel.py:50`
- **MISSING_INPUT_UNDOCUMENTED**: `longitudinal_weights_t200c.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirics/code/hilda/01_compute_hours_moments.py:36`, `empirics/code/hilda/01_make_ALife_inputs.py:22`
- **MISSING_INPUT_UNDOCUMENTED**: `Output/ModelMoments.txt` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `model/POST_plot_fit.py:26`
- **MISSING_INPUT_UNDOCUMENTED**: `Cleaned/OptimalPolicies.pcl` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `model/POST_results_optimal.py:39`
- **MISSING_INPUT_UNDOCUMENTED**: `Cleaned/OptimalPolicies_initialV.pcl` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `model/POST_results_optimal.py:41`
- **MISSING_INPUT_UNDOCUMENTED**: `Output/SMM.txt` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `model/POST_plot_fit.py:25`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: pandas>=1.3.0; numpy>=1.21.0; statsmodels>=0.12.0; sklearn>=0.24.0; patsy>=0.5.0; matplotlib>=3.3.0; cycler>=0.10.0; dask>=2021.0.0; xlrd>=2.0.0  # For reading Excel files; openpyxl>=3.0.0  # Alternative Excel reader. A rerun installs whatever is current and must log the versions it got.
  Evidence: `empirics/requirements_empirics.txt`
- **UNDECLARED_DEPENDENCIES**: Python code imports scipy, tabulate, which no dependency file names.
  Evidence: `empirics/code/alife/01_build.py`, `empirics/code/alife/01_moments_capital.py`, `empirics/code/alife/01_moments_wage.py`, `empirics/code/alife/01_occupation.py`, `empirics/code/alife/02_moments_debt.py`
- **ABSOLUTE_PATH**: 25 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `empirics/code/alife/directories.py:6`, `empirics/code/alife/directories.py:7`, `empirics/code/alife/directories.py:10`, `empirics/code/alife/directories.py:13`, `empirics/code/alife/directories.py:16`, `empirics/code/alife/directories.py:23`, `empirics/code/alife/directories.py:26`, `empirics/code/alife/directories.py:29`, `empirics/code/alife/directories.py:32`, `empirics/code/datalab/01_build.py:44`

## Notes

- **README_NOT_TEXT**: The README is not plain text (README.pdf). Triage cannot read it, so the data availability statement, licence and run time below were not checked against it. Read it by hand.
  Evidence: `README.pdf`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `empirics/code/alife/02_moments_capital_yrfe.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: occupation2_stats.csv. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `occupation2_stats.csv`
- **UNRESOLVED_PATHS**: 30 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `empirics/code/alife/01_build.py:85`, `empirics/code/alife/01_build.py:150`, `empirics/code/alife/01_moments_capital.py:53`, `empirics/code/alife/01_moments_wage.py:50`, `empirics/code/alife/01_occupation.py:33`, `empirics/code/alife/02_moments_capital_yrfe.do:13`, `empirics/code/alife_fullsample/01_build.py:79`, `empirics/code/alife_fullsample/01_build.py:144`, `empirics/code/alife_fullsample/02_bunching.py:41`, `empirics/code/alife_fullsample/02_bunching.py:47`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 143 files, 960,709 bytes. Languages: fortran (23), python (46), shell (7), stata (1).
- Documentation read: none. Licences named: none.
- Master scripts: empirics/code/alife/01_build.py, empirics/code/alife/01_moments_capital.py, empirics/code/alife/01_moments_wage.py, empirics/code/alife/01_occupation.py, empirics/code/alife/02_moments_capital_yrfe.do, empirics/code/alife/02_moments_debt.py, empirics/code/alife/main.sh, empirics/code/alife_fullsample/01_build.py, empirics/code/alife_fullsample/02_bunching.py, empirics/code/alife_fullsample/02_bunching_heterogeneity.py, empirics/code/alife_fullsample/02_moments_bunching.py, empirics/code/alife_fullsample/02_moments_panel.py, empirics/code/alife_fullsample/02_moments_ratios.py, empirics/code/alife_fullsample/02_occupation.py, empirics/code/alife_fullsample/02_summarystats.py, empirics/code/alife_fullsample/main.sh, empirics/code/datalab/01_build.py, empirics/code/datalab/02_plots.py, empirics/code/datalab/main.sh, empirics/code/hilda/01_calibrate_A0.py, empirics/code/hilda/01_calibrate_borrowing_constraint.py, empirics/code/hilda/01_calibrate_eqscale.py, empirics/code/hilda/01_compute_hours_moments.py, empirics/code/hilda/01_make_ALife_inputs.py, empirics/code/hilda/main.sh, empirics/code/miscellaneous/01_mortality.py, empirics/code/miscellaneous/01_rates_dollars.py, empirics/code/miscellaneous/01_smoothed_tax.py, empirics/code/miscellaneous/main.sh.
- File reads traced: 51; writes: 37; unresolved paths: 30; missing: ato_cr_demogs_0621.csv, ato_v5_spine.csv, census_2016_dwelling.csv, census_2016_person.csv, census_2016_v5_spine.csv, comparepolicies.pcl, help_2004.dta, help_2005.dta, longitudinal_weights_t200c.dta, modelmoments.txt, optimalpolicies.pcl, optimalpolicies_initialv.pcl, smm.txt.
- Links found: 0; checked: yes.
