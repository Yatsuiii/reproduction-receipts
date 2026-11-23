# Triage verdict: BLOCKED

- Package: `pkgs/pcmichaud__repl_msa_jf` at commit `487849e1733d37c3aa6ff6ccf95432b0af701dea`
- Triaged: 2026-11-21T18:16:38Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.631 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 7 blockers, 9 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `output/estimates_eu.npy` is read by the code and named in the documentation (DATA_AVAILABILITY.md, EXECUTION_GUIDE.md), but it is not in the package and no source for it is given.
  Evidence: `D-model/3b-compute_eu.py:9`
- **MISSING_INPUT_UNDOCUMENTED**: `output/estimates_ez.npy` is read by the code and named in the documentation (DATA_AVAILABILITY.md, EXECUTION_GUIDE.md), but it is not in the package and no source for it is given.
  Evidence: `D-model/1a-compute_estimate_ez.py:16`, `D-model/1b-grid_estimate_ez.py:14`, `D-model/1c-compute_estimate_eu.py:13`, `D-model/2a-compute_gradients.py:16`, `D-model/2b-compute_standard_errors.py:7`
- **MISSING_INPUT_RESTRICTED**: `../output/respondants/pop_sum_age_value.dct` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `C-health dynamics/compas/output/respondants/create_respondants.do:7`, `C-health dynamics/compas/output/spouses/create_spouses.do:7`
- **MISSING_INPUT_RESTRICTED**: `output/sigmas_eu.npy` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `D-model/4b-compute_deltas_eu.py:39`
- **MISSING_INPUT_RESTRICTED**: `output/sigmas_ez.npy` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `D-model/2a-compute_gradients.py:14`, `D-model/2b-compute_standard_errors.py:5`, `D-model/4-compute_deltas.py:39`, `tables/table 8 NLLS structural parameters estimates.py:8`
- **MISSING_INPUT_RESTRICTED**: `simpopfull-1.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `C-health dynamics/3-merge compas replications.do:50`
- **MISSING_INPUT_RESTRICTED**: `sp_simpopfull-1.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("Confidential"), so it is most likely one of those.
  Evidence: `C-health dynamics/3-merge compas replications.do:108`

## Deviations a rerun would have to log

- **PYTHON2_SYNTAX**: 1 Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 interpreter (end of life since 2020) or a port, and either is a logged deviation.
  Evidence: `B-auxiliary/1-Tax Function Construction.ipynb`
- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: linearmodels; matplotlib; nlopt; numba; numpy; pandas; scipy; statsmodels. A rerun installs whatever is current and must log the versions it got.
  Evidence: `requirements-frozen.txt`, `requirements.txt`
- **UNDECLARED_DEPENDENCIES**: Python code imports srd, which no dependency file names.
  Evidence: `A-survey/1-Survey to Analysis Sample.ipynb`, `A-survey/2-Export Inputs for Model.ipynb`, `A-survey/3-Prepare For Health Dynamics Estimation.ipynb`, `B-auxiliary/1-Tax Function Construction.ipynb`, `B-auxiliary/2-Calibrated Auxiliary Parameters.ipynb`
- **MISSING_INPUT_DOWNLOAD**: `../raw/clean_edm2009.dta` is not in the package; the documentation (DATA_AVAILABILITY.md) says to download it from https://www150.statcan.gc.ca/n1/en/catalogue/62M0004X2009000. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `B-auxiliary/4-Medical Expenses Cailbration.ipynb:5`, `https://www150.statcan.gc.ca/n1/en/catalogue/62M0004X2009000`
- **MISSING_INPUT_DOWNLOAD**: `../raw/gss-12M0015-E-2002-c-16-cr_F1.dta` is not in the package; the documentation (DATA_AVAILABILITY.md) says to download it from https://odesi.ca/. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `B-auxiliary/4-Medical Expenses Cailbration.ipynb:53`, `https://odesi.ca/`
- **MISSING_INPUT_DOWNLOAD**: `../raw/gss-12M0015-E-2002-c-16-m_F1.dta` is not in the package; the documentation (DATA_AVAILABILITY.md) says to download it from https://odesi.ca/. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `B-auxiliary/4-Medical Expenses Cailbration.ipynb:118`, `https://odesi.ca/`
- **MISSING_INPUT_DOWNLOAD**: `../raw/p16i6.dta` is not in the package; the documentation (DATA_AVAILABILITY.md) says to download it from https://www.federalreserve.gov/econres/scf_2016.htm, https://www.federalreserve.gov/econres/scf_2016.htm. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `B-auxiliary/2-Calibrated Auxiliary Parameters.ipynb:25`, `https://www.federalreserve.gov/econres/scf_2016.htm`, `https://www.federalreserve.gov/econres/scf_2016.htm`
- **MISSING_INPUT_DOWNLOAD**: `../raw/SFS-13M0006-E-2016_F1.dta` is not in the package; the documentation (DATA_AVAILABILITY.md) says to download it from https://www150.statcan.gc.ca/n1/pub/13m0006x/2021001/SFS2016-eng.zip, https://www150.statcan.gc.ca/n1/pub/13m0006x/2021001/SFS2016-eng.zip. The download date and the file's SHA-256 become part of the receipt; links were not checked (use --check-links).
  Evidence: `B-auxiliary/2-Calibrated Auxiliary Parameters.ipynb:8`, `B-auxiliary/2-Calibrated Auxiliary Parameters.ipynb:48`, `https://www150.statcan.gc.ca/n1/pub/13m0006x/2021001/SFS2016-eng.zip`, `https://www150.statcan.gc.ca/n1/pub/13m0006x/2021001/SFS2016-eng.zip`
- **LONG_COMPUTE**: The documentation claims a run time of about 160 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata (version 0.12, 0.13, 10.0, 11, 11.0, 13.1, 6.0, 7.0, 8, 8.0, 8.2, 9.2 named in code); the desk says it has it.
  Evidence: `C-health dynamics/3-merge compas replications.do`, `C-health dynamics/compas/ado/plus/_/_eststo.ado`, `C-health dynamics/compas/ado/plus/c/cmp.ado`, `C-health dynamics/compas/ado/plus/c/cmp_clear.ado`, `C-health dynamics/compas/ado/plus/c/cmp_d1.ado`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: ../C-health dynamics/compas/data/input/key_id_r.dta, ../C-health dynamics/compas/data/input/key_id_sp.dta, ../D-model/inputs/benefits.csv, ../D-model/inputs/hcare_costs.csv, ../D-model/inputs/house_prices_real.csv, ../D-model/inputs/hp.csv, ../D-model/inputs/hp_sp.csv, ../D-model/inputs/know.csv, ../D-model/inputs/ncare_costs.csv, ../D-model/inputs/other_vars.csv. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `../C-health dynamics/compas/data/input/key_id_r.dta`, `../C-health dynamics/compas/data/input/key_id_sp.dta`, `../D-model/inputs/benefits.csv`, `../D-model/inputs/hcare_costs.csv`, `../D-model/inputs/house_prices_real.csv`, `../D-model/inputs/hp.csv`, `../D-model/inputs/hp_sp.csv`, `../D-model/inputs/know.csv`, `../D-model/inputs/ncare_costs.csv`, `../D-model/inputs/other_vars.csv`
- **UNRESOLVED_PATHS**: 33 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `C-health dynamics/3-merge compas replications.do:16`, `C-health dynamics/3-merge compas replications.do:28`, `C-health dynamics/3-merge compas replications.do:59`, `C-health dynamics/3-merge compas replications.do:74`, `C-health dynamics/3-merge compas replications.do:86`, `C-health dynamics/3-merge compas replications.do:117`, `C-health dynamics/compas/ado/plus/p/parallel.ado:302`, `C-health dynamics/compas/ado/plus/p/parallel.ado:328`, `C-health dynamics/compas/ado/plus/p/parallel.ado:429`, `C-health dynamics/compas/ado/plus/p/parallel.ado:432`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `C-health dynamics/compas/libs/statamod/COPYING.txt`

## What triage looked at

- 2777 files, 133,675,979 bytes. Languages: fortran (106), python (66), shell (5), stata (25).
- Documentation read: C-health dynamics/README.md, C-health dynamics/compas/libs/compaslib/readme, C-health dynamics/compas/libs/statamod/README.txt, D-model/logs/README.md, D-model/output/README.md, DATA_AVAILABILITY.md, EXECUTION_GUIDE.md, Python Requirements.md, README.md. Licences named: CC BY-NC, CC0, GPL.
- Master scripts: none.
- File reads traced: 179; writes: 117; unresolved paths: 33; missing: clean_edm2009.dta, estimates_eu.npy, estimates_ez.npy, gss-12m0015-e-2002-c-16-cr_f1.dta, gss-12m0015-e-2002-c-16-m_f1.dta, p16i6.dta, pop_sum_age_value.dct, sfs-13m0006-e-2016_f1.dta, sigmas_eu.npy, sigmas_ez.npy, simpopfull-1.dta, sp_simpopfull-1.dta.
- Links found: 15; checked: no.
