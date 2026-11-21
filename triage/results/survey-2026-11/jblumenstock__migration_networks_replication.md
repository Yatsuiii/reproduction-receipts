# Triage verdict: BLOCKED

- Package: `pkgs/jblumenstock__migration_networks_replication` at commit `2651b34cf01a2c9892117c90e1d8dae837b5201c`
- Triaged: 2026-11-21T18:16:57Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 14.771 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 8 blockers, 4 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `cdr_move_from_district_proportion.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `figures/figure_A13_step2.py:11`
- **MISSING_INPUT_UNDOCUMENTED**: `census_destination_simple.csv` is read by the code and named in the documentation (README.md, figures/README.md), but it is not in the package and no source for it is given.
  Evidence: `figures/figure_A13_step2.py:8`, `figures/figure_A1_step2.py:8`
- **MISSING_INPUT_UNDOCUMENTED**: `census_origin.csv` is read by the code and named in the documentation (README.md, figures/README.md), but it is not in the package and no source for it is given.
  Evidence: `figures/figure_A1_step2.py:9`
- **MISSING_INPUT_RESTRICTED**: `data/dest_home_d_s_l_6month_lag.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `tables/table_A12.R:6`
- **MISSING_INPUT_RESTRICTED**: `data/dest_home_for_regression_information_support_diff_between_-12_to_-2_month.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `tables/table_A13_step3.R:62`
- **MISSING_INPUT_RESTRICTED**: `data/dest_home_for_regression_information_support_diff_between_-6_to_-2_month.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `tables/table_A13_step3.R:3`
- **MISSING_INPUT_RESTRICTED**: `data/inset_degree_distribution_dest.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `figures/figure_6bd_7bd_A6bd_step5_plot.py:132`
- **MISSING_INPUT_RESTRICTED**: `data/inset_degree_distribution_home.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `figures/figure_6bd_7bd_A6bd_step5_plot.py:133`

## Deviations a rerun would have to log

- **PYTHON2_SYNTAX**: 1 Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 interpreter (end of life since 2020) or a port, and either is a logged deviation.
  Evidence: `tables/table_A10_step2_support_strong.py`
- **NO_DEPENDENCY_SPEC**: Python code imports dateutil, graphlab, matplotlib, numpy, pandarallel, pandas, seaborn, snap, statsmodels, turicreate but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `figures/figure_4_A2_A3.py`, `figures/figure_5_6ac_7ac.py`, `figures/figure_6bd_7bd_A6bd_step1_generate_data_for_regression.py`, `figures/figure_6bd_7bd_A6bd_step2_convert_data.py`, `figures/figure_6bd_7bd_A6bd_step3_sampling.py`
- **UNPINNED_DEPENDENCIES**: R code loads fixest, lfe, stargazer with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `figures/figure_6bd_7bd_A6bd_step4_regression.R:1`, `tables/table_2_step2_regression.R:1`, `tables/table_A10_step3.R:1`, `tables/table_A11_step3.R:1`, `tables/table_A12.R:1`
- **LONG_COMPUTE**: The documentation claims a run time of about 8640 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: data/cdr_move_from_district_proportion_2month.csv, data/cdr_move_to_district_proportion_12month.csv, data/cdr_move_to_district_proportion_2month.csv, data/cdr_move_to_district_proportion_6month.csv, data/cluster_dest_for_regression_22degree_sampled_10pct.csv, data/dest_home_d_s_l.csv, data/dest_home_d_s_l_infor_strong.csv, data/dest_home_d_s_l_information_overall_network.csv, data/dest_home_d_s_l_recent_migrant.csv, data/dest_home_d_s_l_shorttime_longtime.csv. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `data/cdr_move_from_district_proportion_2month.csv`, `data/cdr_move_to_district_proportion_12month.csv`, `data/cdr_move_to_district_proportion_2month.csv`, `data/cdr_move_to_district_proportion_6month.csv`, `data/cluster_dest_for_regression_22degree_sampled_10pct.csv`, `data/dest_home_d_s_l.csv`, `data/dest_home_d_s_l_infor_strong.csv`, `data/dest_home_d_s_l_information_overall_network.csv`, `data/dest_home_d_s_l_recent_migrant.csv`, `data/dest_home_d_s_l_shorttime_longtime.csv`
- **UNRESOLVED_PATHS**: 72 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `figures/figure_4_A2_A3.py:24`, `figures/figure_4_A2_A3.py:39`, `figures/figure_5_6ac_7ac.py:255`, `figures/figure_5_6ac_7ac.py:265`, `figures/figure_6bd_7bd_A6bd_step1_generate_data_for_regression.py:86`, `figures/figure_6bd_7bd_A6bd_step2_convert_data.py:49`, `figures/figure_6bd_7bd_A6bd_step5_plot.py:134`, `figures/figure_6bd_7bd_A6bd_step5_plot.py:135`, `figures/figure_6bd_7bd_A6bd_step5_plot.py:136`, `figures/figure_A10_A11_A12_step1_calcualte_utility.py:263`
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE`

## What triage looked at

- 107 files, 495,559 bytes. Languages: python (40), r (15).
- Documentation read: README.md, data/README.md, figures/README.md. Licences named: CC BY-NC, GPL.
- Master scripts: none.
- File reads traced: 125; writes: 60; unresolved paths: 72; missing: cdr_move_from_district_proportion.csv, census_destination_simple.csv, census_origin.csv, dest_home_d_s_l_6month_lag.csv, dest_home_for_regression_information_support_diff_between_-12_to_-2_month.csv, dest_home_for_regression_information_support_diff_between_-6_to_-2_month.csv, inset_degree_distribution_dest.csv, inset_degree_distribution_home.csv.
- Links found: 3; checked: no.
