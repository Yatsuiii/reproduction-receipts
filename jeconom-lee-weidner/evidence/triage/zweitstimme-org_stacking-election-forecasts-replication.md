# Triage verdict: BLOCKED

- Package: `pk/zweitstimme-org_stacking-election-forecasts-replication` at commit `5f12ee2f1e81371bedefecfb0c022b5c84d55acd`
- Triaged: 2026-11-23T17:48:03Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.192 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 10 blockers, 6 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **PROPRIETARY_SOFTWARE**: Requires Stata, which is proprietary and not declared available on this desk. Rerun triage with --have stata if a licensed copy is available.
  Evidence: `app_us/input/replication_papers/tien/Pres2024 Forecast Tien Lewis-Beck.do`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_coef_draws.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:801`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_elpd_by_model.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:76`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_loglik_fund.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:74`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_loglik_poll.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:75`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_pred_draws_fund.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:86`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_pred_draws_poll.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:87`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_pred_fund.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:79`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_pred_poll.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:80`
- **MISSING_INPUT_RESTRICTED**: `output/mdl_est/de_weights_by_lead.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `app_germany/05_figures_tables.R:73`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **UNPINNED_DEPENDENCIES**: R code loads DataCombine, EBMAforecast, R, brms, broom, dplyr, forcats, frequency, ggforce, ggh4x, ggplot2, ggrepel, glue, haven, lmtest, loo, lubridate, marginaleffects, modelsummary, patchwork, plyr, readr, readxl, rstan, rvest, sandwich, scales, setup.R, tibble, tidyr, tidyverse, zoo with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `app_germany/04b_L_robustness.R:17`, `app_germany/04b_L_robustness.R:18`, `app_germany/05_figures_tables.R:21`, `app_germany/05_figures_tables.R:22`, `app_germany/05_figures_tables.R:23`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (download.file). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `app_us/R/abramowitz_time_for_change.R:162`, `app_us/R/hibbs_bread_peace.R:51`
- **RUNTIME_DOWNLOAD**: Code downloads https://fred.stlouisfed.org/graph/fredgraph.csv?id=A191RL1Q225SBEA at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `app_us/R/abramowitz_time_for_change.R:153`
- **ABSOLUTE_PATH**: 50 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:51`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:53`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:77`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:87`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:92`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:99`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:103`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:105`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:107`, `app_us/input/replication_papers/algara/PS_Forecasting_Analysis.R:109`
- **LONG_COMPUTE**: The documentation claims a run time of about 336 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **UNRESOLVED_PATHS**: 22 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `app_germany/R/de_ebma_woc.R:200`, `app_germany/R/de_ebma_woc.R:207`, `app_germany/R/de_ebma_woc.R:208`, `app_us/04_figures_tables.R:78`, `app_us/04_figures_tables.R:79`, `app_us/04_figures_tables.R:80`, `app_us/04b_performance_subsets.R:56`, `app_us/04b_performance_subsets.R:57`, `app_us/04b_performance_subsets.R:60`, `app_us/04b_performance_subsets.R:66`
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE`

## What triage looked at

- 127 files, 2,327,156 bytes. Languages: r (30), stata (1).
- Documentation read: README.md, app_us/docs/FORECASTING_2024_COLLECTION.md, app_us/docs/mhw_ebma_component_models_scope.md, app_us/docs/ps_2024_symposium_model_scope.md, app_us/docs/us_implementation_departures.md, app_us/input/replication_papers/abramowitz/README.md, app_us/input/replication_papers/algara/Read_Me_PS_Forecasting_Analysis.txt, app_us/input/replication_papers/campbell/README.md, app_us/input/replication_papers/erikson_wlezien/README.md, app_us/input/replication_papers/fair/README.md, app_us/input/replication_papers/hibbs/README.md. Licences named: CC BY-NC, CC0, MIT.
- Master scripts: 0_setup.R, Makefile, app_germany/01_prepare_data.R, app_germany/02_dlm_estimation.R, app_germany/03_prepare_model_data.R, app_germany/04_estimation.R, app_germany/04b_L_robustness.R, app_germany/05_figures_tables.R, app_us/01_prepare_data.R, app_us/02_estimation.R, app_us/03_post_estimation.R, app_us/04_figures_tables.R, app_us/04b_performance_subsets.R, app_us/04e_jackknife_leavek.R, app_us/04f_forecasts_appendix.R, app_us/05_robustness_L.R.
- File reads traced: 82; writes: 50; unresolved paths: 22; missing: de_coef_draws.rds, de_elpd_by_model.csv, de_loglik_fund.rds, de_loglik_poll.rds, de_pred_draws_fund.rds, de_pred_draws_poll.rds, de_pred_fund.rds, de_pred_poll.rds, de_weights_by_lead.rds.
- Links found: 29; checked: no.
