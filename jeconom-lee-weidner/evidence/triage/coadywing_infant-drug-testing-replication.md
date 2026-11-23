# Triage verdict: BLOCKED

- Package: `pk/coadywing_infant-drug-testing-replication` at commit `fffbd14b587e945dd59fcaf2ad28bfe3b00f7892`
- Triaged: 2026-11-23T17:48:00Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.068 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 14 blockers, 3 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `covid_labs.sas7bdat.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/26.appendix_figure_covid.r:26`
- **MISSING_INPUT_RESTRICTED**: `demo.sas7bdat.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/02.check_data.r:34`, `code/03.build_cohort.r:23`, `code/26.appendix_figure_covid.r:46`
- **MISSING_INPUT_RESTRICTED**: `dx.sas7bdat.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/10.create_mom_cpd_sud_preec_file.r:35`, `code/13.add_infant_characteristics.r:31`
- **MISSING_INPUT_UNDOCUMENTED**: `encounter.sas7bdat.csv` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `code/10.create_mom_cpd_sud_preec_file.r:29`, `code/11.merge_insurance.r:36`, `code/13.add_infant_characteristics.r:25`
- **MISSING_INPUT_RESTRICTED**: `IN_SID_2018.csv` is read by the code but is not in the package, and the documentation (README.md) describes it as restricted ("data use agreement"). The desk cannot run this without access.
  Evidence: `code/hcup_sid/nas_infant_drugs.r:19`
- **MISSING_INPUT_RESTRICTED**: `IN_SID_2019.csv` is read by the code but is not in the package, and the documentation (README.md) describes it as restricted ("data use agreement"). The desk cannot run this without access.
  Evidence: `code/hcup_sid/nas_infant_drugs.r:16`
- **MISSING_INPUT_UNDOCUMENTED**: `insurance.sas7bdat.csv` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `code/11.merge_insurance.r:30`
- **MISSING_INPUT_RESTRICTED**: `lab_Moms_2019.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/33.mom_drug_testing_file.r:18`
- **MISSING_INPUT_RESTRICTED**: `lab_Moms_2020.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/33.mom_drug_testing_file.r:19`
- **MISSING_INPUT_RESTRICTED**: `lab_Moms_2021.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/33.mom_drug_testing_file.r:20`
- **MISSING_INPUT_RESTRICTED**: `lab_Moms_2022.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/33.mom_drug_testing_file.r:21`
- **MISSING_INPUT_RESTRICTED**: `lab_Moms_2023.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/33.mom_drug_testing_file.r:22`
- **MISSING_INPUT_UNDOCUMENTED**: `rdrp5665_baby_matched_fnl.sas7bdat` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `code/01.convert_natality_linked.r:21`
- **MISSING_INPUT_UNDOCUMENTED**: `rdrp5665_mom_matched_fnl.sas7bdat` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `code/01.convert_natality_linked.r:20`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads DBI, boot, collapse, data.table, dplyr, duckdb, fixest, fst, ggplot2, glue, gridExtra, gtsummary, haven, here, kableExtra, lubridate, modelsummary, pacman, pbapply, readr, readxl, rmarkdown, stringr, survey, tableone, tidyverse, vroom, vtable, xtable, zctaCrosswalk with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `code/01.convert_natality_linked.r:10`, `code/01.convert_natality_linked.r:12`, `code/02.check_data.r:10`, `code/02.check_data.r:12`, `code/03.build_cohort.r:10`
- **MISSING_INPUT_REGISTRATION**: `data/inputs/GroupLoincTerms.csv` is not in the package; the documentation (data/inputs/README.md) says it comes from a source that needs registration ("free account"). The desk must register, download and log the extract.
  Evidence: `code/31.find_drug_codes_mom.r:15`
- **MISSING_INPUT_REGISTRATION**: `data/inputs/ZIP_COUNTY_122023.csv` is not in the package; the documentation (data/inputs/README.md) says it comes from a source that needs registration ("free account"). The desk must register, download and log the extract.
  Evidence: `code/08.merge_county_crosswalk.r:18`, `code/14.merge_cnty_nas.r:25`, `code/26.appendix_figure_covid.r:67`

## Notes

- **UNRESOLVED_PATHS**: 1 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/nvss_code/infant_summary_in.r:19`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 133 files, 858,839 bytes. Languages: r (39).
- Documentation read: FILE_PIPELINE.md, README.md, data/inputs/README.md, data/outputs/README.md. Licences named: none.
- Master scripts: code/00_paths.r, code/main.R.
- File reads traced: 117; writes: 70; unresolved paths: 1; missing: covid_labs.sas7bdat.csv, demo.sas7bdat.csv, dx.sas7bdat.csv, encounter.sas7bdat.csv, grouploincterms.csv, in_sid_2018.csv, in_sid_2019.csv, insurance.sas7bdat.csv, lab_moms_2019.csv, lab_moms_2020.csv, lab_moms_2021.csv, lab_moms_2022.csv, lab_moms_2023.csv, rdrp5665_baby_matched_fnl.sas7bdat, rdrp5665_mom_matched_fnl.sas7bdat, zip_county_122023.csv.
- Links found: 7; checked: no.
