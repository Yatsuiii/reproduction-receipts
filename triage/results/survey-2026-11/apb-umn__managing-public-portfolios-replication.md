# Triage verdict: BLOCKED

- Package: `pkgs/apb-umn__managing-public-portfolios-replication` at commit `b9de92dd229ac162a5fafd4a46c8be17e23ef11e`
- Triaged: 2026-11-21T18:16:41Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.133 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 2 blockers, 3 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `../Data/crsp_return_data.csv` is read by the code but is not in the package, and the documentation (Readme.md) describes it as restricted ("cannot be redistributed"). The desk cannot run this without access.
  Evidence: `Notebooks/optimalportfolio_finitemat_nominal_ABN.ipynb:127`, `Notebooks/optimalportfolio_infinitemat_nominal_heteroskedastic_final.ipynb:132`
- **MISSING_INPUT_UNDOCUMENTED**: `Loadings_finer.csv` is read by the code and named in the documentation (Readme.md), but it is not in the package and no source for it is given.
  Evidence: `Notebooks/optimalportfolio_finitemat_nominal_factormimicking_final.ipynb:962`, `Notebooks/optimalportfolio_infinitemat_nominal_heteroskedastic_final.ipynb:891`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: webcolors<24; xlrd>=2.0.1; setuptools; ipykernel; nbconvert. A rerun installs whatever is current and must log the versions it got.
  Evidence: `Notebooks/requirements.txt`
- **UNDECLARED_DEPENDENCIES**: Python code imports IPython, which no dependency file names.
  Evidence: `Notebooks/optimalportfolio_finitemat_nominal_ABN.ipynb`, `Notebooks/optimalportfolio_finitemat_nominal_factormimicking_final.ipynb`, `Notebooks/optimalportfolio_infinitemat_nominal_heteroskedastic_final.ipynb`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (DataReader). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `Notebooks/optimalportfolio_finitemat_nominal_factormimicking_final.ipynb:51`, `Notebooks/optimalportfolio_infinitemat_nominal_heteroskedastic_final.ipynb:54`

## Notes

- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: Sim_data.csv, Sim_other_series.csv. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `Sim_data.csv`, `Sim_other_series.csv`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 77 files, 30,245,777 bytes. Languages: julia (10), python (3).
- Documentation read: Readme.md. Licences named: none.
- Master scripts: none.
- File reads traced: 36; writes: 23; unresolved paths: 0; missing: crsp_return_data.csv, loadings_finer.csv.
- Links found: 0; checked: no.
