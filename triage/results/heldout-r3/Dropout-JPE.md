# Triage verdict: BLOCKED

- Package: `https://github.com/tyleransom/Dropout-JPE` at commit `fb1e3f6962a80c8bd839c9956f6cca7b93acd983`
- Triaged: 2026-11-21T12:12:29Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 1.045 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 21 blockers, 3 deviations, 6 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `../../EstimationNoGradSchTheta0_4/cmapoutput.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:6`
- **MISSING_INPUT_RESTRICTED**: `../../EstimationNoGradSchTheta0_4/cmapoutput_t1.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:7`
- **MISSING_INPUT_RESTRICTED**: `../../EstimationNoGradSchTheta0_4/cmapoutput_t2.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:8`
- **MISSING_INPUT_RESTRICTED**: `CompStatTableBase.tex` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:1624`
- **MISSING_INPUT_RESTRICTED**: `dataStruct.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:5`, `src/simulations-forward-fit/simulatorMCintEstData10D.m:18`, `src/simulations-forward-fit/simulatorMCintEstDataRFCCP10D.m:18`
- **MISSING_INPUT_RESTRICTED**: `../../output/learning/everything37131357.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/estimation-stage3-5-structural/runmodel_consump_jointsearchfrictions_WCabsorb.m:52`, `src/estimation-stage3-gridsearch/runmodel_consump_jointsearchfrictions_WCabsorb.m:59`
- **MISSING_INPUT_RESTRICTED**: `../../output/all-stage-1/everything_all_stage1_interact_type_36688212.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/estimation-stage2-learning/runmodel_learning_only.m:72`, `src/estimation-stage3-5-structural/runmodel_consump_jointsearchfrictions_WCabsorb.m:50`, `src/estimation-stage3-gridsearch/runmodel_consump_jointsearchfrictions_WCabsorb.m:57`, `src/parametric-bootstrap/estimates_tables.m:26`, `src/parametric-bootstrap/parboot.m:39`
- **MISSING_INPUT_RESTRICTED**: `../../output/all-stage-1/everything_all_stage1_interact_type_37753198.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/parametric-bootstrap/parboot.m:40`
- **MISSING_INPUT_RESTRICTED**: `../../output/utility/everything_consumpstructural_FVfast39374622.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/parametric-bootstrap/parboot.m:76`
- **MISSING_INPUT_RESTRICTED**: `../../output/utility/everything_jointsearch_WCabsorb37595330.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/parametric-bootstrap/parboot.m:72`
- **MISSING_INPUT_RESTRICTED**: `../../EstimationNoGradSchTheta0_4/gradLogitEstimatesMostFlex.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:9`
- **MISSING_INPUT_RESTRICTED**: `majSwitchTableBase.tex` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:1674`
- **MISSING_INPUT_RESTRICTED**: `../../output/all-stage-1/msys-schabil36688212.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/parametric-bootstrap/parboot.m:42`
- **MISSING_INPUT_RESTRICTED**: `../../output/all-stage-1/msys-schpref36688212.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/parametric-bootstrap/parboot.m:59`
- **MISSING_INPUT_RESTRICTED**: `../../output/all-stage-1/msys-wrkabilpref36688212.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/parametric-bootstrap/parboot.m:66`
- **MISSING_INPUT_RESTRICTED**: `prior.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/simulatorMCintEstData10D.m:15`, `src/simulations-forward-fit/simulatorMCintEstDataRFCCP10D.m:15`
- **MISSING_INPUT_RESTRICTED**: `simDataMCintEstData10D_10rep.mat` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/simulations-forward-fit/functions/analysisMCintEstDataNormedfunction.m:15`
- **MISSING_INPUT_RESTRICTED**: `${data_loc}/sippl04puw3.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/data-cleaning/sipp/create_sipp.do:57`
- **MISSING_INPUT_RESTRICTED**: `${data_loc}/sippp04putm3.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/data-cleaning/sipp/create_sipp.do:59`
- **MISSING_INPUT_RESTRICTED**: `${data_loc}/sippp04putm4.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `src/data-cleaning/sipp/create_sipp.do:60`
- **MISSING_INPUT_UNDOCUMENTED**: `y97_all_tscrGPA.dta` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `src/descriptives/descriptives.do:13`

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Julia code without a Manifest.toml: package versions are not pinned.
  Evidence: `src/config_julia.jl`, `src/simulations-counterfactual/baseline/allfuns.jl`, `src/simulations-counterfactual/baseline/shellsimbatch.jl`, `src/simulations-counterfactual/baseline/testgpd.jl`, `src/simulations-counterfactual/baseline-1minusBeta/allfuns.jl`
- **ABSOLUTE_PATH**: 135 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `src/parametric-bootstrap/estimates_tables.m:183`, `src/parametric-bootstrap/estimates_tables.m:187`, `src/parametric-bootstrap/estimates_tables.m:191`, `src/parametric-bootstrap/estimates_tables.m:199`, `src/parametric-bootstrap/estimates_tables.m:204`, `src/parametric-bootstrap/estimates_tables.m:207`, `src/parametric-bootstrap/estimates_tables.m:210`, `src/parametric-bootstrap/estimates_tables.m:231`, `src/parametric-bootstrap/estimates_tables.m:235`, `src/parametric-bootstrap/estimates_tables.m:239`
- **LONG_COMPUTE**: The documentation claims a run time of about 336 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `src/data-cleaning/nlsy97/data_import_20220401_tscrGPA.m`, `src/estimation-stage1/functions/applyRestr.m`, `src/estimation-stage1/functions/applyRestrGrad.m`, `src/estimation-stage1/functions/create_estimatemeas_data.m`, `src/estimation-stage1/functions/createchoicedata.m`
- **SOFTWARE_REQUIRED**: Requires Stata (version 13.0, 15.1 named in code); the desk says it has it.
  Evidence: `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do`, `data/nlsy97/raw/AFQT_MATCHING_AR/AFQT_MATCHING_AR_with_weights.do`, `data/nlsy97/raw/AFQT_MATCHING_AR/y79_asvab-value-labels.do`, `data/nlsy97/raw/AFQT_MATCHING_CS/AFQT_MATCHING_CS_with_weights.do`, `data/nlsy97/raw/AFQT_MATCHING_CS/y79_asvab-value-labels.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: afqt_adjusted_final97.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `afqt_adjusted_final97.dta`
- **UNRESOLVED_PATHS**: 357 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:61`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:70`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:96`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:106`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:119`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:203`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:204`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:216`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:224`, `data/nlsy97/raw/AFQT_MATCHING/AFQT_MATCHING_with_weights.do:246`
- **LINK_UNREACHABLE**: 6 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `https://nces.ed.gov/datalab/`, `https://www.nlsinfo.org/investigator/pages/login`, `http://www.fabianlange.ca/data.html`, `https://www.nber.org/research/data/survey-income-and-program-participation-sipp`, `https://cps.ipums.org/cps/`, `https://doi.org/10.18128/D030.V10.0`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.

## What triage looked at

- 627 files, 279,051,916 bytes. Languages: julia (10), matlab (237), shell (1), stata (49).
- Documentation read: README.md, data/cps/cleaned/README, data/cps/raw/README, data/sipp/raw/README, exhibits/figures/README.md, exhibits/tables/README.md, exhibits/tables/junk/README.md, output/all-stage-1/README.md, output/bootstrap/README.md, output/cfl/baseline-1minusBeta/README.md, output/cfl/baseline/README.md, output/cfl/no-cred-cons/README.md, output/cfl/no-frictions/README.md, output/learning/README.md, output/model-fit/README.md, output/utility-grid-search/CRRA-0-05/README.md, output/utility-grid-search/CRRA-0-1/README.md, output/utility-grid-search/CRRA-0-15/README.md, output/utility-grid-search/CRRA-0-2/README.md, output/utility-grid-search/CRRA-0-25/README.md, output/utility-grid-search/CRRA-0-3/README.md, output/utility-grid-search/CRRA-0-35/README.md, output/utility-grid-search/CRRA-0-4/README.md, output/utility-grid-search/CRRA-0-45/README.md, output/utility-grid-search/CRRA-0-5/README.md, output/utility-grid-search/CRRA-0-55/README.md, output/utility-grid-search/CRRA-0-6/README.md, output/utility-grid-search/CRRA-0-65/README.md, output/utility-grid-search/CRRA-0-7/README.md, output/utility-grid-search/CRRA-0-75/README.md, output/utility-grid-search/CRRA-0-8/README.md, output/utility-grid-search/CRRA-0-85/README.md, output/utility-grid-search/CRRA-0-9/README.md, output/utility-grid-search/CRRA-0-95/README.md, output/utility-grid-search/CRRA-0/README.md, output/utility-grid-search/CRRA-1-05/README.md, output/utility-grid-search/CRRA-1-1/README.md, output/utility-grid-search/CRRA-1-15/README.md, output/utility-grid-search/CRRA-1-2/README.md, output/utility-grid-search/CRRA-1-25/README.md, output/utility-grid-search/CRRA-1-3/README.md, output/utility-grid-search/CRRA-1-35/README.md, output/utility-grid-search/CRRA-1-4/README.md, output/utility-grid-search/CRRA-1-45/README.md, output/utility-grid-search/CRRA-1-5/README.md, output/utility-grid-search/CRRA-1-55/README.md, output/utility-grid-search/CRRA-1-6/README.md, output/utility-grid-search/CRRA-1-65/README.md, output/utility-grid-search/CRRA-1-7/README.md, output/utility-grid-search/CRRA-1-75/README.md, output/utility-grid-search/CRRA-1-8/README.md, output/utility-grid-search/CRRA-1-85/README.md, output/utility-grid-search/CRRA-1-9/README.md, output/utility-grid-search/CRRA-1-95/README.md, output/utility-grid-search/CRRA-2/README.md, output/utility/README.md. Licences named: CC0, MIT, GPL.
- Master scripts: src/estimation-stage1/functions/makegrid.m, src/estimation-stage1/functions/makegrid2_con.m, src/estimation-stage1/functions/makegrid_con.m, src/estimation-stage1/functions/makegrid_time_invar.m, src/estimation-stage1/functions/makegridchoice.m, src/estimation-stage1/functions/makegridchoice_con.m, src/estimation-stage1/functions/makegridq.m, src/estimation-stage2-learning/functions/makegrid.m, src/estimation-stage2-learning/functions/makegrid_con.m, src/estimation-stage2-learning/functions/makegridchoice.m, src/estimation-stage2-learning/functions/makegridchoice_con.m, src/estimation-stage3-5-structural/functions/makegrid.m, src/estimation-stage3-5-structural/functions/makegrid_con.m, src/estimation-stage3-5-structural/functions/makegrid_gpa_id.m, src/estimation-stage3-5-structural/functions/makegrid_maj_id.m, src/estimation-stage3-5-structural/functions/makegrid_type_id.m, src/estimation-stage3-5-structural/functions/makegridchoice.m, src/estimation-stage3-5-structural/functions/makegridchoice_con.m.
- File reads traced: 479; writes: 315; unresolved paths: 357; missing: cmapoutput.mat, cmapoutput_t1.mat, cmapoutput_t2.mat, compstattablebase.tex, datastruct.mat, everything37131357.mat, everything_all_stage1_interact_type_36688212.mat, everything_all_stage1_interact_type_37753198.mat, everything_consumpstructural_fvfast39374622.mat, everything_jointsearch_wcabsorb37595330.mat, gradlogitestimatesmostflex.mat, majswitchtablebase.tex, msys-schabil36688212.csv, msys-schpref36688212.csv, msys-wrkabilpref36688212.csv, prior.mat, simdatamcintestdata10d_10rep.mat, sippl04puw3.dta, sippp04putm3.dta, sippp04putm4.dta, y97_all_tscrgpa.dta.
- Links found: 6; checked: yes.
  - http://www.fabianlange.ca/data.html: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://cps.ipums.org/cps/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://doi.org/10.18128/D030.V10.0: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://nces.ed.gov/datalab/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.nber.org/research/data/survey-income-and-program-participation-sipp: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.nlsinfo.org/investigator/pages/login: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
