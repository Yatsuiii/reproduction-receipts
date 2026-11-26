# Protocol, written before any package code ran

Written 2026-11-26 ~16:55 UTC, after reading the README, `renv.lock` and `scripts/00_utils.R`. The run is driven by
[`spec.json`](spec.json) through [`receiptgen/rerun.py`](../receiptgen/README.md) on a GitHub-hosted `ubuntu-24.04`
runner with R, because this container cannot reach CRAN or NORC.

Package: [olizardo/patriotism-choice-process](https://github.com/olizardo/patriotism-choice-process) at commit `5100bd52fd6854ac27ec8881d11f4ebfa43e8fce`
(13 Nov 2026), for Omar Lizardo, "Patriotism as a Choice Process: National Pride After 9/11", forthcoming in *Social
Psychology Quarterly* (per the package README).

## What will run, unchanged

1. Setup: `install.packages("renv")` then `renv::restore()` from the committed `renv.lock` (which names R 4.5.3; the
   runner has the current R release, recorded).
2. The README's four scripts, in its order: `generate_tables.R`, `generate_descriptives.R`, `generate_figures.R`,
   `supplementary_analysis_footnote2.R`. Each fetches the 1996 and 2004 GSS files from NORC at run time through `gssr`.

## Comparison rule, fixed now

The four committed tables in `Tabs/` are compared with the regenerated ones, number by number, relative tolerance 1e-12,
other text exactly. Figures in `Plots/` are compared by hash only; a PDF differs on metadata alone, so a hash difference is
reported and not read as a difference in the figure. `generate_tables.R` prints its own audit of the statistics quoted in the
manuscript text; that audit is kept in the log and summarised in the notes.

The README warns that NORC may revise the GSS files. A table that differs is reported as "did not regenerate here, reason
unknown", and the run records the GSS files' hashes so a data revision can be told apart from a code or version difference.
The receipt says nothing about whether the paper is right.
