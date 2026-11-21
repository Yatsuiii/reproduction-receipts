# Triage verdict: BLOCKED

- Package: `https://github.com/mwaugh0328/welfare-rural-urban-migration` at commit `573c5bffcb0185f482eca89e7151333ef66a72f9`
- Triaged: 2026-11-21T12:11:27Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.798 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 6 blockers, 3 deviations, 8 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `Choice_Profiles_MailMerge` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `empirical-moments/table-C1/Replication for Table C1.do:90`
- **MISSING_INPUT_UNDOCUMENTED**: `$dof/Figure4.do` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `BCM_econometrica_supplement_files/Do-files/Master Table and Figure Creation.do:77`
- **MISSING_INPUT_UNDOCUMENTED**: `$dof/Figure5.do` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `BCM_econometrica_supplement_files/Do-files/Master Table and Figure Creation.do:81`
- **MISSING_INPUT_UNDOCUMENTED**: `migrate_rates.mat` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `plotting/plot_migration.ipynb:5`
- **MISSING_INPUT_UNDOCUMENTED**: `movepolicy_effecient.mat` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `plotting/plot_policy_functions_effecient.ipynb:9`
- **MISSING_INPUT_UNDOCUMENTED**: `targets.mat` is read by the code and named in the documentation (pe_welfare_analysis/README.md), but it is not in the package and no source for it is given.
  Evidence: `plotting/plot_delta_R.ipynb:5`

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Python code imports matplotlib, numpy, pandas, scipy, seaborn but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `plotting/plot_delta_R.ipynb`, `plotting/plot_migration.ipynb`, `plotting/plot_policy_functions-ols=late.ipynb`, `plotting/plot_policy_functions.ipynb`, `plotting/plot_policy_functions_effecient-old=late.ipynb`
- **STATA_NETWORK_INSTALL**: Do-files install estout, outreg2, outtable from the network at run time, with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.
  Evidence: `empirical-moments/table-A9/Replication for Table A9.do:7`, `empirical-moments/table-C1/Replication for Table C1.do:7`, `empirical-moments/table-C1/Replication for Table C1.do:8`
- **ABSOLUTE_PATH**: 4 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `BCM_econometrica_supplement_files/Do-files/Globals.do:1`, `empirical-moments/Replication.do:10`, `plotting/plot_migration.ipynb:44`, `plotting/plot_migration.ipynb:72`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `BCM_code/Quantitative/Cutoffs.m`, `BCM_code/Quantitative/Induceable.m`, `BCM_code/Quantitative/Plots.m`, `BCM_code/Quantitative/RepeatMigrationIncentive.m`, `BCM_code/Quantitative/RepeatMigrationIncentive_HighSub.m`
- **SOFTWARE_REQUIRED**: Requires Stata (version 12.1, 8 named in code); the desk says it has it.
  Evidence: `BCM_econometrica_supplement_files/Do-files/Appendix Table 13.do`, `BCM_econometrica_supplement_files/Do-files/Appendix Table 2.do`, `BCM_econometrica_supplement_files/Do-files/Appendix Table 5.do`, `BCM_econometrica_supplement_files/Do-files/Appendix Table 6.do`, `BCM_econometrica_supplement_files/Do-files/Appendix Table 8.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: appendix_additive_cost.mat, appendix_cal_perm_movingcost.mat, appendix_cal_subsistence.mat, appendix_cal_subsistence_high.mat, appendix_fix_gamma.mat, appendix_fix_lambda.mat, appendix_fix_rho.mat, appendix_fix_theta.mat, appendix_fix_ubar.mat, cal_ols_same.mat. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `appendix_additive_cost.mat`, `appendix_cal_perm_movingcost.mat`, `appendix_cal_subsistence.mat`, `appendix_cal_subsistence_high.mat`, `appendix_fix_gamma.mat`, `appendix_fix_lambda.mat`, `appendix_fix_rho.mat`, `appendix_fix_theta.mat`, `appendix_fix_ubar.mat`, `cal_ols_same.mat`
- **UNRESOLVED_PATHS**: 16 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `BCM_code/Quantitative/Plots.m:9`, `BCM_code/Quantitative/SavingsAmount.m:9`, `BCM_code/Quantitative/WithSavingsPlots.m:9`, `BCM_code/Quantitative/WithSavingsPlotsUtilityCost.m:8`, `BCM_econometrica_supplement_files/Do-files/Figure3.do:92`, `BCM_econometrica_supplement_files/Do-files/Figure3.do:93`, `BCM_econometrica_supplement_files/Do-files/Figure3.do:164`, `BCM_econometrica_supplement_files/Do-files/Figure3.do:165`, `BCM_econometrica_supplement_files/Do-files/Table 2.do:27`, `empirical-moments/table-5/Replication for Table 5.do:34`
- **LINK_UNVERIFIED**: 4 other links answered with an HTTP error other than 404 or 410, which does not show they are gone: https://github.com/mwaugh0328/welfare-rural-urban-migration/blob/6875e6c7be55c4aa9dc1d770c34affb31a8182dd/calibration/preamble.m#L68 (403), https://github.com/mwaugh0328/final_migration/blob/6875e6c7be55c4aa9dc1d770c34affb31a8182dd/calibration/preamble.m#L68 (403), https://github.com/mwaugh0328/final_migration/blob/bfafac24e1fcb9ee0ccd8122d412a053e69cc210/calibration/preamble.m#L68 (403), https://github.com/mwaugh0328/final_migration/blob/e33c12e76c7da2a210012d082578cbe9d368c965/pe_welfare_analysis/preamble_welfare_analysis.m#L47 (403).
  Evidence: `https://github.com/mwaugh0328/welfare-rural-urban-migration/blob/6875e6c7be55c4aa9dc1d770c34affb31a8182dd/calibration/preamble.m#L68`, `https://github.com/mwaugh0328/final_migration/blob/6875e6c7be55c4aa9dc1d770c34affb31a8182dd/calibration/preamble.m#L68`, `https://github.com/mwaugh0328/final_migration/blob/bfafac24e1fcb9ee0ccd8122d412a053e69cc210/calibration/preamble.m#L68`, `https://github.com/mwaugh0328/final_migration/blob/e33c12e76c7da2a210012d082578cbe9d368c965/pe_welfare_analysis/preamble_welfare_analysis.m#L47`
- **LINK_UNREACHABLE**: 5 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `http://www.waugheconomics.com/uploads/2/2/5/6/22563786/lmw.pdf`, `https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA10489`, `https://www.mathworks.com/help/matlab/ref/fminsearch.html`, `https://www.mathworks.com/help/gads/ga.html`, `https://www.mathworks.com/matlabcentral/fileexchange/8277-fminsearchbnd-fminsearchcon`
- **MATLAB_TOOLBOX**: Documentation names MATLAB toolboxes: Curve Fitting Toolbox, Econometrics Toolbox, Financial Instruments Toolbox, Financial Toolbox, Global Optimization Toolbox, Machine Learning Toolbox, Optimization Toolbox, Parallel Computing Toolbox, Partial Differential Equation Toolbox. Each is licensed separately; check the desk's MATLAB has them.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 725 files, 95,594,448 bytes. Languages: matlab (150), python (6), stata (22).
- Documentation read: BCM_econometrica_supplement_files/Readme.txt, README.md, appendix/README.md, bootstrap/README.md, calibration/README.md, efficient/README.md, empirical-moments/README.md, ge_taxation/README.md, pe_welfare_analysis/README.md, utils/README.md. Licences named: none.
- Master scripts: efficient/make_weights.m.
- File reads traced: 159; writes: 165; unresolved paths: 16; missing: choice_profiles_mailmerge, figure4.do, figure5.do, migrate_rates.mat, movepolicy_effecient.mat, targets.mat.
- Links found: 9; checked: yes.
  - http://www.waugheconomics.com/uploads/2/2/5/6/22563786/lmw.pdf: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://github.com/mwaugh0328/final_migration/blob/6875e6c7be55c4aa9dc1d770c34affb31a8182dd/calibration/preamble.m#L68: FAILED (403)
  - https://github.com/mwaugh0328/final_migration/blob/bfafac24e1fcb9ee0ccd8122d412a053e69cc210/calibration/preamble.m#L68: FAILED (403)
  - https://github.com/mwaugh0328/final_migration/blob/e33c12e76c7da2a210012d082578cbe9d368c965/pe_welfare_analysis/preamble_welfare_analysis.m#L47: FAILED (403)
  - https://github.com/mwaugh0328/welfare-rural-urban-migration/blob/6875e6c7be55c4aa9dc1d770c34affb31a8182dd/calibration/preamble.m#L68: FAILED (403)
  - https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA10489: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.mathworks.com/help/gads/ga.html: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.mathworks.com/help/matlab/ref/fminsearch.html: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.mathworks.com/matlabcentral/fileexchange/8277-fminsearchbnd-fminsearchcon: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
