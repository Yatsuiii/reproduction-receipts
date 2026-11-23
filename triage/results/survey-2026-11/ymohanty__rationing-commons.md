# Triage verdict: BLOCKED

- Package: `pkgs/ymohanty__rationing-commons` at commit `4d60ad2f8d12ced60106c70649d8984b8d97bce0`
- Triaged: 2026-11-21T18:16:40Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.244 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 8 blockers, 6 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `95feindiamap_state.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/maps/ration_states_map.R:74`
- **MISSING_INPUT_UNDOCUMENTED**: `baseline_survey.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/cleaning/farmer_survey/build_farmer_crop_data.do:42`
- **MISSING_INPUT_UNDOCUMENTED**: `d4_kotputli_mundawar_bansur/KOTPUTLI, MANDAWAR & BUNSUR BLOCK VECTOR/FRACTURE_LINEAMENT.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/cleaning/geology/build_geological_variables.R:103`, `code/cleaning/geology/build_geological_variables.R:107`, `code/cleaning/geology/build_geological_variables.R:111`, `code/maps/depth_maps.R:109`, `code/maps/depth_maps.R:113`
- **MISSING_INPUT_UNDOCUMENTED**: `d4_kotputli_mundawar_bansur/KOTPUTLI, MANDAWAR & BUNSUR BLOCK VECTOR/FRACTURE_LINEAMENT_Inferred.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/cleaning/geology/build_geological_variables.R:104`, `code/cleaning/geology/build_geological_variables.R:108`, `code/cleaning/geology/build_geological_variables.R:112`, `code/maps/depth_maps.R:110`, `code/maps/depth_maps.R:114`
- **MISSING_INPUT_UNDOCUMENTED**: `d2_dug/GANGDHAR BLOCK VECTOR/HYDROGEOMORPHIC_DIVISION.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/cleaning/geology/build_geological_variables.R:84`, `code/cleaning/geology/build_geological_variables.R:86`, `code/cleaning/geology/build_geological_variables.R:88`, `code/maps/depth_maps.R:90`, `code/maps/depth_maps.R:92`
- **MISSING_INPUT_UNDOCUMENTED**: `prediction.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/maps/depth_maps.R:211`
- **MISSING_INPUT_UNDOCUMENTED**: `project_root.txt` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/structural_analysis/rationing_main.m:16`
- **MISSING_INPUT_UNDOCUMENTED**: `telangana_shapefile.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/maps/ration_states_map.R:80`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: - pandas; - numpy; - openpyxl. A rerun installs whatever is current and must log the versions it got.
  Evidence: `code/environment.yml`
- **UNDECLARED_DEPENDENCIES**: Python code imports matplotlib, which no dependency file names.
  Evidence: `code/cleaning/pending_consumers/clean_consumer_data.py`, `code/cleaning/pending_consumers/clean_pending_consumers_data.ipynb`, `code/cleaning/soil/clean_soil_data.py`
- **UNPINNED_DEPENDENCIES**: R code loads FNN, GISTools, RColorBrewer, checkpoint, crop, dplyr, extrafont, foreign, fuzzyjoin, ggsn, gridExtra, gstat, lubridate, maptools, ncdf4, plm, plyr, raster, readstata13, readxl, rgdal, rlist, sf, sp, spdep, sphet, splm, stName, stplanr, tidyverse, tmap, tmaptools, waterfalls with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `code/cleaning/farmer_survey/water_flow.R:33`, `code/cleaning/farmer_survey/water_flow.R:46`, `code/cleaning/farmer_survey/water_flow.R:50`, `code/cleaning/farmer_survey/water_flow.R:51`, `code/cleaning/farmer_survey/water_flow.R:52`
- **MISSING_INPUT_DOWNLOAD**: `\t` is not in the package; the documentation (README.md, code/structural_analysis/panel_data_toolbox/README.md, code/structural_analysis/panel_data_toolbox/readme.txt) says to download it from https://github.com/ymohanty/rationing_the_commons.git, http://www.paneldatatoolbox.com, http://dx.doi.org/10.18637/jss.v076.i06. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `code/structural_analysis/@waterData/waterData.m:55`, `https://github.com/ymohanty/rationing_the_commons.git`, `http://www.paneldatatoolbox.com`, `http://dx.doi.org/10.18637/jss.v076.i06`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (webuse). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `code/structural_analysis/panel_data_toolbox/unittests/ut_IV2SLS.do:7`, `code/structural_analysis/panel_data_toolbox/unittests/ut_OLS.do:7`, `code/structural_analysis/panel_data_toolbox/unittests/ut_PANEL.do:7`
- **ABSOLUTE_PATH**: 51 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `code/cleaning/farmer_survey/build_farmer_crop_data.do:23`, `code/cleaning/farmer_survey/build_farmer_crop_data.do:24`, `code/cleaning/farmer_survey/build_farmer_crop_data.do:27`, `code/cleaning/farmer_survey/build_farmer_crop_data.do:28`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:17`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:18`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:21`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:22`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:1631`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:1632`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `code/structural_analysis/@gmm/gmm.m`, `code/structural_analysis/@waterCounter/findOptimalTransfers.m`, `code/structural_analysis/@waterCounter/plotFit.m`, `code/structural_analysis/@waterCounter/plotOptimalTransfers.m`, `code/structural_analysis/@waterCounter/plotShadowValue.m`
- **SOFTWARE_REQUIRED**: Requires Stata (version 11, 15, 6.0, 9.2 named in code); the desk says it has it.
  Evidence: `code/ado/LASSO_~1.ADO`, `code/ado/_ivreg.ado`, `code/ado/_lasso_iv.ado`, `code/ado/_lasso_iv_first.ado`, `code/ado/_reg_ols.ado`
- **UNRESOLVED_PATHS**: 57 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/cleaning/farmer_survey/build_farmer_crop_data.do:33`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:26`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:38`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:52`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:80`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:1640`, `code/cleaning/farmer_survey/impute_profits_farmer_crop.do:1641`, `code/cleaning/farmer_survey/rationing_dynamics_data.do:24`, `code/cleaning/farmer_survey/rationing_dynamics_data.do:29`, `code/cleaning/farmer_survey/rationing_dynamics_data.do:127`
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: Panel Data Toolbox. Each is licensed separately; check the desk's MATLAB has them.

## What triage looked at

- 321 files, 2,150,811 bytes. Languages: matlab (126), python (3), r (14), shell (1), stata (36).
- Documentation read: README.md, code/structural_analysis/panel_data_toolbox/README.md, code/structural_analysis/panel_data_toolbox/readme.txt. Licences named: GPL.
- Master scripts: code/main.sh, code/structural_analysis/panel_data_toolbox/paneldata/util/replicate_elements.m.
- File reads traced: 107; writes: 141; unresolved paths: 57; missing: 95feindiamap_state.shp, baseline_survey.dta, fracture_lineament.shp, fracture_lineament_inferred.shp, hydrogeomorphic_division.shp, prediction.csv, project_root.txt, t, telangana_shapefile.shp.
- Links found: 6; checked: no.
