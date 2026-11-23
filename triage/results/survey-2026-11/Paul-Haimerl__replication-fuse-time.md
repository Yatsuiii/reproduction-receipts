# Triage verdict: BLOCKED

- Package: `pkgs/Paul-Haimerl__replication-fuse-time` at commit `d768f7539e679bda30f1663233147f3fd25cb8de`
- Triaged: 2026-11-21T18:16:37Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.09 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 6 blockers, 2 deviations, 6 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `df_emp_illustration.xlsx` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `Code/Matlab/empirical_illustration.m:43`
- **MISSING_INPUT_UNDOCUMENTED**: `empirical_coefficients_reference.mat` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `Code/Matlab/verify_empirical.m:51`
- **MISSING_INPUT_RESTRICTED**: `empirical_verification.json` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("proprietary"), so it is most likely one of those.
  Evidence: `Code/Matlab/verify_empirical.m:80`, `Code/Matlab/verify_empirical.m:136`
- **MISSING_INPUT_UNDOCUMENTED**: `Timing_DGP1_N100_T50.rds` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `Code/R/07_Timing_Table.R:30`
- **MISSING_INPUT_UNDOCUMENTED**: `Timing_DGP1_N50_T50.rds` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `Code/R/07_Timing_Table.R:29`
- **MISSING_INPUT_UNDOCUMENTED**: `Timing_summary_DGP_1_K_N50_N100_T50.xlsx` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `Code/R/07_Timing_Table.R:32`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads PAGFL, PAGFLReplication, aricode, gridExtra, openxlsx, pckg, readxl with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `Code/R/01_MC_Simulation_Study.R:165`, `Code/R/Fast_One_Cell_Check.R:247`, `Code/R/Helper_Functions.R:2`, `Code/R/Helper_Functions.R:7`, `Code/R/Helper_Functions.R:166`
- **LONG_COMPUTE**: The documentation claims a run time of about 48 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `Code/Matlab/IC.m`, `Code/Matlab/IC_DGP2.m`, `Code/Matlab/MC_Sim_Study.m`, `Code/Matlab/PLS_group_mod.m`, `Code/Matlab/Timing_script.m`
- **ENVIRONMENT_IMAGE**: The package ships a container definition. A rerun can build it, but image tags and base images must be pinned by digest to be reproducible.
  Evidence: `Dockerfile`
- **UNRESOLVED_PATHS**: 27 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Code/Matlab/MC_Sim_Study.m:100`, `Code/Matlab/MC_Sim_Study.m:107`, `Code/Matlab/Timing_script.m:44`, `Code/R/02_Extract_Simulated_Data.R:43`, `Code/R/05_Timing_Benchmark.R:66`, `Code/R/C_Lasso_Helper_Functions.R:58`, `Code/R/C_Lasso_Helper_Functions.R:63`, `Code/R/C_Lasso_Helper_Functions.R:64`, `Code/R/C_Lasso_Helper_Functions.R:69`, `Code/R/C_Lasso_Helper_Functions.R:70`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: Parallel Computing Toolbox. Each is licensed separately; check the desk's MATLAB has them.
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE.txt`

## What triage looked at

- 67 files, 7,232,924 bytes. Languages: matlab (18), r (13).
- Documentation read: README.md. Licences named: CC BY-NC, CC0, GPL.
- Master scripts: Code/R/01_MC_Simulation_Study.R, Code/R/02_Extract_Simulated_Data.R, Code/R/03_MC_Figures.R, Code/R/04_Empirical_Illustration.R, Code/R/05_Timing_Benchmark.R, Code/R/06_C_Lasso_Comparison.R, Code/R/07_Timing_Table.R, Code/R/08_Empirical_C_Lasso_Comparison.R.
- File reads traced: 51; writes: 23; unresolved paths: 27; missing: df_emp_illustration.xlsx, empirical_coefficients_reference.mat, empirical_verification.json, timing_dgp1_n100_t50.rds, timing_dgp1_n50_t50.rds, timing_summary_dgp_1_k_n50_n100_t50.xlsx.
- Links found: 22; checked: no.
