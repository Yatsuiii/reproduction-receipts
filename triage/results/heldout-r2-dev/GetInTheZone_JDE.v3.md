# Triage verdict: BLOCKED

- Package: `https://github.com/Ellakirchner/GetInTheZone_JDE` at commit `cf696bc1d756df185fca391933326fd3fb06b7b0`
- Triaged: 2026-11-21T12:11:31Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.064 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 4 blockers, 2 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `ggsave_latex.R` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("cannot be shared"), so it is most likely one of those.
  Evidence: `06_calcCE.R:74`
- **MISSING_INPUT_RESTRICTED**: `datasets/heatmap_cost0.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("cannot be shared"), so it is most likely one of those.
  Evidence: `06_calcCE.R:1422`
- **MISSING_INPUT_RESTRICTED**: `datasets/heatmap_cost10.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("cannot be shared"), so it is most likely one of those.
  Evidence: `06_calcCE.R:1423`
- **MISSING_INPUT_RESTRICTED**: `datasets/heatmap_cost10_nodesignrisk.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("cannot be shared"), so it is most likely one of those.
  Evidence: `06_calcCE.R:1424`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads ClustGeo, PerformanceAnalytics, RColorBrewer, aricode, caret, chron, cowplot, doParallel, dplyr, dtplyr, furrr, future, geodata, geojsonsf, ggpattern, ggplot2, ggpubr, ggspatial, gridExtra, gtable, janitor, lubridate, mclust, ncdf4, palmerpenguins, patchwork, proxy, purrr, randomForest, scales, sf, sp, spdep, stringr, summarytools, terra, tictoc, tidylog, tidyr, tidyverse, writexl, xgboost, xtable, zoo with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `01_prepData.R:50`, `01_prepData.R:51`, `01_prepData.R:52`, `01_prepData.R:53`, `01_prepData.R:54`
- **EXTERNAL_SERVICE**: A step runs in Google Earth Engine, which needs an account and exports through Google Drive. Its outputs are inputs to later steps; a receipt must record the export date and hash, because the hosted image collections change.
  Evidence: `00_extract_data_gee.js`

## Notes

- **UNRESOLVED_PATHS**: 1 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `01_prepData.R:104`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 13 files, 5,426,763 bytes. Languages: earthengine (1), r (6).
- Documentation read: README.md. Licences named: none.
- Master scripts: 01_prepData.R, 02_predictYields.R, 03_mergeCluster.R, 04_calcDescriptives.R, 05_mapROI.R, 06_calcCE.R.
- File reads traced: 42; writes: 91; unresolved paths: 1; missing: ggsave_latex.r, heatmap_cost0.csv, heatmap_cost10.csv, heatmap_cost10_nodesignrisk.csv.
- Links found: 0; checked: yes.
