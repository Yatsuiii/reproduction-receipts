# Public CI corroboration

**Result: PASS.** A fresh GitHub-hosted Windows runner cloned the pinned upstream repository, installed the recorded upstream-derived dependencies into a new environment, ran the README ANOVA example without the original harness, and produced the same scientific CSV bytes.

- [Public workflow run 42859691077](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/42859691077).
- Bundle commit actually executed: [`a000d24b0939f3e92cfb4544b13211605cbea8e4`](https://github.com/Yatsuiii/reproduction-receipts/commit/a000d24b0939f3e92cfb4544b13211605cbea8e4).
- [Executed workflow](https://github.com/Yatsuiii/reproduction-receipts/blob/a000d24b0939f3e92cfb4544b13211605cbea8e4/.github/workflows/independent-check.yml) and [executed standalone command script](https://github.com/Yatsuiii/reproduction-receipts/blob/a000d24b0939f3e92cfb4544b13211605cbea8e4/IndependentCheck.ps1).
- Upstream: `raphaelvallat/pingouin`, commit `1ffb923219c636a396c3f749eac7092b00e80e8d`.
- GitHub job conclusion: `success`. The script checks the analysis process exit code, upstream entry-point hash, output CSV hash and clean upstream checkout.
- Python `3.12.10`; uv `0.12.24`; identical dependency lockfiles.
- Scientific output: [downloaded original CI CSV](ci/independent-analysis.csv).
- CSV SHA-256: `bb7b390027087569e4baa58ab9664fa739aaad9f5e62f41258dcd49ea7bfe0a0`.
- Full-precision Group F: `5.243655749705594`; p: `0.023200326227690037`.
- [Captured public Actions log](ci/command.log) and [GitHub run metadata](ci/run.json).

The workflow never imports or invokes `pingouin/harness.py` or `pingouin/verify.py`. The CI artifact was downloaded through `gh run download` and hashed separately with Python's standard-library SHA-256 implementation; it matched the two local original outputs and the standalone local control byte-for-byte.

The job's analysis step also includes upstream clone and dependency installation. It is not a separately measured scientific-analysis wall time. The original receipt contains the separately measured local process times.

## What this establishes

The displayed README statistic can be reproduced on a separate hosted machine using the pinned source and recorded dependency versions. Readers can inspect public execution logs, retrieve the raw artifact while GitHub retains it, compare the preserved downloaded CSV, or run the short [manual commands](INDEPENDENT_CHECK.md) themselves.

The workflow is authored by this project's operator. This is hosted CI corroboration, not independent human scientific review or a signed attestation of the earlier local runs. It does not validate the whole package, a neuroimaging paper, or native OS-level input tracing. The original local receipt and its checksum index remain unmodified; this file records the later CI event separately.
