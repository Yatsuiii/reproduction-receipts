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
- 2026-11-25: added fixtures `replay_from_intermediate` and `intermediate_regenerated`, before the fix. Found on the first real run (Conlon and Rao, JPE): Tables 6 to 8 were counted as reproduced although the step that writes the intermediates they read had failed, so they were formatted from committed `results/*.parquet`.
- 2026-11-25: `rerun.py` traces reads of `committed_intermediates` with strace and does not count outputs formatted from them; 16/16 after the fix, `results/fixtures.json` regenerated.
- 2026-11-25: `rerun.py` resolves `--out` and `--workdir` to absolute paths. Run 2 of the JPE receipt first started with a relative `--out`, and strace, which runs inside the checkout, could not open its trace file, so every command failed in 0 s. That attempt was a fault of this tool, not the package, and its directory was deleted. 16/16 after the fix.
- 2026-11-25: `rerun.py`: text-differs outputs with the same count of numbers now also list number differences (the Assemblage `.rds` files differ in a stored R version string and in some numbers, and v1 reported only the first); `--render` re-renders a receipt from results.json with post-run notes under their own heading; Windows-safe process handling. 16/16.
- 2026-11-25: `rerun.py` takes the shell from `RECEIPTGEN_BASH` (default `bash`). The first Windows run of the Assemblage spec failed in 0 s because `bash` resolved to the WSL stub; that run was a fault of this tool, and its directory was deleted. 16/16.
