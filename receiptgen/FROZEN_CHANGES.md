# Frozen file changes

Every change to a file pinned in `FROZEN.json` is logged here, with the reason, in the same commit as the registry update.

- 2026-11-25: registry created. 13 failure injections and `EXPECTED.json` committed before `rerun.py` existed.
- 2026-11-25: entry points `rerun.py` and `run_fixtures.py` pinned after they passed 13/13. Same day, before any real
  package ran: `rerun.py` gained outputs given as `{"glob": ..., "compare": "hash-only"}`, for figures whose bytes carry
  metadata (class `rewritten-not-compared`, never counted as reproduced). No fixture or expected outcome changed; the
  fixtures were re-run after the change, 13/13.
- 2026-11-25: added fixture `converted_binary` and its expected outcome, before `rerun.py` supported converters. Needed for R `.rds` outputs, whose header records the R version that wrote them.
- 2026-11-25: `rerun.py` gained per-output converters; 14/14 after the change, `results/fixtures.json` regenerated.
- 2026-11-25: spec `environment_commands` now run after the package commands, so versions a setup command installs are the ones recorded. 14/14 after the change.
