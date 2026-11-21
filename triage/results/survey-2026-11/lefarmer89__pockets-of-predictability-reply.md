# Triage verdict: BLOCKED

- Package: `pkgs/lefarmer89__pockets-of-predictability-reply` at commit `22c6be1295b898a9ad9b963f1061cac6e6fcfb7c`
- Triaged: 2026-11-21T18:16:39Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.106 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 3 blockers, 15 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `pcPredictor.mat` is read by the code and named in the documentation (MAT_ARCHIVE.md, README.md), but it is not in the package and no source for it is given.
  Evidence: `dailyEmpirics.m:69`, `dailyEmpiricsHyperparameters1.m:38`, `subroutines/forecasting/selectPredictor.m:30`
- **MISSING_INPUT_UNDOCUMENTED**: `simulatedPaths.mat` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `stickyExpectationsSim.m:58`
- **MISSING_INPUT_UNDOCUMENTED**: `results/aggregates/topKbotK.mat` is read by the code and named in the documentation (README.md, tests/VERIFICATION.md), but it is not in the package and no source for it is given.
  Evidence: `figures/figure1.m:11`, `figures/figureA1.m:10`, `figures/figureA2.m:10`, `figures/figureA3.m:9`

## Deviations a rerun would have to log

- **MISSING_INPUT_SOURCE_LISTED**: `forecastResults_1_2.5yE_1yDM_1S_pm.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `figures/figure2.m:15`, `subroutines/bootstrap/computeSignifCell.m:24`, `tables/table2.m:14`
- **MISSING_INPUT_SOURCE_LISTED**: `forecastResults_2_2.5yE_1yDM_1S_pm_HyperR1.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `subroutines/hyperparameters/adaptivePanelsForSplit.m:67`
- **MISSING_INPUT_SOURCE_LISTED**: `forecastResultsMonthly_1_2.5yE_1yDM_1S_pm.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/tableA5.m:11`
- **MISSING_INPUT_SOURCE_LISTED**: `integralR2.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `subroutines/bootstrap/computeSignifCell.m:36`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResults_1_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/table3.m:23`, `tables/table4.m:17`
- **MISSING_INPUT_SOURCE_LISTED**: `daily/OOSResults_2_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `subroutines/hyperparameters/computeTab1Results.m:34`, `subroutines/hyperparameters/computeTabA3Results.m:74`, `tables/table3.m:28`, `tables/tableA1.m:24`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResults_2_HyperR1_ExpandingC.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `subroutines/hyperparameters/adaptivePanelsForSplit.m:124`, `subroutines/hyperparameters/adaptivePanelsForSplit.m:127`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResults_3_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/table3.m:33`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResultsHML_1_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/tableA4.m:20`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResultsMonthly_1_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/tableA6.m:16`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResultsMonthly_2_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/tableA6.m:21`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResultsMonthly_3_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/tableA6.m:26`
- **MISSING_INPUT_SOURCE_LISTED**: `OOSResultsSMB_1_2.5yE_1yDM.mat` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `tables/tableA4.m:15`
- **MISSING_INPUT_SOURCE_LISTED**: `W_sim.csv` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (MAT_ARCHIVE.md: 3 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `dailyAssetPricingBootstrap.m:68`
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `subroutines/io/prettifyLatexTable.m:45`, `subroutines/io/prettifyLatexTable.m:46`, `subroutines/io/prettifyLatexTable.m:47`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `PathSimulator.m`, `dailyAssetPricingBootstrap.m`, `dailyBootstrap.m`, `dailyEmpirics.m`, `dailyEmpiricsGPriorRobustness.m`
- **UNRESOLVED_PATHS**: 9 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `dailyAssetPricingBootstrap.m:71`, `dailyEmpiricsHyperparametersMarginals.m:268`, `dailyEmpiricsHyperparametersMarginals.m:269`, `subroutines/hyperparameters/computeTabA3Results.m:89`, `subroutines/io/saveTableScript.m:20`, `subroutines/io/splitDataPanels.m:61`, `tables/table4.m:26`, `tables/table5.m:24`, `tables/tableA2.m:23`
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: Machine Learning Toolbox, Parallel Computing Toolbox. Each is licensed separately; check the desk's MATLAB has them.

## What triage looked at

- 94 files, 4,665,083 bytes. Languages: matlab (83).
- Documentation read: MAT_ARCHIVE.md, README.md, tests/VERIFICATION.md. Licences named: MIT.
- Master scripts: runAll.m.
- File reads traced: 49; writes: 26; unresolved paths: 9; missing: forecastresults_1_2.5ye_1ydm_1s_pm.mat, forecastresults_2_2.5ye_1ydm_1s_pm_hyperr1.mat, forecastresultsmonthly_1_2.5ye_1ydm_1s_pm.mat, integralr2.mat, oosresults_1_2.5ye_1ydm.mat, oosresults_2_2.5ye_1ydm.mat, oosresults_2_hyperr1_expandingc.mat, oosresults_3_2.5ye_1ydm.mat, oosresultshml_1_2.5ye_1ydm.mat, oosresultsmonthly_1_2.5ye_1ydm.mat, oosresultsmonthly_2_2.5ye_1ydm.mat, oosresultsmonthly_3_2.5ye_1ydm.mat, oosresultssmb_1_2.5ye_1ydm.mat, pcpredictor.mat, simulatedpaths.mat, topkbotk.mat, w_sim.csv.
- Links found: 3; checked: no.
