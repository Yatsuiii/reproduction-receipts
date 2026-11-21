# Triage verdict: BLOCKED

- Package: `https://github.com/CMK-EEC-Food/JDE_replication` at commit `4616a49bfa67aab2cfba215f80bcf914d1043651`
- Triaged: 2026-11-21T10:23:24Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.819 s of analysis
- Triage script: `triage.py` SHA-256 `42fe3acc44ecb384ba61c190862dd5f58ac33d0d2e15650289c1fc23359b63f6`; options: --have matlab,stata --check-links
- 17 blockers, 2 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `R/processed_data/afr_cty_admin2_missingSPEI.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/analysis_fs.R:180`
- **MISSING_INPUT_UNDOCUMENTED**: `R/processed_data/AFR_tradepattern_qty_ddat_y_dt.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/descriptive_statistics.R:18`, `R/process_combine_adm2_fs.R:63`
- **MISSING_INPUT_UNDOCUMENTED**: `R/processed_data/AFR_tradepattern_value_ddat_y_dt.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_combine_adm2_fs.R:64`
- **MISSING_INPUT_UNDOCUMENTED**: `R/output/data_fs_cc_trade_ym_adm2.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/prepare_analysis_fs.R:8`
- **MISSING_INPUT_UNDOCUMENTED**: `R/output/data_fs_cc_trade_ym_adm2_processed.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/analysis_fs.R:177`
- **MISSING_INPUT_UNDOCUMENTED**: `data/FEWSNET/Grids/df_grid_clean_wtgeom_2021-08-16.Rdata` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_fs.R:69`
- **MISSING_INPUT_UNDOCUMENTED**: `data/ILOSTAT/EMP_2EMP_SEX_GEO_ECO_NB_A_EN_sel.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_control.R:693`
- **MISSING_INPUT_UNDOCUMENTED**: `R/output/FEWS_mapping_prices_market_admin2.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/parameterize_scenarios.R:54`
- **MISSING_INPUT_UNDOCUMENTED**: `data/prices/FEWS_NET_Staple_Food_Price_Data.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_fp.R:95`
- **MISSING_INPUT_UNDOCUMENTED**: `R/output/FPMA_mapping_prices_market_admin2.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/parameterize_scenarios.R:55`
- **MISSING_INPUT_UNDOCUMENTED**: `R/output/FS_id_geo_sample_AEZall.RData` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/analysis_spatialcorrelation.R:44`, `R/parameterize_scenarios.R:31`
- **MISSING_INPUT_UNDOCUMENTED**: `data/GADM/gadm36_1.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_spatialunit.R:11`
- **MISSING_INPUT_UNDOCUMENTED**: `data/GADM/gadm36_2.shp` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_spatialunit.R:12`
- **MISSING_INPUT_UNDOCUMENTED**: `R/processed_data/GEDEvent_AFR_dt_adm2_ym.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_combine_adm2_fs.R:65`
- **MISSING_INPUT_UNDOCUMENTED**: `data/UCDP/GEDEvent_v21_1.rdata` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/process_control.R:63`
- **MISSING_INPUT_UNDOCUMENTED**: `/etc/redhat-release` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `renv/activate.R:923`
- **MISSING_INPUT_UNDOCUMENTED**: `R/processed_data/spei_3m_adm2_share_ym_gs_dt.Rda` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `R/analysis_spatialcorrelation.R:215`, `R/descriptive_statistics.R:13`, `R/prepare_analysis_fs.R:110`

## Deviations a rerun would have to log

- **UNDECLARED_DEPENDENCIES**: R code loads libpath, project, version, which renv.lock does not pin.
  Evidence: `renv.lock`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (WDI). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `R/process_trade.R:1110`

## Notes

- **DEAD_LINK**: 2 other links answered with an HTTP error: https://api.github.com/repos/rstudio/renv/tarball (403), https://github.com/rstudio/renv/issues (403).
  Evidence: `https://api.github.com/repos/rstudio/renv/tarball`, `https://github.com/rstudio/renv/issues`
- **LINK_UNREACHABLE**: 19 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `https://hal.inrae.fr/hal-04497903`, `https://doi.org/10.1016/j.jdeveco.2026.103761`, `https://www.cepii.fr/DATA_DOWNLOAD/baci/doc/baci_webpage.html#download-links`, `https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LMSYG5`, `https://gadm.org/old_versions.html`, `https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-adjusted-to-2015-unwpp-country-totals-rev11`, `https://www.ifpri.org/publication/agro-ecological-zones-africa-south-sahara`, `https://doi.org/10.7910/DVN/M7XIUB`, `https://ilostat.ilo.org/topics/employment/#elementor-toc__heading-anchor-1`, `https://figshare.com/articles/dataset/Travel_time_to_cities_and_ports_in_the_year_2015/7638134`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 69 files, 13,384,503 bytes. Languages: r (24).
- Documentation read: data_sources.md, readme.md, workflow.md. Licences named: none.
- Master scripts: none.
- File reads traced: 65; writes: 73; unresolved paths: 0; missing: afr_cty_admin2_missingspei.rda, afr_tradepattern_qty_ddat_y_dt.rda, afr_tradepattern_value_ddat_y_dt.rda, data_fs_cc_trade_ym_adm2.rda, data_fs_cc_trade_ym_adm2_processed.rda, df_grid_clean_wtgeom_2021-08-16.rdata, emp_2emp_sex_geo_eco_nb_a_en_sel.csv, fews_mapping_prices_market_admin2.rda, fews_net_staple_food_price_data.csv, fpma_mapping_prices_market_admin2.rda, fs_id_geo_sample_aezall.rdata, gadm36_1.shp, gadm36_2.shp, gedevent_afr_dt_adm2_ym.rda, gedevent_v21_1.rdata, redhat-release, spei_3m_adm2_share_ym_gs_dt.rda.
- Links found: 21; checked: yes.
  - http://dx.doi.org/10.5285/bbdfd09a04304158b366777eba0d2aeb: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://api.github.com/repos/rstudio/renv/tarball: FAILED (403)
  - https://apps.fas.usda.gov/psdonline/app/index.html#/app/downloads: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://catalogue.ceda.ac.uk/uuid/bbdfd09a04304158b366777eba0d2aeb: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://catalogue.ceda.ac.uk/uuid/bbdfd09a04304158b366777eba0d2aeb/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://cloud.r-project.org: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LMSYG5: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://doi.org/10.1016/j.jdeveco.2026.103761: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://doi.org/10.7910/DVN/M7XIUB: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://fews.net/fews-data/337: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://figshare.com/articles/dataset/Travel_time_to_cities_and_ports_in_the_year_2015/7638134: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://fpma.apps.fao.org/giews/food-prices/tool/public/#/dataset/domestic: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://gadm.org/old_versions.html: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://github.com/rstudio/renv/issues: FAILED (403)
  - https://hal.inrae.fr/hal-04497903: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://ilostat.ilo.org/topics/employment/#elementor-toc__heading-anchor-1: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://msi.nga.mil/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-adjusted-to-2015-unwpp-country-totals-rev11: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://ucdp.uu.se/downloads/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.cepii.fr/DATA_DOWNLOAD/baci/doc/baci_webpage.html#download-links: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.ifpri.org/publication/agro-ecological-zones-africa-south-sahara: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
