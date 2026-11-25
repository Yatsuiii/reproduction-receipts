# Frozen file changes

Every change to a file pinned in `FROZEN.json` is logged here, with the reason, in the same commit as the registry update.

- 2026-11-25: registry created. 13 failure injections and `EXPECTED.json` committed before `rerun.py` existed.
- 2026-11-25: entry points `rerun.py` and `run_fixtures.py` pinned after they passed 13/13. Same day, before any real
  package ran: `rerun.py` gained outputs given as `{"glob": ..., "compare": "hash-only"}`, for figures whose bytes carry
  metadata (class `rewritten-not-compared`, never counted as reproduced). No fixture or expected outcome changed; the
  fixtures were re-run after the change, 13/13.
