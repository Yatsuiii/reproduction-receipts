# Protocol, written before any package code ran

Written 2026-11-25 ~17:37 UTC, after reading the README and the one R script. The run is driven by
[`spec.json`](spec.json) through [`receiptgen/rerun.py`](../receiptgen/README.md) on a GitHub-hosted `ubuntu-24.04` runner
(this container cannot reach CRAN), listed in `.github/receipt-queue` with `#r`.

Package: [mdcattaneo/replication-CMMS_2020_JPE](https://github.com/mdcattaneo/replication-CMMS_2020_JPE) at commit
`d307dcdc7e9d8982eda70196b10d2af2907b4be2` (28 May 2023), for Cattaneo, Ma, Masatlioglu and Suleymanov, "A Random
Attention Model", *JPE* 128(7), 2020.

## What will run

1. Setup: `install.packages("ramchoice")` from CRAN, current version, recorded by the environment command.
2. `Rscript Cattaneo-Ma-Masatlioglu-Suleymanov_2020_JPE.R`, unchanged: 1,000 simulated datasets, seed 42, the GMS
   critical value at level 0.05, five preference hypotheses. The script says it takes 10 to 20 minutes.

R is the runner's current release (installed by `r-lib/actions/setup-r`).

## Comparison rule, fixed now

The script writes no file, so `rerun.py` records only exit code, log and time. The script's own comment block (committed in
the package) states the final result:

| Hypothesis | Empirical rejection rate |
|---|---|
| 1, 2, 3, 4, 5 (null) | 0.000 |
| 2, 3, 4, 5, 1 (null) | 0.004 |
| 3, 4, 5, 2, 1 (alternative) | 0.144 |
| 4, 5, 3, 2, 1 (alternative) | 0.275 |
| 5, 4, 3, 2, 1 (alternative) | 0.351 |

The five printed `colMeans(result)` values are compared with this table, after rounding to three decimals, by hand. Each
matches or does not; a mismatch is listed with both values as "did not regenerate here, reason unknown". The rates are
counts out of 1,000, so a difference of one repetition shows as 0.001.

These are the script's comments, not the paper's table; whether the paper prints the same rates was not checked from this
machine. The receipt does not say whether the paper is right. It says what the committed materials did on this machine.

## Addendum, 2026-11-25 ~18:05 UTC, after run 1

Run 1 ([`runs/github-45666704089-linux/`](runs/github-45666704089-linux/RECEIPT.md)), with `ramchoice` 3.0.0: the two null
rates match the script's comments; the three alternative rates differ by one or two repetitions out of 1,000.

Run 2 ([`spec2.json`](spec2.json)) changes only the `ramchoice` version: the newest release in the CRAN archive published
on or before 2021-10-20, the date in the script's header, chosen by the setup step from the archive index (the current release
is installed first only to bring in its dependencies, then replaced) and recorded by the
environment command. The comparison rule is unchanged. Whatever run 2 shows is reported next to run 1; neither replaces the
other.
