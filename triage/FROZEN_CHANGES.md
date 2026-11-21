# Changes to frozen triage files

Every change to a file pinned in `FROZEN.json` is logged here before the registry is updated, with the date, the files, the reason
and whether triage results had already been seen when the change was made.

- 2026-11-21: registry created. Fixtures and `EXPECTED.json` written before `triage.py` existed.
- 2026-11-21, round 2: added five fixtures (`removed_api`, `runtime_fetch`, `cache_via_variable`, `helper_modules`, `python2`) and
  their cases in `EXPECTED.json`. No existing fixture or case changed. Results had been seen: triage v1 was run on frontiers2013
  (the next target in this repository) and missed its committed score caches, its run-time dataset download, its removed
  scikit-learn and NumPy APIs, and counted its helper modules as scripts with no run order. The v1 result is kept in
  `results/frontiers2013.v1.json`. These fixtures were written before the fixes, to fail against v1.
- 2026-11-21, round 3: **changed one existing case.** `external_download --check-links` expected `blocked` with
  `DEAD_DATA_LINK` for a refused connection to 127.0.0.1:9. That expectation encoded the round 2 held-out failure: a refused
  connection, DNS failure or proxy refusal is evidence about this machine's network, not about the link. It now expects
  `runnable-with-deviations` with `DATA_LINK_UNREACHABLE`. Only an HTTP 404 or 410 counts as dead (new `link_status` cases); other
  HTTP errors are `DATA_LINK_UNVERIFIED`. Held-out results had been seen (`results/heldout_review.md`, failure 1).
- 2026-11-21, round 3: added eight fixtures, one or more per held-out failure in `results/heldout_review.md`: `link_status` (1),
  `dynare_model` and `matlab_command_save` (2), `source_listed_data` (3), `gams_model` and `earth_engine` (4), `gpu_listing` (5),
  `stata_prose` (6). Written before the fixes.
- 2026-11-21, round 3b: added `dynare_mod_save` and `stata_macro_dir`. Written after running a v3 draft on the six round 2
  packages (now development cases), which still reported Dynare `.mod` saves, extension-less MATLAB `save('name')` and a Stata
  local-macro directory as missing inputs. Written before the fix.
