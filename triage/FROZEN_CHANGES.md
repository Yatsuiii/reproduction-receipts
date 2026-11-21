# Changes to frozen triage files

Every change to a file pinned in `FROZEN.json` is logged here before the registry is updated, with the date, the files, the reason
and whether triage results had already been seen when the change was made.

- 2026-11-21: registry created. Fixtures and `EXPECTED.json` written before `triage.py` existed.
- 2026-11-21, round 2: added five fixtures (`removed_api`, `runtime_fetch`, `cache_via_variable`, `helper_modules`, `python2`) and
  their cases in `EXPECTED.json`. No existing fixture or case changed. Results had been seen: triage v1 was run on frontiers2013
  (the next target in this repository) and missed its committed score caches, its run-time dataset download, its removed
  scikit-learn and NumPy APIs, and counted its helper modules as scripts with no run order. The v1 result is kept in
  `results/frontiers2013.v1.json`. These fixtures were written before the fixes, to fail against v1.
