# Next target: Miyawaki decoding in a published neuroimaging paper

**Status: selected and inspected; no reproduction attempt has run.** No claim of incorrect published numbers is made.

- Paper: Abraham et al. (2014), [Machine learning for neuroimaging with scikit-learn](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2014.00014/full), DOI `10.3389/fninf.2014.00014`.
- Author repository: [AlexandreAbraham/frontiers2013](https://github.com/AlexandreAbraham/frontiers2013).
- Inspected commit: `97bf25836804195401ef213f963135957b431d70`.
- Entry point: [`scripts/miyawaki_decoding.py`](https://github.com/AlexandreAbraham/frontiers2013/blob/97bf25836804195401ef213f963135957b431d70/scripts/miyawaki_decoding.py).
- Target: the per-pixel, five-fold reconstruction-accuracy results used by the paper's Miyawaki decoding panels. Compare raw score arrays, not PDF byte identity, which can differ for non-scientific metadata reasons.
- Preflight hashes: [`next-target/PREFLIGHT.json`](next-target/PREFLIGHT.json).

## Why this target deserves a check

1. **The README identifies this repository as unmaintained.** It directs readers to the maintained Nilearn library. That is an environment-reconstruction concern, not evidence that the original analysis was wrong.
2. **The script imports historical APIs.** Examples in the inspected source include `sklearn.cross_validation`, `sklearn.externals.joblib`, `sklearn.datasets.base.Bunch`, NumPy's `np.int`/`np.float` aliases, and old nibabel accessors. These raise a concrete compatibility question for an unmodified run today.
3. **A clean checkout already contains result caches.** `scripts/miyawaki/lr_scores.npy`, `svc_scores.npy` and `svcl2_scores.npy` are committed arrays, each shaped `(100, 5)`. The script only computes cross-validation scores when those paths do not exist. A successful unmodified run can therefore read the old arrays rather than recompute them. A repeated output hash alone would not demonstrate fresh score computation.
4. **The checkout has no machine-readable dependency specification or lockfile.** The paper names scientific libraries, but the exact original environment is not specified in this checkout. Installing an arbitrary modern environment and observing an import error would establish that environment's execution failure, not a numerical contradiction of the paper.

## What a future receipt must distinguish

- **Environment failure:** dependency installation or import fails. Preserve logs and stop. Do not call this a failed scientific finding.
- **Cache replay:** the script reads committed score arrays without executing the scoring branch. Label it replay, even if output hashes match.
- **Fresh recomputation:** score arrays were generated from the raw data by the upstream scoring path. Only then compare the scientific results with the committed arrays/figure.
- **Numerical disagreement:** preserve the produced arrays, exact compared cells, dependency/data hashes and the predeclared comparison rule. Do not infer it from a visual difference between PDFs.

The original as-is check must leave committed caches intact. Removing caches, forcing branches, porting APIs, choosing replacement data URLs or constructing an undocumented environment would be deviations requiring an explicit separate protocol. None has been done.

This is a candidate for testing whether the harness can expose a provenance or execution problem. It has not yet supplied a failing run or a numerical non-reproduction. No model weights have been downloaded or used.
