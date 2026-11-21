# Held-out review: triage v2 on six journal replication packages

Six author-published packages were pinned in [`HELDOUT.json`](../HELDOUT.json) before triage ran on any of them, then triaged
once with `triage.py` SHA-256 `42fe3acc44ecb384ba61c190862dd5f58ac33d0d2e15650289c1fc23359b63f6`, options
`--have stata,matlab --check-links`. Each verdict was then compared with a hand reading of the package's README and the files
it names. The hand label is a reading, not a run: none of these packages was executed.

Raw verdicts: [`heldout/`](heldout/). Run on 2026-11-21 from a cloud container whose network allows HTTPS only through a proxy;
this matters for the link results below.

## Result

| Package | Journal | Hand label | Triage | Verdict agrees | Main reason right |
|---|---|---|---|---|---|
| Bachas, Gertler, Higgins, Seira | J. Finance | blocked: confidential Bansefi, Banxico, INEGI, Prospera data | blocked | yes | yes |
| Gabaix, Behavioral New Keynesian | AER | runnable with deviations: MATLAB + Dynare, version named only in README | blocked | **no** | no |
| Halpern, Koren, Szeidl, imported inputs | AER | blocked: confidential Hungarian firm data, on-site access | blocked | yes | yes |
| Lagakos, Mobarak, Waugh, migration | Econometrica | runnable with deviations (likely): MATLAB toolbox, Stata, unpinned Python | blocked | **no** | no |
| Janssens, trade and storage | JDE | blocked: GAMS licence for the model; about ten manual downloads for the empirics | blocked | yes | **no** |
| Kirchner et al., insurance zones | JDE | blocked: partner data with private locations | blocked | yes | yes |

- Verdict agrees: **4 of 6**. Verdict and main reason both right: **3 of 6**.
- Cheap baselines on the same six: always-runnable 0/6, readme-and-code 0/6 (every package has both).
- **An always-blocked baseline also scores 4/6.** On this sample, triage's verdict alone is no better than assuming every economics
  package is blocked. What triage adds over that baseline is the reason and the evidence, and on this sample the reason was right
  three times in six. That is the honest size of the result.

## Failures, left as found

These were not fixed in this pull request, by the rule written in `HELDOUT.json` before the run.

1. **Proxy refusals reported as dead data links (Bachas).** Nine `DEAD_DATA_LINK` blockers name openICPSR, CONEVAL, Prospera and
   GitHub URLs that failed with `Tunnel connection failed: 403` or HTTP 403 from this container's proxy. Those links were not shown
   to be dead. The verdict is still right (the confidential data blocks it anyway), but nine of the stated reasons are claims the
   evidence does not support. A network failure must never be reported as a dead link.
2. **Generated outputs read as missing inputs (Gabaix, Waugh).** Dynare writes `<model>_results.mat`, and MATLAB's command syntax
   `save targets.mat x y` was not parsed as a write, so files the code creates were reported as missing. Both verdicts are wrong
   because of this.
3. **Documentation by source rather than file name (Janssens).** `data_sources.md` documents each raw input by dataset and URL
   (BACI, FAOSTAT, FEWS NET, GADM, ...) but not by file name, so triage called 17 inputs undocumented. One was `/etc/redhat-release`,
   which the code reads to detect the operating system.
4. **Missed software.** GAMS (`.gms`, licence required, Janssens) and Google Earth Engine JavaScript (Kirchner) are not in the
   language table. Dynare was detected from `.mod` files but not reported as a requirement.
5. **GPU from a version listing (Waugh).** `GPU_REQUIRED` fired on "GPU Coder" in a pasted MATLAB `ver` listing.
6. **Stata parsing noise (Koren).** `it.do`, `the.do` and `using` were reported as missing inputs; they come from prose and an
   `.ado` argument, not from file reads.

## What would change the verdict next time

A round 3 starts the same way as round 2: one injection per failure above, written before the fix and frozen, then the fix, then a
new held-out set that this round's failures did not inform. These six packages are now development cases.
