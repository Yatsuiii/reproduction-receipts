# Triage verdict: BLOCKED

- Package: `pkgs/chrisconlon__Liquor_Replication_JPE` at commit `97567b1968f44980a47a7b72c1928a5e01255a67`
- Triaged: 2026-11-21T18:16:40Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.503 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 2 blockers, 5 deviations, 1 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `../proc_data/annual_discus_raw.parquet` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `cleaning_code/reference/1b_predict_discus.R:11`
- **MISSING_INPUT_RESTRICTED**: `../proc_data/predict_manuf.parquet` is read by the code but is not in the package, and the documentation (cleaning_code/README.md) describes it as restricted ("nielsen"). The desk cannot run this without access.
  Evidence: `cleaning_code/1d_impute_manuf.R:10`

## Deviations a rerun would have to log

- **PYTHON2_SYNTAX**: 5 Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 interpreter (end of life since 2020) or a port, and either is a logged deviation.
  Evidence: `counterfactual_code/10_tagging.ipynb`, `counterfactual_code/11_extra_response_plots.ipynb`, `counterfactual_code/7_appendix_sales_prices.ipynb`, `counterfactual_code/8_appendix_time_variation.ipynb`, `counterfactual_code/9_appendix_plot_both_tax.ipynb`
- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: matplotlib>=3.6.0; numpy>=1.22.4; pandas>=1.5.2; polars>=0.19.0; pyblp>=0.13.0; pyfixest>=0.2.0; scikit_learn>=1.1.3; scipy>=1.9.0; seaborn>=0.12.1; statsmodels>=0.13.2. A rerun installs whatever is current and must log the versions it got.
  Evidence: `requirements.txt`
- **UNDECLARED_DEPENDENCIES**: Python code imports cycler, ipumspy, which no dependency file names.
  Evidence: `cleaning_code/0_read_kilts.py`, `cleaning_code/1c_monthly_prices.py`, `cleaning_code/1e_combine_monthly.py`, `cleaning_code/2_combine_quarterly.py`, `cleaning_code/3_process_agents.py`
- **UNPINNED_DEPENDENCIES**: R code loads arrow, broom, fixest, latex2exp, ranger, tidyverse with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `cleaning_code/1d_impute_manuf.R:1`, `cleaning_code/1d_impute_manuf.R:2`, `cleaning_code/1d_impute_manuf.R:3`, `cleaning_code/1d_impute_manuf.R:4`, `cleaning_code/1d_impute_manuf.R:5`
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `counterfactual_code/download_acs.py:162`, `counterfactual_code/download_acs.py:166`, `counterfactual_code/download_acs.py:170`

## Notes

- **UNRESOLVED_PATHS**: 11 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `cleaning_code/process_inputs.py:174`, `cleaning_code/reference/2_combine_quarterly_original.py:73`, `cleaning_code/reference/panel_regression.py:63`, `counterfactual_code/0_nielsen_figures.py:40`, `counterfactual_code/1_descriptive_tables.py:34`, `counterfactual_code/2_manufacturer_plots.py:33`, `counterfactual_code/2b_price_plots.py:46`, `counterfactual_code/4_parameter_tables.py:22`, `counterfactual_code/4c_rho_sensitivity_table.py:109`, `counterfactual_code/5_diversion_plot.py:37`

## What triage looked at

- 257 files, 355,111,812 bytes. Languages: python (69), r (3), shell (6).
- Documentation read: README.md, cleaning_code/README.md, cleaning_code/reference/README.md, estimation_outputs/README.md, our_inputs/our_inputs_readme.md, paper_output_checklist.md, raw_data/raw_data_readme.md, raw_nielsen_data/README.md. Licences named: MIT.
- Master scripts: cleaning_code/0_read_kilts.py, counterfactual_code/0_nielsen_figures.py.
- File reads traced: 19; writes: 43; unresolved paths: 11; missing: annual_discus_raw.parquet, predict_manuf.parquet.
- Links found: 10; checked: no.
