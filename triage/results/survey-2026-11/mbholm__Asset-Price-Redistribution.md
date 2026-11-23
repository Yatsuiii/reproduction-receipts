# Triage verdict: BLOCKED

- Package: `pkgs/mbholm__Asset-Price-Redistribution` at commit `6636b72eafad8506756f4fa7e76b50b542ab70ad`
- Triaged: 2026-11-21T18:16:40Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.055 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 28 blockers, 3 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/cooperative_transactions_by_sector` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/2 - kappa.do:249`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/corr_welfare_revgain_sc_rank_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:315`
- **MISSING_INPUT_UNDOCUMENTED**: `$data/cpi_1960_2020_USD.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Pre/aggregate_housing_transactions.do:44`, `Code/Pre/aggregate_housing_transactions.do:88`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/hist_revgain_total_sc_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:273`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/hist_welfare_total_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:226`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/hist_welfare_total_diff_xi_10_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:345`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/hist_welfare_total_sc_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:126`, `Code/Stata/3 - individuals.do:239`, `Code/Stata/3 - individuals.do:269`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/housing_transactions_by_sector` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/2 - kappa.do:243`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/interest_rate_and_ltv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:359`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/interest_rate_and_ltv_regression` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:382`
- **MISSING_INPUT_UNDOCUMENTED**: `$data/lnr_mlnr_flnr_updated2013.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Pre/P_clean_bequest_data.do:94`, `Code/Pre/P_clean_bequest_data.do:99`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/planner_welfare` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:252`
- **MISSING_INPUT_UNDOCUMENTED**: `${output}/planner_welfare.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Pre/welfare_histograms.do:229`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/sum_stats_stocks_1993` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:48`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/sum_stats_welfare_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:97`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/sum_stats_welfare_total_diff_xi_10_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:325`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/sum_stats_welfare_total_diff_xi_5_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:330`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Aggregate Data/Table10788` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/2 - kappa.do:23`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/welfare_cohort_xi_0` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/4 - bycohort.do:275`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/welfare_cohort_xi_10` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/4 - bycohort.do:283`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/welfare_cohort_xi_5` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/4 - bycohort.do:279`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/welfare_effect_decompose_100` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:168`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/welfare_revgain_sc_heatmap_5_1994` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:297`
- **MISSING_INPUT_UNDOCUMENTED**: `$WorldscopePath/wrds_ws_company.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Pre/worldscope.do:7`
- **MISSING_INPUT_UNDOCUMENTED**: `$WorldscopePath/wrds_ws_funda.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Pre/worldscope.do:19`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/year_cohort` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/2 - kappa.do:352`, `Code/Stata/2 - kappa.do:422`, `Code/Stata/4 - bycohort.do:6`, `Code/Stata/4 - bycohort.do:54`, `Code/Stata/4 - bycohort.do:102`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/year_cohort_percentile` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/5 - bywealth.do:7`, `Code/Stata/5 - bywealth.do:56`
- **MISSING_INPUT_UNDOCUMENTED**: `$MyPath/Data/Micro Data/year_mean_ltv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `Code/Stata/3 - individuals.do:372`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **NO_DEPENDENCY_SPEC**: Julia code without a Manifest.toml: package versions are not pinned.
  Evidence: `Code/Julia/IncompleteMarkets.jl`, `Code/Julia/run.jl`
- **ABSOLUTE_PATH**: 10 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `Code/Julia/run.jl:21`, `Code/Julia/run.jl:22`, `Code/Julia/run.jl:23`, `Code/Julia/run.jl:26`, `Code/Julia/run.jl:30`, `Code/Julia/run.jl:31`, `Code/Julia/run.jl:114`, `Code/Julia/run.jl:115`, `Code/Pre/worldscope.do:2`, `Code/Stata/run.do:1`

## Notes

- **README_NOT_TEXT**: The README is not plain text (README.pdf). Triage cannot read it, so the data availability statement, licence and run time below were not checked against it. Read it by hand.
  Evidence: `README.pdf`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `Code/Pre/P_clean_bequest_data.do`, `Code/Pre/P_copy_data.do`, `Code/Pre/P_final_data.do`, `Code/Pre/P_inheritance_events.do`, `Code/Pre/aggregate_housing_transactions.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: $MyPath/Save/prices.dta, $MyPath/Save/prices_synthetic.dta, $MyPath/Save/sector_scons.dta, $MyPath/data/worldscope/worldscope.csv, $MyPath/save/bycohort_cov.dta, $MyPath/save/bycohort_secondorder_transactions.dta, $MyPath/save/bycohort_synthetic.dta, $MyPath/save/bycohort_welfare_baseline.dta, $MyPath/save/bycohort_welfare_collateral.dta, $MyPath/save/bycohort_welfare_combine.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `$MyPath/Save/prices.dta`, `$MyPath/Save/prices_synthetic.dta`, `$MyPath/Save/sector_scons.dta`, `$MyPath/data/worldscope/worldscope.csv`, `$MyPath/save/bycohort_cov.dta`, `$MyPath/save/bycohort_secondorder_transactions.dta`, `$MyPath/save/bycohort_synthetic.dta`, `$MyPath/save/bycohort_welfare_baseline.dta`, `$MyPath/save/bycohort_welfare_collateral.dta`, `$MyPath/save/bycohort_welfare_combine.dta`
- **UNRESOLVED_PATHS**: 58 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Code/Pre/incomplete_markets.do:132`, `Code/Pre/incomplete_markets.do:137`, `Code/Pre/welfare_histograms.do:97`, `Code/Pre/welfare_histograms.do:163`, `Code/Pre/worldscope.do:21`, `Code/Stata/1 - prices.do:39`, `Code/Stata/1 - prices.do:66`, `Code/Stata/1 - prices.do:83`, `Code/Stata/1 - prices.do:93`, `Code/Stata/1 - prices.do:94`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 816 files, 62,749,003 bytes. Languages: julia (2), stata (21).
- Documentation read: none. Licences named: none.
- Master scripts: Code/Julia/run.jl, Code/Stata/run.do.
- File reads traced: 206; writes: 134; unresolved paths: 58; missing: cooperative_transactions_by_sector, corr_welfare_revgain_sc_rank_1994, cpi_1960_2020_usd.dta, hist_revgain_total_sc_1994, hist_welfare_total_1994, hist_welfare_total_diff_xi_10_1994, hist_welfare_total_sc_1994, housing_transactions_by_sector, interest_rate_and_ltv, interest_rate_and_ltv_regression, lnr_mlnr_flnr_updated2013.dta, planner_welfare, planner_welfare.xlsx, sum_stats_stocks_1993, sum_stats_welfare_1994, sum_stats_welfare_total_diff_xi_10_1994, sum_stats_welfare_total_diff_xi_5_1994, table10788, welfare_cohort_xi_0, welfare_cohort_xi_10, welfare_cohort_xi_5, welfare_effect_decompose_100, welfare_revgain_sc_heatmap_5_1994, wrds_ws_company.dta, wrds_ws_funda.dta, year_cohort, year_cohort_percentile, year_mean_ltv.
- Links found: 0; checked: no.
