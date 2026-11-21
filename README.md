# Reproduction receipts

Small verification runs on third-party scientific code. Each receipt names an upstream commit, identifies the computation and data, records the environment and outputs, and states what the check cannot establish.

## Completed: Pingouin README ANOVA

- Upstream commit: [`1ffb923219c636a396c3f749eac7092b00e80e8d`](https://github.com/raphaelvallat/pingouin/commit/1ffb923219c636a396c3f749eac7092b00e80e8d).
- Two clean clones and separate environments reproduced the README example: F = `5.243655749705594`, p = `0.023200326227690037`.
- Both analysis exits were 0; scientific CSVs and stdout were byte-identical.
- [Full receipt](pingouin/RECEIPT.md), [raw CSV](pingouin/run-1/analysis.csv), [independent verification instructions](INDEPENDENT_CHECK.md), [additional standalone local check](standalone-control/RESULT.md).
- [Public GitHub Actions check](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/42859691077): passed on a fresh Windows runner; [CI evidence and downloaded CSV](CI_RECEIPT.md).

This is one library example, not a neuroimaging paper replication or a complete native-I/O audit. The checksums document bytes; they do not independently prove that a run happened. The public CI procedure avoids the original harness and produces an inspectable execution log and artifact. It is hosted CI corroboration, not independent human scientific review.

## Package triage

[`triage/`](triage/README.md) decides in about a second whether a replication package can run at all, and why not, before a rerun is attempted. On six held-out journal packages its verdict agreed with a hand reading 4 times in 6, the same as assuming every package is blocked; its stated reason was right 3 times in 6. [Review, with every failure](triage/results/heldout_review.md).

## Offline model receipt

[`offline-model/`](offline-model/README.md): an open-weight model (Qwen2.5-1.5B-Instruct, Apache-2.0) scored a frozen 60-line task on CPU with no network interface but `lo`, on two fresh GitHub machines with different CPUs. Predictions were byte-identical and a third clean checkout re-verified both. The model got 42/60; a regular expression got 53/60, and the README says so first. A [second receipt](offline-model/clinical/README.md) on a clinical judgement task: Qwen3-4B got 58/60 against 50/60 for a keyword rule, reproduced on two machines; the 1.5B model got 45/60.

## Next target

[A published neuroimaging paper with deprecated APIs and committed score caches](NEXT_TARGET.md). Selection is a preflight decision, not a finding of numerical non-reproduction.

## Also in this repo

Each folder below was its own repository and was merged in with its full history. The original repositories stay up and will be archived rather than deleted, so existing links keep working.

- [`mcp-teardown/`](mcp-teardown/): teardown receipts for published MCP servers, run in bulk.
- [`agent-disclosure-fidelity/`](agent-disclosure-fidelity/): does an agent's report of what it did match what the machine shows. Source of the teardown probe.
- [`custody/`](custody/): source and revocation state on every memory (Vertex AI Memory Bank). Only `main` was merged; the experiment branches stay in the original repository.
- [`stalefence/`](stalefence/): fencing for agents acting on state that changed under them. Was private until this merge.
