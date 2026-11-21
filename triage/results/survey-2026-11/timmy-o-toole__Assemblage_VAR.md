# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/timmy-o-toole__Assemblage_VAR` at commit `199c5f8c432c9571e601ce68ada49ab3d1819e55`
- Triaged: 2026-11-21T18:16:38Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.072 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 6 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads DescTools, NlcOptim, RJDemetra, ggh4x, ggplot2, ggthemes, p, ragg, readxl, scales, systemfonts, vars, zoo with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `code/00_prepare_data.R:20`, `code/02_irf_bands.R:18`, `code/05b_figures_bootstrap.R:9`, `code/06_summary_numbers.R:27`, `code/funcs/fig_series_weights.R:19`
- **MISSING_INPUT_DOWNLOAD**: `2025-12-md.csv` is not in the package; the documentation (data/README.md, data/raw/README.md) says to download it from https://actuariesclimateindex.org, https://actuariesclimateindex.org/terms-of-use/, https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `code/00_prepare_data.R:221`, `https://actuariesclimateindex.org`, `https://actuariesclimateindex.org/terms-of-use/`, `https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions`
- **MISSING_INPUT_DOWNLOAD**: `ACI_Data_Site.xlsx` is not in the package; the documentation (data/raw/README.md) says to download it from https://www.stlouisfed.org/research/economists/mccracken/fred-databases, https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/monthly/2025-12-md.csv, https://www.atlantafed.org/research-and-data/data/wu-xia-shadow-federal-funds-rate. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `code/00_prepare_data.R:90`, `https://www.stlouisfed.org/research/economists/mccracken/fred-databases`, `https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/monthly/2025-12-md.csv`, `https://www.atlantafed.org/research-and-data/data/wu-xia-shadow-federal-funds-rate`
- **MISSING_INPUT_DOWNLOAD**: `noaa_macrobond_export.xlsx` is not in the package; the documentation (data/raw/README.md) says to download it from https://www.stlouisfed.org/research/economists/mccracken/fred-databases, https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/monthly/2025-12-md.csv, https://www.atlantafed.org/research-and-data/data/wu-xia-shadow-federal-funds-rate. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `code/00_prepare_data.R:127`, `https://www.stlouisfed.org/research/economists/mccracken/fred-databases`, `https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/monthly/2025-12-md.csv`, `https://www.atlantafed.org/research-and-data/data/wu-xia-shadow-federal-funds-rate`
- **MISSING_INPUT_DOWNLOAD**: `WuXiaShadowRate.xlsx` is not in the package; the documentation (data/README.md, data/raw/README.md) says to download it from https://actuariesclimateindex.org, https://actuariesclimateindex.org/terms-of-use/, https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `code/00_prepare_data.R:229`, `https://actuariesclimateindex.org`, `https://actuariesclimateindex.org/terms-of-use/`, `https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions`
- **LONG_COMPUTE**: The documentation claims a run time of about 422640 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **UNRESOLVED_PATHS**: 5 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/02_irf_bands.R:37`, `code/04b_figures_series_weights.R:28`, `code/05b_figures_bootstrap.R:50`, `code/06_summary_numbers.R:48`, `config.R:127`
- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("confidential") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.

## What triage looked at

- 78 files, 163,251,853 bytes. Languages: r (24), shell (2).
- Documentation read: README.md, code/README.md, code/slurm_helper/README.md, data/README.md, data/raw/README.md, results/README.md. Licences named: CC0, MIT.
- Master scripts: code/00_prepare_data.R, code/01_estimate_weights.R, code/02_irf_bands.R, code/03_bootstrap_weights.R, code/04a_figures_irf.R, code/04b_figures_series_weights.R, code/05a_figures_irfboot.R, code/05b_figures_bootstrap.R, code/06_summary_numbers.R, run_all.R.
- File reads traced: 62; writes: 2; unresolved paths: 5; missing: 2025-12-md.csv, aci_data_site.xlsx, noaa_macrobond_export.xlsx, wuxiashadowrate.xlsx.
- Links found: 16; checked: no.
