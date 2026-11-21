# Changes to frozen files

Every change to a file pinned in `FROZEN.json` is logged here first, with the reason, in the same commit as the registry update.

| Date | Files | Why |
|---|---|---|
| 2026-11-21 | `task/`, `injections/` | First freeze, before any harness code or model run. |
| 2026-11-21 | `MODEL.json`, `requirements.in`, `requirements.lock`, `harness.py`, `runtime_transformers.py`, `fetch_weights.py`, `verify.py`, `baseline.py` | Entry points, weights pin and dependency lock frozen after all 14 injection tests passed and before the first real model run. |
