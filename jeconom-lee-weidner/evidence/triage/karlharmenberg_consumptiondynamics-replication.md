# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/karlharmenberg_consumptiondynamics-replication` at commit `dac46ace39dd93f35010f8fd74c8be0cd9159dd7`
- Triaged: 2026-11-23T17:48:01Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.384 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 2 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: - numpy>=2.0; - scipy>=1.14; - numba>=0.60; - pandas>=2.2; - statsmodels>=0.14; - patsy>=1.0; - matplotlib>=3.9; - scikit-learn>=1.5; - tabulate>=0.9; - quantecon>=0.10. A rerun installs whatever is current and must log the versions it got.
  Evidence: `environment.yml`, `requirements.txt`
- **ABSOLUTE_PATH**: 4 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `code/tables/generate_all_tables.py:229`, `code/tables/generate_all_tables.py:231`, `code/tables/generate_all_tables.py:272`, `code/tables/generate_all_tables.py:280`

## Notes

- **UNRESOLVED_PATHS**: 13 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/empirical/02_us_gdp_footnote.py:38`, `code/empirical/02_us_gdp_footnote.py:39`, `code/empirical/lib/shiw_data.py:122`, `code/empirical/lib/shiw_data.py:123`, `code/empirical/lib/shiw_data.py:124`, `code/empirical/lib/shiw_data.py:125`, `code/empirical/lib/shiw_data.py:126`, `code/empirical/lib/shiw_data.py:127`, `code/empirical/lib/shiw_data.py:128`, `code/empirical/lib/shiw_data.py:133`
- **RESTRICTED_DATA_MENTIONED**: The documentation mentions restricted data ("Confidential") but every input triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **NONCOMMERCIAL_LICENCE**: Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should not redistribute the package's files.
  Evidence: `LICENSE.txt`

## What triage looked at

- 488 files, 81,842,865 bytes. Languages: python (29), shell (2).
- Documentation read: README.md, data/README_data.md, output/logs/verification_report.md. Licences named: CC BY-NC, CC0, MIT.
- Master scripts: code/empirical/01_labormarket_oecd.py, code/empirical/02_us_gdp_footnote.py, code/empirical/03_shiw_baseline.py, code/empirical/04_shiw_robustness_curves.py, code/empirical/05_shiw_probit.py, code/empirical/06_shiw_time_region_fe.py, run_all.sh.
- File reads traced: 17; writes: 22; unresolved paths: 13; missing: none.
- Links found: 12; checked: no.
