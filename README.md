# Reproduction receipts

Small verification runs on third-party scientific code. Each receipt names an upstream commit, identifies the computation and data, records the environment and outputs, and states what the check cannot establish.

## Completed: Pingouin README ANOVA

- Upstream commit: [`1ffb923219c636a396c3f749eac7092b00e80e8d`](https://github.com/raphaelvallat/pingouin/commit/1ffb923219c636a396c3f749eac7092b00e80e8d).
- Two clean clones and separate environments reproduced the README example: F = `5.243655749705594`, p = `0.023200326227690037`.
- Both analysis exits were 0; scientific CSVs and stdout were byte-identical.
- [Full receipt](pingouin/RECEIPT.md), [raw CSV](pingouin/run-1/analysis.csv), [independent verification instructions](INDEPENDENT_CHECK.md), [additional standalone local check](standalone-control/RESULT.md).

This is one library example, not a neuroimaging paper replication or a complete native-I/O audit. The checksums document bytes; they do not independently prove that a run happened. The independent procedure avoids the original harness. Public CI has not run yet.

## Next target

[A published neuroimaging paper with deprecated APIs and committed score caches](NEXT_TARGET.md). Selection is a preflight decision, not a finding of numerical non-reproduction.
