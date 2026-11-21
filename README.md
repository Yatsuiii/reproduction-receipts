# Reproduction receipts

Small verification runs on third-party scientific code. Each receipt names an upstream commit, identifies the computation and data, records the environment and outputs, and states what the check cannot establish.

## Completed: Pingouin README ANOVA

- Upstream commit: [`1ffb923219c636a396c3f749eac7092b00e80e8d`](https://github.com/raphaelvallat/pingouin/commit/1ffb923219c636a396c3f749eac7092b00e80e8d).
- Two clean clones and separate environments reproduced the README example: F = `5.243655749705594`, p = `0.023200326227690037`.
- Both analysis exits were 0; scientific CSVs and stdout were byte-identical.
- [Full receipt](pingouin/RECEIPT.md), [raw CSV](pingouin/run-1/analysis.csv), [independent verification instructions](INDEPENDENT_CHECK.md), [additional standalone local check](standalone-control/RESULT.md).
- [Public GitHub Actions check](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/42859691077): passed on a fresh Windows runner; [CI evidence and downloaded CSV](CI_RECEIPT.md).

This is one library example, not a neuroimaging paper replication or a complete native-I/O audit. The checksums document bytes; they do not independently prove that a run happened. The public CI procedure avoids the original harness and produces an inspectable execution log and artifact. It is hosted CI corroboration, not independent human scientific review.

## Next target

[A published neuroimaging paper with deprecated APIs and committed score caches](NEXT_TARGET.md). Selection is a preflight decision, not a finding of numerical non-reproduction.

## Also in this repo

Each folder below was its own repository and was merged in with its full history. The original repositories stay up and will be archived rather than deleted, so existing links keep working.

- [`mcp-teardown/`](mcp-teardown/): teardown receipts for published MCP servers, run in bulk.
- [`agent-disclosure-fidelity/`](agent-disclosure-fidelity/): does an agent's report of what it did match what the machine shows. Source of the teardown probe.
- [`custody/`](custody/): source and revocation state on every memory (Vertex AI Memory Bank). Only `main` was merged; the experiment branches stay in the original repository.
- [`stalefence/`](stalefence/): fencing for agents acting on state that changed under them. Was private until this merge.
