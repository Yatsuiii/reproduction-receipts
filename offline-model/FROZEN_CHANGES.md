# Changes to frozen files

Every change to a file pinned in `FROZEN.json` is logged here first, with the reason, in the same commit as the registry update.

| Date | Files | Why |
|---|---|---|
| 2026-11-21 | `task/`, `injections/` | First freeze, before any harness code or model run. |
| 2026-11-21 | `MODEL.json`, `requirements.in`, `requirements.lock`, `harness.py`, `runtime_transformers.py`, `fetch_weights.py`, `verify.py`, `baseline.py` | Entry points, weights pin and dependency lock frozen after all 14 injection tests passed and before the first real model run. |
| 2026-11-21 | `clinical/task/` | Second task frozen before its keyword baseline, any harness change, or any model run on it. |

## Incident, 2026-11-21: a second lock appeared

The one-off discover workflow ran again on the push that froze the entry points (its path filter matches the whole PR diff, not the pushed commit) and committed a different lock: nine packages resolved to older versions (anyio 4.14.2 instead of 4.16.0, numpy 2.5.3 instead of 2.5.4, and so on), from the same command four minutes later. `--exclude-newer` did not make the resolution repeatable across the PyPI and PyTorch indexes with `unsafe-best-match`. The frozen check flagged `requirements.lock` as changed. The second lock (sha256 `4846dea9…45a2`) was reverted, the frozen lock (sha256 `c3646b01…78d3`) stands, and the discover workflow was deleted so it cannot run again. Lesson kept in the receipt: a lock is evidence only once committed; re-resolving is not a reproduction.
