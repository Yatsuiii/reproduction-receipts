# Local standalone control

An additional clean clone and fresh environment were run using `IndependentCheck.ps1`, without importing or calling the original `harness.py` or `verify.py`.

- Upstream commit: `1ffb923219c636a396c3f749eac7092b00e80e8d`.
- Process exit: `0`.
- Returned F: `5.243655749705594`.
- Returned p: `0.023200326227690037`.
- Scientific CSV SHA-256: `bb7b390027087569e4baa58ab9664fa739aaad9f5e62f41258dcd49ea7bfe0a0`.
- Upstream checkout after execution: clean.
- [Raw CSV](independent-analysis.csv), [captured command log](command.log), [manual verification procedure](../INDEPENDENT_CHECK.md).

This checks a separate execution path on the original operator's machine. It is not independent human review, independent execution by another party, or a completed public CI run. The checksum and this note alone do not authenticate the original runs.
