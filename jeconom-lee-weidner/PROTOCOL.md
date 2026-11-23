# Protocol, written before any package code ran

Written 2026-11-23 ~18:05 UTC, after reading the package and before running any of its scripts.

Package: the authors' public repository [ATbounds/ATbounds-replication](https://github.com/ATbounds/ATbounds-replication)
at commit `67c2c4d403d3dfbbfa4cfb25f72fe88d7d0f00da` (7 May 2026), for Sokbae Lee and Martin Weidner, "Bounding Treatment
Effects by Pooling Limited Information across Observations", forthcoming in the *Journal of Econometrics*
([arXiv:2111.05243](https://arxiv.org/abs/2111.05243)). This is the authors' repository, not a journal deposit. 15 tracked
files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256).

Why this one: it came out on top of a triage pass over 13 recent author packages (see [`CANDIDATES.md`](CANDIDATES.md)). It
is R, small, seeded, has a written run order, and commits the generated tables, so every printed number can be checked.

## What will run

On two GitHub-hosted machines (`ubuntu-24.04` and `ubuntu-22.04`), each README command in its own fresh clone:

1. The runner's R. If it has none, Ubuntu's `r-base-core` from apt. The README names no R version, so whatever is there is
   used and logged.
2. `install.packages()` of the six packages the README and `check_dependencies.R` name (`ATbounds`, `FNN`, `xtable`,
   `ggplot2`, `sandwich`, `lmtest`), current CRAN versions, using Posit's prebuilt Linux binaries of CRAN to save build time.
   The README pins no versions, so the resolved versions get logged. That is a property of the package, not a deviation. The
   binary mirror is a deviation and is listed.
3. `Rscript check_dependencies.R`, then the five README commands exactly as written, from the repository root, unchanged and
   with no environment variables set (so the Monte Carlo scripts run the full `n_sim = 1000`):
   `MC/Table1_MonteCarlo.R`, `Examples/Table2_RHC.R`, `Examples/Table3_NSW.R`, `MC/AppendixTable_MonteCarloInference.R`,
   `Examples/NSW_main_text.R`.

The NSW scripts download five data files from Rajeev Dehejia's NBER page at run time, as the README says. Those files are
hashed and kept with the evidence so a later reader can tell whether the inputs changed.

## Comparison rule, fixed now

- Each script overwrites its committed output under `Results/`. Each regenerated file is compared with the committed one
  (read with `git show HEAD:`), line by line, by [`compare_results.py`](compare_results.py), committed with this protocol.
- Every printed number is either **exact** (same printed text) or **differs** (reported with both values). Non-numeric text
  must match. A missing or extra line is reported. There is no tolerance band: the tables print 3 to 4 decimals, so a
  difference at that precision is a real difference in the printed value.
- The paper's PDF is not compared. This machine cannot reach the journal, and the committed tables are what the README says
  the package produces. The receipt says so.
- The two machines' outputs are also compared with each other.
- A difference is reported as "the committed materials did not regenerate the committed value in this environment, reason
  unknown", never as an error in the paper.
- Any edit to package code, any extra install, and any failed command goes in the deviations list, in order. Nothing in the
  package is edited.
