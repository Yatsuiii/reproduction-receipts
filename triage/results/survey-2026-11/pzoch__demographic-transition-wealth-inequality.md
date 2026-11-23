# Triage verdict: BLOCKED

- Package: `pkgs/pzoch__demographic-transition-wealth-inequality` at commit `bc01805b1e16ee906f200292c0f73d4b0b5568a8`
- Triaged: 2026-11-21T18:16:35Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.233 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 4 blockers, 8 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `$resultspath\\$scenario\\avg_hours_trans.txt` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `outputs_stata_code/MvD_1_macro.do:126`
- **MISSING_INPUT_UNDOCUMENTED**: `$resultspath\\$scenario\\benefits_trans.txt` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `outputs_stata_code/MvD_1_macro.do:70`
- **MISSING_INPUT_UNDOCUMENTED**: `$resultspath\\$scenario\\irr_trans_1y.txt` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `outputs_stata_code/MvD_1_macro.do:28`
- **MISSING_INPUT_RESTRICTED**: `\r\n` is read by the code but is not in the package, and the documentation (README.md, SCENARIOS.md, fortran_code/Instructions/beqs_all_govt__instructions.txt, fortran_code/Instructions/beqs_ndm_govt__instructions.txt, fortran_code/Instructions/crr3_all_govt__instructions.txt, fortran_code/Instructions/crr3_ndm_govt__instructions.txt, fortran_code/Instructions/exor_all_govt__instructions.txt, fortran_code/Instructions/gcbo_all_govt__instructions.txt, fortran_code/Instructions/gcbo_ndm_govt__instructions.txt, fortran_code/Instructions/hrat_all_govt__instructions.txt, fortran_code/Instructions/hrat_ndm_govt__instructions.txt, fortran_code/Instructions/ndel_all_govt__instructions.txt, fortran_code/Instructions/ndel_ndm_govt__instructions.txt, fortran_code/Instructions/nstr_all_govt__instructions.txt, fortran_code/Instructions/nstr_ndm_govt__instructions.txt, fortran_code/Instructions/psid_all_govt__instructions.txt, fortran_code/Instructions/psid_ncp_govt__instructions.txt, fortran_code/Instructions/psid_ncs_govt__instructions.txt, fortran_code/Instructions/psid_ndm_govt__instructions.txt, fortran_code/Instructions/psid_ndo_govt__instructions.txt, fortran_code/Instructions/psid_ndp_govt__instructions.txt, fortran_code/Instructions/psid_nds_govt__instructions.txt, fortran_code/Instructions/psid_nga_govt__instructions.txt, fortran_code/Instructions/psid_nlb_govt__instructions.txt, fortran_code/Instructions/psid_nls_govt__instructions.txt, fortran_code/Instructions/psid_nsh_govt__instructions.txt, fortran_code/Instructions/psid_ntc_govt__instructions.txt, fortran_code/Instructions/psid_ntk_govt__instructions.txt, fortran_code/Instructions/psid_ntl_govt__instructions.txt, fortran_code/Instructions/psid_ntp_govt__instructions.txt, fortran_code/Instructions/psid_nts_govt__instructions.txt, fortran_code/Instructions/psid_ntx_govt__instructions.txt, inputs_stata_code/income_process/PSID/README.md, inputs_stata_code/skill_premium/ACS_college/README.md) describes it as restricted ("restricted-use"). The desk cannot run this without access.
  Evidence: `inputs_matlab_code/income_process/loader.m:18`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **UNPINNED_DEPENDENCIES**: R code loads data.table, foreign, psidR with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `inputs_stata_code/income_process/PSID/psid_read.R:20`, `inputs_stata_code/income_process/PSID/psid_read.R:21`, `inputs_stata_code/income_process/PSID/psid_read.R:22`
- **STATA_NETWORK_INSTALL**: Do-files install ineqdeco, lorenz, mat2txt, scheme-burd from the network at run time, with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.
  Evidence: `inputs_stata_code/__main_data_prepare.do:4`, `inputs_stata_code/income_process/I01_00_config.do:80`, `inputs_stata_code/social_security/T04plot_rho.do:6`, `outputs_stata_code/MvD_2_Gini_income.do:5`, `outputs_stata_code/__main.do:16`, `outputs_stata_code/_prep_Gini_data.do:3`
- **MISSING_INPUT_REGISTRATION**: `skill_premium\ACS_college\ACS_college.dta` is not in the package; the documentation (README.md, inputs_stata_code/skill_premium/ACS_college/README.md) says it comes from a source that needs registration ("IPUMS"). The desk must register, download and log the extract.
  Evidence: `inputs_stata_code/skill_premium/D02_prepare_college.do:9`
- **MISSING_INPUT_REGISTRATION**: `$resultspath/$variant_base/population.csv` is not in the package; the documentation (README.md, SCENARIOS.md) says it comes from a source that needs registration ("IPUMS"). The desk must register, download and log the extract.
  Evidence: `outputs_stata_code/R_FigureC1_popstructure.do:7`, `outputs_stata_code/R_FigureC1_popstructure.do:21`
- **MISSING_INPUT_REGISTRATION**: `..\data\PSID\psid_ready.dta` is not in the package; the documentation (README.md, inputs_stata_code/income_process/PSID/README.md) says it comes from a source that needs registration ("IPUMS"). The desk must register, download and log the extract.
  Evidence: `outputs_stata_code/MvD_2_Gini_income.do:12`
- **MISSING_INPUT_REGISTRATION**: `..\data\SCF\SCF_plus.dta` is not in the package; the documentation (README.md) says it comes from a source that needs registration ("IPUMS"). The desk must register, download and log the extract.
  Evidence: `outputs_stata_code/MvD_3_GE_decomposition.do:70`, `outputs_stata_code/_prep_Gini_data.do:41`
- **ABSOLUTE_PATH**: 1 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `inputs_stata_code/income_process/PSID/psid_read.R:78`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `inputs_matlab_code/income_process/create_parameters_binned.m`, `inputs_matlab_code/income_process/estimate_parameters.m`, `inputs_matlab_code/income_process/loader.m`, `inputs_matlab_code/income_process/objective_cohort_binned.m`, `outputs_matlab_code/income_process/plot_estimates.m`
- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `inputs_stata_code/__main_data_prepare.do`, `inputs_stata_code/_prepare_programs.do`, `inputs_stata_code/demography/hetero_pi/D03_prepare_hetero_pi.do`, `inputs_stata_code/demography/mortality/D01_life_tables.do`, `inputs_stata_code/depreciation/M01prepare_depr.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: ../graphs/outputs/wealth_inequality/combined_gini.dta, bone.dta, bone1y.dta, data/avghours_data.dta, data/benefits_cbo.dta, data/irr_data.dta, demography\hetero_pi\processed\hetero_pi.dta, demography\hetero_pi\processed\pi_col_merge_M.dta, demography\mortality\processed\mortality_part_00.dta, demography\mortality\processed\mortality_part_11.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `../graphs/outputs/wealth_inequality/combined_gini.dta`, `bone.dta`, `bone1y.dta`, `data/avghours_data.dta`, `data/benefits_cbo.dta`, `data/irr_data.dta`, `demography\hetero_pi\processed\hetero_pi.dta`, `demography\hetero_pi\processed\pi_col_merge_M.dta`, `demography\mortality\processed\mortality_part_00.dta`, `demography\mortality\processed\mortality_part_11.dta`
- **UNRESOLVED_PATHS**: 36 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `inputs_matlab_code/income_process/estimate_parameters.m:351`, `inputs_stata_code/demography/hetero_pi/D03_prepare_hetero_pi.do:38`, `inputs_stata_code/demography/hetero_pi/D03_prepare_hetero_pi.do:176`, `inputs_stata_code/demography/hetero_pi/D03_prepare_hetero_pi.do:177`, `inputs_stata_code/income_process/I01_01_prepare_common_sample.do:19`, `inputs_stata_code/income_process/I01_02_make_variant_samples.do:27`, `inputs_stata_code/income_process/I01_02_make_variant_samples.do:46`, `inputs_stata_code/income_process/I01_02_make_variant_samples.do:76`, `inputs_stata_code/income_process/I01_03_export_omega_covariances.do:46`, `inputs_stata_code/income_process/I01_03_export_omega_covariances.do:49`

## What triage looked at

- 465 files, 212,843,414 bytes. Languages: fortran (46), matlab (5), r (1), stata (38).
- Documentation read: README.md, SCENARIOS.md, fortran_code/Instructions/beqs_all_govt__instructions.txt, fortran_code/Instructions/beqs_ndm_govt__instructions.txt, fortran_code/Instructions/crr3_all_govt__instructions.txt, fortran_code/Instructions/crr3_ndm_govt__instructions.txt, fortran_code/Instructions/exor_all_govt__instructions.txt, fortran_code/Instructions/gcbo_all_govt__instructions.txt, fortran_code/Instructions/gcbo_ndm_govt__instructions.txt, fortran_code/Instructions/hrat_all_govt__instructions.txt, fortran_code/Instructions/hrat_ndm_govt__instructions.txt, fortran_code/Instructions/ndel_all_govt__instructions.txt, fortran_code/Instructions/ndel_ndm_govt__instructions.txt, fortran_code/Instructions/nstr_all_govt__instructions.txt, fortran_code/Instructions/nstr_ndm_govt__instructions.txt, fortran_code/Instructions/psid_all_govt__instructions.txt, fortran_code/Instructions/psid_ncp_govt__instructions.txt, fortran_code/Instructions/psid_ncs_govt__instructions.txt, fortran_code/Instructions/psid_ndm_govt__instructions.txt, fortran_code/Instructions/psid_ndo_govt__instructions.txt, fortran_code/Instructions/psid_ndp_govt__instructions.txt, fortran_code/Instructions/psid_nds_govt__instructions.txt, fortran_code/Instructions/psid_nga_govt__instructions.txt, fortran_code/Instructions/psid_nlb_govt__instructions.txt, fortran_code/Instructions/psid_nls_govt__instructions.txt, fortran_code/Instructions/psid_nsh_govt__instructions.txt, fortran_code/Instructions/psid_ntc_govt__instructions.txt, fortran_code/Instructions/psid_ntk_govt__instructions.txt, fortran_code/Instructions/psid_ntl_govt__instructions.txt, fortran_code/Instructions/psid_ntp_govt__instructions.txt, fortran_code/Instructions/psid_nts_govt__instructions.txt, fortran_code/Instructions/psid_ntx_govt__instructions.txt, inputs_stata_code/income_process/PSID/README.md, inputs_stata_code/skill_premium/ACS_college/README.md. Licences named: MIT.
- Master scripts: fortran_code/main.f90.
- File reads traced: 161; writes: 72; unresolved paths: 36; missing: acs_college.dta, avg_hours_trans.txt, benefits_trans.txt, irr_trans_1y.txt, n, population.csv, psid_ready.dta, scf_plus.dta.
- Links found: 23; checked: no.
