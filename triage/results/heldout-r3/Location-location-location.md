# Triage verdict: BLOCKED

- Package: `https://github.com/jrothst/Location-location-location` at commit `f7391e148cb75509e97db1e296983707a51edaf2`
- Triaged: 2026-11-21T12:12:32Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.432 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 15 blockers, 3 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **PROPRIETARY_SOFTWARE**: Requires Sas, which is proprietary and not declared available on this desk. Rerun triage with --have sas if a licensed copy is available.
  Evidence: `portion1_acs/code/step2_extract_programs/extract10.sas`, `portion1_acs/code/step2_extract_programs/extract11.sas`, `portion1_acs/code/step2_extract_programs/extract12.sas`, `portion1_acs/code/step2_extract_programs/extract13.sas`, `portion1_acs/code/step2_extract_programs/extract14.sas`
- **MISSING_INPUT_RESTRICTED**: `$tempdir/datafrommatlab_cz.raw` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/runakm_2step_rep.do:260`
- **MISSING_INPUT_RESTRICTED**: `$tempdir/datafrommatlab_firm.raw` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/6_disc7-8_rep.do:2005`, `portion2_rdc/runakm_2step_rep.do:273`
- **MISSING_INPUT_RESTRICTED**: `$tempdir/datafrommatlab_person.raw` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/runakm_2step_rep.do:278`
- **MISSING_INPUT_RESTRICTED**: `$tempdir/datafrommatlab_stats.raw` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/runakm_2step_rep.do:264`
- **MISSING_INPUT_RESTRICTED**: `$data/M10_AKM_10pctB.txt` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/mig5_tabsdisclosure7.do:192`
- **MISSING_INPUT_RESTRICTED**: `$data/M10_AKM_10pctB_jc.txt` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/mig5_tabsdisclosure7.do:202`
- **MISSING_INPUT_RESTRICTED**: `$yidata/m5_ecf_seinunit.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/6_disc7-8_rep.do:92`, `portion2_rdc/6_disc7-8_rep.do:158`, `portion2_rdc/6_disc7-8_rep.do:377`, `portion2_rdc/6_disc7-8_rep.do:681`, `portion2_rdc/6_disc7-8_rep.do:962`
- **MISSING_INPUT_RESTRICTED**: `m5_icf_dob.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/mig5_clean2.do:79`
- **MISSING_INPUT_RESTRICTED**: `m5_piklist_educacs.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/mig5_clean2.do:322`, `portion2_rdc/mig5_clean2.do:334`
- **MISSING_INPUT_RESTRICTED**: `$yidata/mig5_pikqtime_1018_educacstop59_new.raw` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/6_disc7-8_rep.do:920`
- **MISSING_INPUT_RESTRICTED**: `phftemp_akm.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `portion2_rdc/mig5_clean2.do:65`, `portion2_rdc/mig5_clean2.do:486`
- **MISSING_INPUT_UNDOCUMENTED**: `${scratch}/phi_cz_alt-wage.dta` is read by the code and named in the documentation (portion1_acs/readme.txt), but it is not in the package and no source for it is given.
  Evidence: `portion1_acs/code/step6_tocensus/makecensusfiles.do:12`
- **MISSING_INPUT_UNDOCUMENTED**: `$data2step/young_comparemodels_top10.dta` is read by the code and named in the documentation (portion2_rdc/readme.txt), but it is not in the package and no source for it is given.
  Evidence: `portion2_rdc/mig5_tabsdisclosure7.do:172`
- **MISSING_INPUT_UNDOCUMENTED**: `$data2step/young_comparemodels_top25.dta` is read by the code and named in the documentation (portion2_rdc/readme.txt), but it is not in the package and no source for it is given.
  Evidence: `portion2_rdc/mig5_tabsdisclosure7.do:182`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **MISSING_INPUT_DOWNLOAD**: `${scratch}/household.dta` is not in the package; the documentation (portion1_acs/origdata/readme_sources.txt, portion1_acs/readme.txt) says to download it from https://www2.census.gov/programs-surveys/acs/data/pums/2018/5-Year/unix_hus.zip. The download date and the file's SHA-256 become part of the receipt.
  Evidence: `portion1_acs/code/step5_housing/hprices.do:10`, `https://www2.census.gov/programs-surveys/acs/data/pums/2018/5-Year/unix_hus.zip`
- **DATA_LINK_UNREACHABLE**: Could not reach https://www2.census.gov/programs-surveys/acs/data/pums/2018/5-Year/unix_hus.zip from this machine (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>). That is evidence about this machine's network, not about the link; check it from another network before treating the data as unavailable.
  Evidence: `portion1_acs/code/step5_housing/hprices.do:10`, `https://www2.census.gov/programs-surveys/acs/data/pums/2018/5-Year/unix_hus.zip`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `portion2_rdc/M10_AKM_10pctB_cz.m`, `portion2_rdc/M10_AKM_10pctB_czind.m`, `portion2_rdc/akm_pcg_spelldata.m`, `portion2_rdc/dynamic_young/akm_pcg.m`, `portion2_rdc/dynamic_young/firmAKM_callable.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `portion1_acs/code/main_acs.do`, `portion1_acs/code/step1_CZ_puma_files/puma2000_prep.do`, `portion1_acs/code/step1_CZ_puma_files/puma2010_prep.do`, `portion1_acs/code/step2_extract_programs/extractacs.do`, `portion1_acs/code/step2_extract_programs/hours1.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: ${scratch}/czeffects.dta, ${tocensus}/czeffects.dta, ${tocensus}/czranking6_alt-wage.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `${scratch}/czeffects.dta`, `${tocensus}/czeffects.dta`, `${tocensus}/czranking6_alt-wage.dta`
- **UNRESOLVED_PATHS**: 211 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `portion1_acs/code/step2_extract_programs/hours1.do:13`, `portion1_acs/code/step2_extract_programs/hours1.do:133`, `portion1_acs/code/step2_extract_programs/hours1.do:247`, `portion1_acs/code/step2_extract_programs/hours1.do:248`, `portion1_acs/code/step2_extract_programs/rank_revised_extravars.do:19`, `portion1_acs/code/step2_extract_programs/rank_revised_extravars.do:140`, `portion1_acs/code/step2_extract_programs/rank_revised_extravars.do:255`, `portion1_acs/code/step2_extract_programs/rank_revised_extravars.do:256`, `portion1_acs/code/step2_extract_programs/readacs.do:14`, `portion1_acs/code/step3_collapse/cz_chars.do:16`
- **LINK_UNREACHABLE**: 13 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `https://www.openicpsr.org/openicpsr/project/193945/version/V1/view?path=/openicpsr/193945/fcr:versions/V1&type=project`, `https://doi.org/10.3886/E193945V1`, `http://ddorn.net/data.htm#Local%20Labor%20Market%20Geography`, `https://www2.census.gov/programs-surveys/acs/data/pums/2010/1-Year/csv_pus.zip`, `https://www2.census.gov/programs-surveys/acs/data/pums/2011/1-Year/csv_pus.zip`, `https://www2.census.gov/programs-surveys/acs/data/pums/2012/1-Year/csv_pus.zip`, `https://www2.census.gov/programs-surveys/acs/data/pums/2013/1-Year/csv_pus.zip`, `https://www2.census.gov/programs-surveys/acs/data/pums/2014/1-Year/csv_pus.zip`, `https://www2.census.gov/programs-surveys/acs/data/pums/2015/1-Year/csv_pus.zip`, `https://www2.census.gov/programs-surveys/acs/data/pums/2016/1-Year/csv_pus.zip`

## What triage looked at

- 114 files, 7,750,409 bytes. Languages: matlab (6), sas (12), stata (39).
- Documentation read: README.md, portion1_acs/origdata/dorn/README_Dorn.txt, portion1_acs/origdata/readme_sources.txt, portion1_acs/readme.txt, portion2_rdc/readme.txt. Licences named: CC BY, BSD.
- Master scripts: portion1_acs/code/step6_tocensus/makecensusfiles.do.
- File reads traced: 463; writes: 214; unresolved paths: 211; missing: datafrommatlab_cz.raw, datafrommatlab_firm.raw, datafrommatlab_person.raw, datafrommatlab_stats.raw, household.dta, m10_akm_10pctb.txt, m10_akm_10pctb_jc.txt, m5_ecf_seinunit.dta, m5_icf_dob.dta, m5_piklist_educacs.dta, mig5_pikqtime_1018_educacstop59_new.raw, phftemp_akm.dta, phi_cz_alt-wage.dta, young_comparemodels_top10.dta, young_comparemodels_top25.dta.
- Links found: 14; checked: yes.
  - http://ddorn.net/data.htm#Local%20Labor%20Market%20Geography: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://ddorn.net/data/cw_cty_czone.zip: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://doi.org/10.3886/E193945V1: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.openicpsr.org/openicpsr/project/193945/version/V1/view?path=/openicpsr/193945/fcr:versions/V1&type=project: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2010/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2011/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2012/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2013/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2014/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2015/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2016/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2017/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2018/1-Year/csv_pus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www2.census.gov/programs-surveys/acs/data/pums/2018/5-Year/unix_hus.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
