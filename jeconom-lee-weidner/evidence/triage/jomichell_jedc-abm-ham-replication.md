# Triage verdict: BLOCKED

- Package: `pk/jomichell_jedc-abm-ham-replication` at commit `a8aa69344fc9bc491e7356e8ae11937ad7570020`
- Triaged: 2026-11-23T17:48:01Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.015 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 1 blockers, 2 deviations, 0 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `path/to/compustat_annual.csv` is read by the code but is not in the package, and the documentation (replication_notes.txt) describes it as restricted ("WRDS"). The desk cannot run this without access.
  Evidence: `replicate_moments.R:72`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: R code loads boot, dplyr, fredr, tibble with no renv.lock. A rerun installs current CRAN versions and must log them.
  Evidence: `replicate_moments.R:25`, `replicate_moments.R:26`, `replicate_moments.R:27`, `replicate_moments.R:28`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (fredr). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `replicate_moments.R:304`

## What triage looked at

- 9 files, 35,397 bytes. Languages: r (3).
- Documentation read: README.md, replication_notes.txt. Licences named: MIT.
- Master scripts: replicate_moments.R.
- File reads traced: 2; writes: 0; unresolved paths: 0; missing: compustat_annual.csv.
- Links found: 2; checked: no.
