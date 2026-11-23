# Triage verdict: BLOCKED

- Package: `pkgs/johanneswieland__MPC2001` at commit `15a801cc5d4acae71a9956c52a016d5bb510f644`
- Triaged: 2026-11-21T18:16:35Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.309 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 2 blockers, 19 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `../input/fmli.parquet` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `createconsumptionvariables/code/sumFMLIquarterlyconsumption.py:9`
- **MISSING_INPUT_UNDOCUMENTED**: `../input/mtbi.parquet` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `createconsumptionvariables/code/create_new_UCC.py:12`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **UNDECLARED_DEPENDENCIES**: Python code imports cycler, which no dependency file names.
  Evidence: `appendCEXfiles/code/appendCEXfiles.py`, `checkforsmoothing/code/checkforsmoothing.py`, `createconsumptionvariables/code/aggregateMTBIucc.py`, `createconsumptionvariables/code/aggregateMTBIucc_smallmemory.py`, `createconsumptionvariables/code/aggregation_labels.py`
- **STATA_NETWORK_INSTALL**: Do-files install did_imputation from the network at run time, with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.
  Evidence: `psmjregressions/code/variablelabels.do:1`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/agglabels_levelnames_nipa.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjregressions/code/Table2001_bea_all.do:68`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/agglabelsnipa.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjregressions/code/Table2001_bea_all.do:67`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/agglabelspsmj.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjregressions/code/Table2001_bea_all.do:70`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/mtbimonthly.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `checkforsmoothing/code/checkforsmoothing.py:9`, `psmjvariables/code/psmjexpenditures.py:13`, `psmjvariables/code/psmjexpenditures.py:17`, `testingconsumptionaggregation/code/testingaggregation.py:9`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/pceexpenditure.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `jpsexpenditure/code/jpsexpenditure.py:12`, `jpsexpenditure/code/jpsexpenditure.py:36`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/pceexpenditureprice.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `jpsexpenditure/code/jpsexpenditure.py:35`
- **MISSING_INPUT_SOURCE_LISTED**: `../output/psmjexpendituresinterview.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjvariables/code/psmjexpenditures.py:120`
- **MISSING_INPUT_SOURCE_LISTED**: `../output/psmjexpendituresmonthly.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjvariables/code/psmjexpenditures.py:117`
- **MISSING_INPUT_SOURCE_LISTED**: `../output/psmjsampleinterview_wlabels.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjregressions/code/Table2001_aggdef.do:27`, `psmjregressions/code/Table2001_bea_all.do:8`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/psmjvariablesinterview.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjsample/code/psmjsample.py:15`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/psmjvariablesmonthly.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `psmjsample/code/psmjsample.py:118`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/rebate2001cuid.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `nipavariables/code/nipamergedata.py:21`, `psmjvariables/code/psmjmergedata.py:28`
- **MISSING_INPUT_SOURCE_LISTED**: `../input/TAX.parquet` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `processrebatemodule/code/rebate2001.py:18`
- **MISSING_INPUT_SOURCE_LISTED**: `../output/testirfs.csv` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `model/code/nk_rebates_mpc_model.py:407`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (import fred, requests.get). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `downloaddata/code/pcefromBEA.py:40`, `downloaddata/code/pull_pce_detail.py:36`, `survey_prof_fore/code/pull_SPF.py:18`, `forecasting/code/build_forecast_data.do:34`, `forecasting/code/build_forecast_data.do:69`, `narrative/code/build_narrative_data.do:42`, `survey_prof_fore/code/graph_SPF_cons_dist.do:15`
- **ABSOLUTE_PATH**: 2 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `model/code/nk_rebates_mpc_plot2001.py:364`, `model/code/tables.py:30`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `forecasting/code/build_forecast_data.do`, `forecasting/code/forecast2001.do`, `narrative/code/build_narrative_data.do`, `narrative/code/narrative_graphs.do`, `psmjregressions/code/Table2001_aggdef.do`
- **UNRESOLVED_PATHS**: 17 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `forecasting/code/build_forecast_data.do:76`, `forecasting/code/build_forecast_data.do:176`, `narrative/code/build_narrative_data.do:52`, `nipavariables/code/nipaexpenditures.py:26`, `nipavariables/code/nipamergedata.py:31`, `nipavariables/code/nipamergedata.py:34`, `processrebatemodule/code/rebate2001.py:46`, `processrebatemodule/code/rebate2001.py:49`, `psmjregressions/code/Table2001_bea_all.do:77`, `psmjregressions/code/Table2001_bea_all.do:90`
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE`, `license_sss`

## What triage looked at

- 116 files, 87,134,371 bytes. Languages: python (41), shell (3), stata (8).
- Documentation read: README.md. Licences named: CC BY-NC, CC0, BSD, GPL.
- Master scripts: none.
- File reads traced: 73; writes: 66; unresolved paths: 17; missing: agglabels_levelnames_nipa.dta, agglabelsnipa.dta, agglabelspsmj.dta, fmli.parquet, mtbi.parquet, mtbimonthly.parquet, pceexpenditure.parquet, pceexpenditureprice.parquet, psmjexpendituresinterview.parquet, psmjexpendituresmonthly.parquet, psmjsampleinterview_wlabels.dta, psmjvariablesinterview.parquet, psmjvariablesmonthly.parquet, rebate2001cuid.parquet, tax.parquet, testirfs.csv.
- Links found: 6; checked: no.
