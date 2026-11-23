# Candidates for the third unasked receipt, 23 Nov 2026

How the list was made: GitHub repository search for recent (pushed in 2025-2026) Python, R and Julia repositories whose
README mentions a replication package and a journal, or "forthcoming" or "accepted". That gave about 650 hits, mostly course
projects and templates. 13 looked like an author's own package for a named paper. Each was cloned at its current commit and
run through [`triage/triage.py`](../triage/triage.py) as it is (v2, parked on 21 Nov because it did not clearly beat "assume
blocked" on held-out packages, so its verdicts here are a first filter, not evidence). Then I read each README.

Not considered: packages hosted on Zenodo, openICPSR or Dataverse, which this machine cannot reach; Stata or MATLAB packages
(proprietary software); and the JPE-Reproducibility organisation, which is the JPE desk's own work in progress.

| Package | Journal (as the README states it) | Lang | Triage verdict | What decided it |
|---|---|---|---|---|
| [ATbounds/ATbounds-replication](https://github.com/ATbounds/ATbounds-replication) | Journal of Econometrics, forthcoming | R | runnable-with-deviations (unpinned CRAN, NSW data downloaded at run time) | **Picked.** Seeded, written run order, committed tables to compare against, small |
| [marcburri/nowcasting-simple-news](https://github.com/marcburri/nowcasting-simple-news) | Oxford Bulletin of Economics and Statistics, forthcoming | R | runnable-with-deviations (unpinned, absolute path) | Good second. Committed results; the long forecasting step is optional |
| [ballesterogh/algorithmic-collusion-IJIO-replication-code](https://github.com/ballesterogh/algorithmic-collusion-IJIO-replication-code) | Int. J. of Industrial Organization 106 (2026) | Julia | runnable-with-deviations (no Project.toml, absolute path) | IJIO has a data editor, which makes it the most relevant desk. Simulation outputs (GBs) not included, long compute |
| [karlharmenberg/consumptiondynamics-replication](https://github.com/karlharmenberg/consumptiondynamics-replication) | J. of Monetary Economics 118 (2021) | Python | runnable-with-deviations | 2021 paper; README says the package was rebuilt from old code by an AI agent in 2026, so a rerun checks the rebuild, not the original |
| [korobkay/orthoset](https://github.com/korobkay/orthoset) | not stated (cites Semenova 2023, J. of Econometrics, for the data) | Python | runnable-with-deviations (no dependency file) | No journal named. Reading the code: `common.py` expects `code/` and `data/` folders, but the repo is flat, so the README commands as written look for `../data/cps2015.csv` |
| [mdcattaneo/replication-CFS_2026_AOS](https://github.com/mdcattaneo/replication-CFS_2026_AOS) | Annals of Statistics, forthcoming | Python | runnable-with-deviations | Statistics journal, simulations only |
| [mdcattaneo/replication-CJN_2026_ET](https://github.com/mdcattaneo/replication-CJN_2026_ET) | Econometric Theory (2026) | R + C++ | runnable-with-deviations | Built for a SLURM cluster |
| [yonathanarbel/generative-reasonable-person](https://github.com/yonathanarbel/generative-reasonable-person) | law review, forthcoming | Python | runnable-with-deviations | Calls LLM APIs |
| [thimodeschouwer/replication-meaningflexibilitypuzzle](https://github.com/thimodeschouwer/replication-meaningflexibilitypuzzle) | not checked | R | runnable-with-deviations (4 inputs only listed by source) | Inputs must be fetched by hand |
| [jomichell/jedc-abm-ham-replication](https://github.com/jomichell/jedc-abm-ham-replication) | J. of Economic Dynamics and Control, accepted | R | blocked (restricted input) | |
| [coadywing/infant-drug-testing-replication](https://github.com/coadywing/infant-drug-testing-replication) | Demography | R | blocked (restricted inputs) | |
| [zweitstimme-org/stacking-election-forecasts-replication](https://github.com/zweitstimme-org/stacking-election-forecasts-replication) | Political Analysis | R + Stata | blocked (Stata, restricted inputs) | |
| [haukelicht/validating_opensource_mt](https://github.com/haukelicht/validating_opensource_mt) | Political Science Research and Methods | Python + R | blocked (inputs, GPU) | |

Triage verdicts and findings per package are in [`evidence/triage/`](evidence/triage/).
