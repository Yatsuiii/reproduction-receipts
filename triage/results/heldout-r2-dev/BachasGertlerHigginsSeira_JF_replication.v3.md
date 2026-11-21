# Triage verdict: BLOCKED

- Package: `https://github.com/skhiggins/BachasGertlerHigginsSeira_JF_replication` at commit `bf71158ff85e148ac8e6d4b6b44258d2f7625026`
- Triaged: 2026-11-21T12:11:19Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 1.071 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 31 blockers, 14 deviations, 6 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `$data/Prospera/1. Modelo_Urbano_263-Locs.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/57_iter_locality_dataprep.do:31`
- **MISSING_INPUT_RESTRICTED**: `$proc/bansefi_baseline.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/18_withdrawals_dataprep.do:175`, `scripts/20_savings_event_dataprep.do:100`
- **MISSING_INPUT_RESTRICTED**: `data/BDU/bdu_actual_sean.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/38_bdu_hist_dataprep.R:33`
- **MISSING_INPUT_RESTRICTED**: `proc/bdu_cp_month_means_new.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/43_bdu_allgiro_month.R:30`
- **MISSING_INPUT_RESTRICTED**: `proc/bdu_fake.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/38_bdu_hist_dataprep.R:59`
- **MISSING_INPUT_RESTRICTED**: `data/BDU/bdu_historico_sean.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/37_bdu_hist_read.R:16`
- **MISSING_INPUT_RESTRICTED**: `data/BDU/cat_movimientos.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/37_bdu_hist_read.R:108`
- **MISSING_INPUT_RESTRICTED**: `data/SEPOMEX/CPdescarga.txt` is read by the code but is not in the package, and the documentation (README.md, README.txt) describes it as restricted ("administrative data"). The desk cannot run this without access.
  Evidence: `scripts/36_cp_municipio.R:15`
- **MISSING_INPUT_RESTRICTED**: `data/INE/elecciones_long.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/53_elections_dataprep.R:21`
- **MISSING_INPUT_RESTRICTED**: `$proc/encel09_hh.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/63_encelurb_merge.do:36`
- **MISSING_INPUT_RESTRICTED**: `$proc/encel_forreg_permutations.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/64_encelurb_reg_dataprep.do:167`
- **MISSING_INPUT_RESTRICTED**: `$data/Prospera/Transfers/Encel_sample/encelurb_trans_2002_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/63_encelurb_merge.do:249`
- **MISSING_INPUT_RESTRICTED**: `$proc/entrevistas_educacion_noviembre_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/74_encasdu_dataprep.do:199`, `scripts/74_encasdu_dataprep.do:846`
- **MISSING_INPUT_RESTRICTED**: `$proc/entrevistas_mapo_noviembre_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/74_encasdu_dataprep.do:86`, `scripts/74_encasdu_dataprep.do:824`
- **MISSING_INPUT_RESTRICTED**: `data/ITER/2005/fd_iter_2005.xlsx` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/23_iter_dataprep.R:80`
- **MISSING_INPUT_RESTRICTED**: `$proc/hogar_educacion_diciembre_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/74_encasdu_dataprep.do:197`, `scripts/74_encasdu_dataprep.do:649`, `scripts/74_encasdu_dataprep.do:690`, `scripts/74_encasdu_dataprep.do:784`, `scripts/74_encasdu_dataprep.do:844`
- **MISSING_INPUT_RESTRICTED**: `$proc/hogar_mapo_noviembre_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/74_encasdu_dataprep.do:84`, `scripts/74_encasdu_dataprep.do:461`, `scripts/74_encasdu_dataprep.do:499`, `scripts/74_encasdu_dataprep.do:584`, `scripts/74_encasdu_dataprep.do:822`
- **MISSING_INPUT_RESTRICTED**: `data/CPI/INPC_02_14_Workhorse_MuniByMonth_02_14_d.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/70_cpix_read.R:41`
- **MISSING_INPUT_RESTRICTED**: `$proc/integrantes_educacion_diciembre_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/74_encasdu_dataprep.do:619`, `scripts/74_encasdu_dataprep.do:648`, `scripts/74_encasdu_dataprep.do:689`
- **MISSING_INPUT_RESTRICTED**: `$proc/integrantes_mapo_noviembre_2010.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/74_encasdu_dataprep.do:433`, `scripts/74_encasdu_dataprep.do:460`, `scripts/74_encasdu_dataprep.do:498`
- **MISSING_INPUT_RESTRICTED**: `$proc/iter05u.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/58_locality_dataprep.do:24`
- **MISSING_INPUT_RESTRICTED**: `data/ITER/2005/ITER_NALTXT05.txt` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/23_iter_dataprep.R:76`
- **MISSING_INPUT_RESTRICTED**: `data/ITER/2010/ITER_NALTXT10.TXT` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/23_iter_dataprep.R:20`
- **MISSING_INPUT_RESTRICTED**: `proc/N_withdrawals.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/104_bansefi_pre_graph.R:27`
- **MISSING_INPUT_RESTRICTED**: `proc/net_savings_ind_0_ln.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/104_bansefi_pre_graph.R:26`
- **MISSING_INPUT_RESTRICTED**: `proc/net_savings_ind_0_w5.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/104_bansefi_pre_graph.R:25`
- **MISSING_INPUT_RESTRICTED**: `$data/Bansefi/Saldos Promedio Cuentahorro.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/07_bansefi_avgbal.do:25`
- **MISSING_INPUT_RESTRICTED**: `$data/Bansefi/Saldos Promedio Debicuenta.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/07_bansefi_avgbal.do:26`
- **MISSING_INPUT_RESTRICTED**: `$proc/SP_2007.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/07_bansefi_avgbal.do:74`
- **MISSING_INPUT_RESTRICTED**: `$proc/SP_2008.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/07_bansefi_avgbal.do:75`
- **MISSING_INPUT_RESTRICTED**: `year.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `scripts/66_enoe_read.do:19`

## Deviations a rerun would have to log

- **UNDECLARED_DEPENDENCIES**: R code loads libpath, project, remotes, version, which renv.lock does not pin.
  Evidence: `renv.lock`
- **MISSING_INPUT_REGISTRATION**: `$data/comparison/Karlan_etal_2016_MgmtSci/analysis_dataallcountries.dta` is not in the package; the documentation (README.md, README.txt) says it comes from a source that needs registration ("openicpsr"). The desk must register, download and log the extract.
  Evidence: `scripts/96_comparison_figure.do:369`
- **MISSING_INPUT_REGISTRATION**: `$data/comparison/Karlan_Zinman_2017/proc/dreamfinal_for_analysis.dta` is not in the package; the documentation (README.md, README.txt) says it comes from a source that needs registration ("openicpsr"). The desk must register, download and log the extract.
  Evidence: `scripts/96_comparison_figure.do:426`
- **MISSING_INPUT_REGISTRATION**: `$data/comparison/Dupas_Robinson_2013_AER/HARP_ROSCA_final.dta` is not in the package; the documentation (README.md, README.txt) says it comes from a source that needs registration ("openicpsr"). The desk must register, download and log the extract.
  Evidence: `scripts/96_comparison_figure.do:240`
- **MISSING_INPUT_REGISTRATION**: `$data/comparison/Drexler_etal_2014_AEJApplied/kisDataFinal.dta` is not in the package; the documentation (README.md, README.txt) says it comes from a source that needs registration ("openicpsr"). The desk must register, download and log the extract.
  Evidence: `scripts/96_comparison_figure.do:167`
- **MISSING_INPUT_DOWNLOAD**: `data/MCC/mcc_codes.csv` is not in the package; the documentation (README.md, README.txt) says to download it from https://github.com/greggles/mcc-codes, https://github.com/greggles/mcc-codes. The download date and the file's SHA-256 become part of the receipt.
  Evidence: `scripts/37_bdu_hist_read.R:59`, `https://github.com/greggles/mcc-codes`, `https://github.com/greggles/mcc-codes`
- **DATA_LINK_UNVERIFIED**: The server answered https://github.com/greggles/mcc-codes with HTTP 403, https://github.com/greggles/mcc-codes with HTTP 403. That does not show the data are gone (only 404 or 410 would); it may need a login, a browser or a retry.
  Evidence: `scripts/37_bdu_hist_read.R:59`, `https://github.com/greggles/mcc-codes`, `https://github.com/greggles/mcc-codes`
- **MISSING_INPUT_DOWNLOAD**: `$data/Medios_de_Pago/medios_pago_titular_beneficiarios.dta` is not in the package; the documentation (README.md, README.txt) says to download it from https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php, https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php. The download date and the file's SHA-256 become part of the receipt.
  Evidence: `scripts/113_medios_histogram_graph.do:18`, `scripts/75_medios_de_pago_dataprep.do:52`, `https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php`, `https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php`
- **DATA_LINK_UNREACHABLE**: Could not reach https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php, https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php from this machine (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>). That is evidence about this machine's network, not about the link; check it from another network before treating the data as unavailable.
  Evidence: `scripts/113_medios_histogram_graph.do:18`, `scripts/75_medios_de_pago_dataprep.do:52`, `https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php`, `https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php`
- **MISSING_INPUT_REGISTRATION**: `$data/comparison/Prina_2015_JDE/Nepal_JDE_R1.dta` is not in the package; the documentation (README.md, README.txt) says it comes from a source that needs registration ("openicpsr"). The desk must register, download and log the extract.
  Evidence: `scripts/96_comparison_figure.do:662`
- **MISSING_INPUT_DOWNLOAD**: `$data/CONEVAL/rezago_social_localidad.dta` is not in the package; the documentation (README.md, README.txt) says to download it from https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar, https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar. The download date and the file's SHA-256 become part of the receipt.
  Evidence: `scripts/58_locality_dataprep.do:20`, `https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar`, `https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar`
- **DATA_LINK_UNREACHABLE**: Could not reach https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar, https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar from this machine (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>). That is evidence about this machine's network, not about the link; check it from another network before treating the data as unavailable.
  Evidence: `scripts/58_locality_dataprep.do:20`, `https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar`, `https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (download.file). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `renv/activate.R:76`
- **ABSOLUTE_PATH**: 9 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `adofiles/f/ftab.ado:173`, `adofiles/r/reghdfe.ado:81`, `adofiles/r/reghdfe.ado:91`, `scripts/00_run.do:18`, `scripts/00_run.do:19`, `scripts/00_run.do:20`, `scripts/77_withdrawals_event_randinf.do:22`, `scripts/78_savings_event_randinf.do:22`, `scripts/80_balance_checks_event_randinf.do:22`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata (version 10, 11, 13.1, 4.0, 5.0, 6, 7.0, 8, 8.2, 9.2 named in code); the desk says it has it.
  Evidence: `adofiles/_gbom.ado`, `adofiles/_geom.ado`, `adofiles/bimestrify.ado`, `adofiles/carryforward.ado`, `adofiles/cluster_permute.ado`
- **UNRESOLVED_PATHS**: 150 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `adofiles/f/fcollapse.ado:280`, `adofiles/f/fcollapse.ado:283`, `adofiles/f/fegen_group.ado:128`, `adofiles/f/fisid.ado:51`, `adofiles/f/flevelsof.ado:80`, `adofiles/f/fsort.ado:60`, `adofiles/f/ftab.ado:124`, `adofiles/j/join.ado:78`, `adofiles/j/join.ado:255`, `adofiles/l/local_inlist.ado:17`
- **DEAD_LINK**: 1 other links answered 404 or 410: https://maps.googleapis.com/maps/api/geocode/ (404).
  Evidence: `https://maps.googleapis.com/maps/api/geocode/`
- **LINK_UNVERIFIED**: 4 other links answered with an HTTP error other than 404 or 410, which does not show they are gone: https://github.com/sergiocorreia/ftools/raw/master/src/ (400), https://github.com/sergiocorreia/reghdfe/raw/master/src/ (400), https://github.com/sergiocorreia/ivreghdfe} (403), https://api.github.com/repos/rstudio/renv/tarball (403).
  Evidence: `https://github.com/sergiocorreia/ftools/raw/master/src/`, `https://github.com/sergiocorreia/reghdfe/raw/master/src/`, `https://github.com/sergiocorreia/ivreghdfe}`, `https://api.github.com/repos/rstudio/renv/tarball`
- **LINK_UNREACHABLE**: 16 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `http://portafolioinfo.cnbv.gob.mx/PortafolioInformacion/`, `https://www.openicpsr.org/openicpsr/project/113888/version/V1/view`, `https://www.openicpsr.org/openicpsr/project/116115/version/V1/view`, `https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/UJD5OP`, `https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/STTNUF`, `https://ars.els-cdn.com/content/image/1-s2.0-S0304387815000061-mmc1.zip`, `https://www.sciencedirect.com/science/article/pii/S0304387815000061#s0075`, `https://www.inegi.org.mx/app/descarga/`, `https://www.inegi.org.mx/programas/enoe/15ymas/default.html#Microdatos`, `https://www.inegi.org.mx/app/ageeml/#`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.

## What triage looked at

- 275 files, 1,698,061 bytes. Languages: python (1), r (50), stata (133).
- Documentation read: LICENSE.md, README.md, README.txt. Licences named: CC BY.
- Master scripts: scripts/00_run.do, scripts/01_bansefi_saldos_dataprep.do, scripts/02_bansefi_generales_dataprep.do, scripts/03_bansefi_movimientos_dataprep.do, scripts/04_bansefi_make_sample.do, scripts/05_bansefi_sucursales_dataprep.do, scripts/06_bansefi_bimswitch.do, scripts/07_bansefi_avgbal.do, scripts/08_bansefi_transactions_redef.do, scripts/09_bansefi_mechanical_effect.do.
- File reads traced: 391; writes: 245; unresolved paths: 150; missing: 1. modelo_urbano_263-locs.csv, analysis_dataallcountries.dta, bansefi_baseline.dta, bdu_actual_sean.rds, bdu_cp_month_means_new.csv, bdu_fake.rds, bdu_historico_sean.rds, cat_movimientos.csv, cpdescarga.txt, dreamfinal_for_analysis.dta, elecciones_long.dta, encel09_hh.dta, encel_forreg_permutations.dta, encelurb_trans_2002_2010.dta, entrevistas_educacion_noviembre_2010.dta, entrevistas_mapo_noviembre_2010.dta, fd_iter_2005.xlsx, harp_rosca_final.dta, hogar_educacion_diciembre_2010.dta, hogar_mapo_noviembre_2010.dta, inpc_02_14_workhorse_munibymonth_02_14_d.dta, integrantes_educacion_diciembre_2010.dta, integrantes_mapo_noviembre_2010.dta, iter05u.dta, iter_naltxt05.txt, iter_naltxt10.txt, kisdatafinal.dta, mcc_codes.csv, medios_pago_titular_beneficiarios.dta, n_withdrawals.dta, nepal_jde_r1.dta, net_savings_ind_0_ln.dta, net_savings_ind_0_w5.dta, rezago_social_localidad.dta, saldos promedio cuentahorro.dta, saldos promedio debicuenta.dta, sp_2007.dta, sp_2008.dta, year.dta.
- Links found: 24; checked: yes.
  - http://cran.us.r-project.org: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://creativecommons.org/policies: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://portafolioinfo.cnbv.gob.mx/PortafolioInformacion/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://scorreia.com/reghdfe/nested_within_cluster.pdf: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://api.github.com/repos/rstudio/renv/tarball: FAILED (403)
  - https://ars.els-cdn.com/content/image/1-s2.0-S0304387815000061-mmc1.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://blog.diegovalle.net/2013/06/shapefiles-of-mexico-agebs-manzanas-etc.html: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://cloud.r-project.org: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/STTNUF: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/UJD5OP: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://evaluacion.prospera.gob.mx/es/eval_cuant/p_bases_cuanti.php: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://github.com/greggles/mcc-codes: FAILED (403)
  - https://github.com/sergiocorreia/ftools/raw/master/src/: FAILED (400)
  - https://github.com/sergiocorreia/ivreghdfe}: FAILED (403)
  - https://github.com/sergiocorreia/reghdfe/raw/master/src/: FAILED (400)
  - https://maps.googleapis.com/maps/api/geocode/: FAILED (404)
  - https://www.coneval.org.mx/rw/resource/Rezago_social_-_localidad_-_stata.rar: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.inegi.org.mx/app/ageeml/#: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.inegi.org.mx/app/descarga/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.inegi.org.mx/programas/enoe/15ymas/default.html#Microdatos: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.openicpsr.org/openicpsr/project/113888/version/V1/view: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.openicpsr.org/openicpsr/project/116115/version/V1/view: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.sciencedirect.com/science/article/pii/S0304387815000061#s0075: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
