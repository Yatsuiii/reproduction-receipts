# Triage verdict: BLOCKED

- Package: `pkgs/rsaggio87__Replication_DKSS` at commit `ddbe91801f7193c63aebb4fd74cc63b77b0041d4`
- Triaged: 2026-11-21T18:16:36Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.398 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 23 blockers, 1 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `airfoil.mat` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/matlab_bgl/test/test_benchmark.m:58`
- **MISSING_INPUT_UNDOCUMENTED**: `src/AM_Tabulation5.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/AM_CI.m:15`, `analysis/add_ons/LeaveOutTwoWay/codes/AM_CI_old.m:13`
- **MISSING_INPUT_UNDOCUMENTED**: `tables/baseline_stats1.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/tableA2.do:294`
- **MISSING_INPUT_UNDOCUMENTED**: `tables/baseline_stats2.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/tableA2.do:295`
- **MISSING_INPUT_UNDOCUMENTED**: `tables/baseline_stats3.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/tableA2.do:296`
- **MISSING_INPUT_UNDOCUMENTED**: `/scratch/public/board/RAKIM/CLEANED_SPELL_GIANT_INVIND_data_1990_2016.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/multiple_spells.do:12`
- **MISSING_INPUT_UNDOCUMENTED**: `tables/controls_effects_FEMALE_SAMPLE_group_1_2_3.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/full_oaxaca.do:98`
- **MISSING_INPUT_UNDOCUMENTED**: `tables/controls_effects_MALE_SAMPLE_group_1_2_3.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/full_oaxaca.do:75`
- **MISSING_INPUT_UNDOCUMENTED**: `src/file_example1.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/example_testing_MC.m:158`
- **MISSING_INPUT_UNDOCUMENTED**: `/scratch/public/leave_out/matr_bitalia_1990_2013NEW_INVIND.dta` is read by the code and named in the documentation (README.md, README.txt), but it is not in the package and no source for it is given.
  Evidence: `analysis/codes/missing_reason.do:101`, `analysis/codes/tableA1.do:10`, `build/build_RAKIM.do:29`, `build/export_matlab.do:80`
- **MISSING_INPUT_UNDOCUMENTED**: `name_save.mat` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/mc_read.m:19`
- **MISSING_INPUT_UNDOCUMENTED**: `tables/oaxaca_decom1.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/figure8.do:205`, `analysis/codes/figure8.do:213`
- **MISSING_INPUT_UNDOCUMENTED**: `parfor_progress.txt` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/parfor_progress.m:46`, `analysis/add_ons/LeaveOutTwoWay/codes/parfor_progress.m:68`, `analysis/add_ons/LeaveOutTwoWay/codes/parfor_progress.m:72`
- **MISSING_INPUT_UNDOCUMENTED**: `/scratch/public/leave_out/PROVINCE.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/missing_reason.do:121`, `build/build_AKM.do:41`
- **MISSING_INPUT_UNDOCUMENTED**: `../build/src/RAKIM/Q_CLEANED_SPELL_GIANT_INVIND_data_1990_2016.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/figureA4.do:26`, `analysis/codes/tableA1.do:54`, `build/build_AKM.do:59`, `build/build_AKM.do:90`
- **MISSING_INPUT_UNDOCUMENTED**: `results/RESULTS_ALL_VENETO_LEAVE1_OUT.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/table_3.m:9`
- **MISSING_INPUT_UNDOCUMENTED**: `results/RESULTS_ALL_VENETO_LEAVE1_OUT_Lambda_P.mat` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/table_3.m:17`
- **MISSING_INPUT_UNDOCUMENTED**: `../tmp/RovigoCS_Leave2.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/verify_stayers.m:1`
- **MISSING_INPUT_UNDOCUMENTED**: `codes/summary_build.do` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/main.do:41`
- **MISSING_INPUT_UNDOCUMENTED**: `../src/test.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/main.m:55`
- **MISSING_INPUT_UNDOCUMENTED**: `/scratch/public/leave_out/Third_CLEANED_MONTHLY_PANEL_GIANT_1_INVIND_data_1990_2016.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/codes/build_figure6.do:36`
- **MISSING_INPUT_UNDOCUMENTED**: `/scratch/public/leave_out/Verona_1996or2001_unbalanced.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/example_testing_MC.m:60`
- **MISSING_INPUT_UNDOCUMENTED**: `west0479.mat` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `analysis/add_ons/matlab_bgl/test/test_benchmark.m:74`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/AM_CI.m`, `analysis/add_ons/LeaveOutTwoWay/codes/AM_CI_old.m`, `analysis/add_ons/LeaveOutTwoWay/codes/C_build.m`, `analysis/add_ons/LeaveOutTwoWay/codes/C_build_FD.m`, `analysis/add_ons/LeaveOutTwoWay/codes/C_build_cck.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `analysis/codes/beaudry_di_nardo.do`, `analysis/codes/build_figure6.do`, `analysis/codes/build_lincom.do`, `analysis/codes/build_managers.do`, `analysis/codes/build_oaxaca.do`
- **UNRESOLVED_PATHS**: 218 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `analysis/add_ons/LeaveOutTwoWay/codes/example_testing_MC.m:83`, `analysis/add_ons/LeaveOutTwoWay/codes/example_testing_MC.m:92`, `analysis/add_ons/LeaveOutTwoWay/codes/example_testing_MC.m:177`, `analysis/add_ons/LeaveOutTwoWay/codes/example_testing_MC.m:185`, `analysis/add_ons/LeaveOutTwoWay/codes/kss_cck.m:21`, `analysis/add_ons/LeaveOutTwoWay/codes/kss_cck.m:22`, `analysis/add_ons/LeaveOutTwoWay/codes/table_3_panel_B.m:5`, `analysis/add_ons/LeaveOutTwoWay/codes/table_3_panel_B.m:18`, `analysis/add_ons/LeaveOutTwoWay/codes/testing_cck.m:38`, `analysis/add_ons/LeaveOutTwoWay/codes/testing_cck.m:52`

## What triage looked at

- 1353 files, 38,374,715 bytes. Languages: c (52), c++ (1), matlab (297), shell (6), stata (38).
- Documentation read: README.md, README.txt. Licences named: none.
- Master scripts: analysis/add_ons/LeaveOutTwoWay/codes/MATLAB/Hierarchy/MexFunctions/MakeHierarchyMex.m, analysis/add_ons/LeaveOutTwoWay/codes/MATLAB/Hierarchy/MexFunctions/MakeHierarchyMex_debug.m, analysis/add_ons/LeaveOutTwoWay/codes/MATLAB/Solver/MakeSolverMex.m, analysis/add_ons/LeaveOutTwoWay/codes/MATLAB/Solver/MakeSolverMex_debug.m, analysis/add_ons/LeaveOutTwoWay/codes/MakeCMG.m, analysis/add_ons/LeaveOutTwoWay/codes/main.m, analysis/add_ons/matlab_bgl/libmbgl/libmbgl_test/Makefile, analysis/add_ons/matlab_bgl/make_biconnected_planar.m, analysis/add_ons/matlab_bgl/make_connected.m, analysis/add_ons/matlab_bgl/make_maximal_planar.m, analysis/main.do, build/main.do.
- File reads traced: 368; writes: 154; unresolved paths: 218; missing: airfoil.mat, am_tabulation5.csv, baseline_stats1.dta, baseline_stats2.dta, baseline_stats3.dta, cleaned_spell_giant_invind_data_1990_2016.dta, controls_effects_female_sample_group_1_2_3.csv, controls_effects_male_sample_group_1_2_3.csv, file_example1.csv, matr_bitalia_1990_2013new_invind.dta, name_save.mat, oaxaca_decom1.dta, parfor_progress.txt, province.dta, q_cleaned_spell_giant_invind_data_1990_2016.dta, results_all_veneto_leave1_out.csv, results_all_veneto_leave1_out_lambda_p.mat, rovigocs_leave2.csv, summary_build.do, test.csv, third_cleaned_monthly_panel_giant_1_invind_data_1990_2016.dta, verona_1996or2001_unbalanced.csv, west0479.mat.
- Links found: 3; checked: no.
