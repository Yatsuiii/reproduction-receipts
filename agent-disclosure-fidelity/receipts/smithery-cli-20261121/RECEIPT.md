# Receipt: smithery-cli uplink teardown, re-run 2026-11-21

Re-run in this checkout of reproduction-receipts (main at merge of PR #1, `c08743a`), not carried over
from the September run in DISCOVERY.md.

- SUT: `arcadeai-labs/smithery-cli` at `407ac3b33944a585357379bc213fdf1ee55464d7` (release 1.2.0). On
  2026-11-21 `git log 407ac3b..origin/HEAD` is empty, so this is still the default branch.
- Fixture server: built from `modelcontextprotocol/typescript-sdk` at `b65426158ed9f29aea8ef3dc09ca22d7d9d6f970`
  (core and server packages).
- `pytest tests/test_discovery_smithery_cli.py -v`: 4 passed in 307.60 s (negative control trips; arms 10/10
  both directions; broken control FAIL with the grandchild as residue; fixed control PASS).
- `record.py` (this folder): 10 trials per control, written to `trials.json`.

| Control | Verdict | Trials with residue | `close()` returned after | Wall clock |
|---|---|---:|---|---:|
| unpatched | fail | 10 / 10 | 10.008 to 10.010 s | 138.6 s |
| constructed process-group patch | pass | 0 / 10 | 6.04 to 6.99 s | 70.8 s |

The patched arm took 6 to 7 s, not the ~5 s DISCOVERY.md states: the wrapper does not exit on stdin
EOF, so the group SIGTERM lands after the first 5 s window. Reported as measured.

Environment: Linux-6.18.44 x86_64, glibc 2.39, Intel Xeon @ 2.10 GHz, 4 vCPU, 15.7 GB; node v22.23.5;
pnpm 10.26.1 (typescript-sdk) and 10.27.0 (smithery-cli); Python 3.13.18; pytest 9.2.0. Cloud
container, no paid API or model calls, marginal cash cost $0.

Deviations: installs used `--ignore-scripts` with only esbuild rebuilt (as `sut.py` does); the
wrapper is `adapters/typescript_sdk/fixtures/wrapper.mjs`, not real `npx`; the relay is the in-process
mock in `adapters/smithery_cli/fixtures/mockRelay.mjs`.

Prior art, 2026-11-21: issue search on the repo for orphan, zombie, child process, uplink, process
group, SIGKILL, close hang. Hits are #779 (registry ID state), #680 (TTY prompt hang) and per-server
bug reports; none covers this.

Draft issue text: `ISSUE_DRAFT.md`. Not posted.
