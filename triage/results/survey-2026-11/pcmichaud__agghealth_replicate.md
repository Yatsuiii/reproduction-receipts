# Triage verdict: BLOCKED

- Package: `pkgs/pcmichaud__agghealth_replicate` at commit `360fec651d2b451d5bc8b2b30f5b1ce7177f3f70`
- Triaged: 2026-11-21T18:16:41Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.479 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 29 blockers, 4 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `CPI.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/old/Table 2 Historical Price Effects.m:66`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPI_de.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:55`
- **MISSING_INPUT_UNDOCUMENTED**: `../agghealth_replicate/data_sources/prices/CPI_dk.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:66`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPI_fr.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:77`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPI_it.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:88`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPI_nl.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:99`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPI_se.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:110`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPI_sp.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:121`
- **MISSING_INPUT_UNDOCUMENTED**: `CPIH.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/old/Table 2 Historical Price Effects.m:69`
- **MISSING_INPUT_UNDOCUMENTED**: `../agghealth_replicate/data_sources/prices/CPIH_de.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:59`
- **MISSING_INPUT_UNDOCUMENTED**: `../agghealth_replicate/data_sources/prices/CPIH_dk.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:70`
- **MISSING_INPUT_UNDOCUMENTED**: `../agghealth_replicate/data_sources/prices/CPIH_fr.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:81`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPIH_it.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:92`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPIH_nl.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:103`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPIH_se.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:114`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/CPIH_sp.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:125`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/xlsx_files/DALY_my_sample.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `post/Figure 3 Health Risks.ipynb:23`, `post/Figure 3 Health Risks.ipynb:25`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/data_regFL.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:178`, `build/old/Table 2 Historical Price Effects.m:137`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/xlsx_files/data_risky_alpha.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `post/Figure 3 Health Risks.ipynb:131`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/prices/DataPriceUS.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 2 Historical Price.ipynb:25`, `build/Table 2 Historical Price.ipynb:27`, `build/old/Table 2 Historical Price Effects.m:21`, `build/old/Table 2 Historical Price Effects.m:25`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/echp/echp_incomes.pkl` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 5 Income Shocks.ipynb:6`
- **MISSING_INPUT_UNDOCUMENTED**: `output/eq_` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `post/Tables 10-11 Welfare.ipynb:27`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/fred/gsy.xls` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Macro Moments.ipynb:48`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/hmd/leatbirth.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 1 Historical Growth.ipynb:6`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/meps/MEPS0004_agghealth.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `post/Figure D2 Health Spending by Income.ipynb:33`, `post/Figure D2 Health Spending by Income.ipynb:102`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/oecd/oecd_history.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 1 Historical Growth.ipynb:5`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/psid/psid_incomes.pkl` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Table 5 Income Shocks.ipynb:65`
- **MISSING_INPUT_UNDOCUMENTED**: `../data_sources/hrs/rndhrs_n.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `build/Preparation HRS.ipynb:3`
- **MISSING_INPUT_UNDOCUMENTED**: `xlsx_files/TFP_data.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `post/Figure D1 Model Fit.py:227`

## Deviations a rerun would have to log

- **PYTHON2_SYNTAX**: 1 Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 interpreter (end of life since 2020) or a port, and either is a logged deviation.
  Evidence: `post/logs/table9-ref.py`
- **NO_DEPENDENCY_SPEC**: Python code imports linearmodels, matplotlib, nlopt, numba, numpy, pandas, scipy, seaborn, statsmodels but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `build/Figure 1 Moments.ipynb`, `build/Health Moments.ipynb`, `build/Macro Moments.ipynb`, `build/Preparation ECHP.ipynb`, `build/Preparation HRS-SHARE.ipynb`
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `build/old/Table 2 Historical Price Effects.m:9`, `build/old/Table 2 Historical Price Effects.m:10`, `build/old/Table 2 Historical Price Effects.m:11`
- **NO_RUN_ORDER**: 61 scripts, no master script, and the README does not name an order. A rerun must choose one and log it.
  Evidence: `build/Figure 1 Moments.ipynb`, `build/Health Moments.ipynb`, `build/Macro Moments.ipynb`, `build/Preparation ECHP.ipynb`, `build/Preparation HRS-SHARE.ipynb`, `build/Preparation HRS.ipynb`, `build/Preparation PSID.ipynb`, `build/Preparation SHARE.ipynb`, `build/Section 2 Static Model with Insurance.ipynb`, `build/Section 2 Static Model.ipynb`

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `build/old/Table 2 Historical Price Effects.m`, `build/old/monthly2annual.m`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: ../estimation/moments/means_health.pkl, ../estimation/moments/means_macro.pkl, ../estimation/moments/stds_health.pkl, ../estimation/moments/stds_macro.pkl, ../model/params/auxiliary.pkl, ../model/params/income_shocks.pkl, /model/params/sim_gdp_us.csv, output/eq_pus_ge3.pkl, output/moms.pkl, output/moms_sim.pkl. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `../estimation/moments/means_health.pkl`, `../estimation/moments/means_macro.pkl`, `../estimation/moments/stds_health.pkl`, `../estimation/moments/stds_macro.pkl`, `../model/params/auxiliary.pkl`, `../model/params/income_shocks.pkl`, `/model/params/sim_gdp_us.csv`, `output/eq_pus_ge3.pkl`, `output/moms.pkl`, `output/moms_sim.pkl`
- **UNRESOLVED_PATHS**: 46 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `build/Macro Moments.ipynb:10`, `build/Macro Moments.ipynb:36`, `build/Preparation ECHP.ipynb:4`, `build/Preparation ECHP.ipynb:9`, `build/Preparation ECHP.ipynb:11`, `build/Preparation ECHP.ipynb:18`, `build/Preparation ECHP.ipynb:25`, `build/Preparation ECHP.ipynb:34`, `build/Preparation PSID.ipynb:4`, `build/Preparation PSID.ipynb:8`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 246 files, 15,350,300 bytes. Languages: matlab (2), python (79), shell (1).
- Documentation read: README.md, estimation/README.md. Licences named: none.
- Master scripts: none.
- File reads traced: 242; writes: 85; unresolved paths: 46; missing: cpi.xlsx, cpi_de.xlsx, cpi_dk.xlsx, cpi_fr.xlsx, cpi_it.xlsx, cpi_nl.xlsx, cpi_se.xlsx, cpi_sp.xlsx, cpih.xlsx, cpih_de.xlsx, cpih_dk.xlsx, cpih_fr.xlsx, cpih_it.xlsx, cpih_nl.xlsx, cpih_se.xlsx, cpih_sp.xlsx, daly_my_sample.xlsx, data_regfl.xlsx, data_risky_alpha.xlsx, datapriceus.xlsx, echp_incomes.pkl, eq_, gsy.xls, leatbirth.dta, meps0004_agghealth.dta, oecd_history.dta, psid_incomes.pkl, rndhrs_n.dta, tfp_data.xlsx.
- Links found: 0; checked: no.
