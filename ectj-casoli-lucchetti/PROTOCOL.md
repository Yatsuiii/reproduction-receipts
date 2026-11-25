# Protocol, written before any package code ran

Written 2026-11-25 ~17:34 UTC, after reading the README and the three Section 4 scripts. The run is driven by
[`spec.json`](spec.json) through [`receiptgen/rerun.py`](../receiptgen/README.md). The only thing run beforehand was
installing the two gretl function packages the README names (`DFM`, `staticfactor`), to check this machine can reach
gretl's package server; the third, `extra` (Monte Carlo only), timed out.

Package: [InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication](https://github.com/InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication)
at commit `d46e6006dda79c13313daa02d405b76e53df0ae4` (10 Feb 2026), for Casoli and Lucchetti, *The Econometrics Journal*
25(2), 2022.

## What will run

1. Setup: `pkg install DFM` and `pkg install staticfactor` in gretl (current versions; the README names no versions).
2. `gretlcli -b part1.inp`, `part2.inp`, `part3.inp` from `Sec4-Commodities/`, unchanged. gretl 2023c from Ubuntu 24.04;
   the README asks for 2021a or later and says it was last run with 2021c. `part1.inp` itself adjusts the lag criterion
   index for gretl versions after 2023.0.

Not run: Section 3 Monte Carlo (hand-edited per table row; `extra` package unavailable here).

## Comparison rule, fixed now

The package commits no outputs, so `rerun.py` can only record exit codes, logs and hashes. One hand comparison is added:

- The block table printed by `part1.inp` (VAR length, cointegration rank, number of common trends per block, and totals)
  against the paper's cointegration table. The source available from this machine is the working paper version,
  FEEM Nota di Lavoro 2021-019 ([AgEcon Search](https://ageconsearch.umn.edu/record/312367/files/ndl2021-019.pdf)),
  Table 4, page 12, read before the run:

  | Block | VAR length | Coint. rank | Common trends |
  |---|---|---|---|
  | Base metals | 2 | 1 | 5 |
  | Precious metals | 2 | 1 | 2 |
  | Energy | 2 | 3 | 1 |
  | Livestock | 2 | 2 | 4 |
  | Raw materials | 2 | 1 | 7 |
  | Food | 2 | 9 | 1 |
  | Total | | 17 | 20 |

  The published article's table could differ from the working paper; the receipt says which version it compared with.
  Each cell matches or does not; a mismatch is listed with both values as "did not regenerate here, reason unknown".
- The working paper (p. 12) also states q = 2 dynamic factors, chosen by Bai and Ng (2007). `part2.inp` hard-codes
  `q = 2` and computes the criterion as `optimal_q`; if the log shows it, it is reported, not scored.
- The receipt does not say whether the paper is right. It says what the committed materials did on this machine.

## Addendum, 2026-11-25 ~17:35 UTC, after a first attempt

The first attempt's setup step failed in 0.03 s on the spec's side: gretl did not find the install script at the relative
path `../pkgs.inp`. The scripts still ran, using the copies of `DFM` and `staticfactor` installed by the pre-run check
above. Because the packages were not installed by the run itself, that attempt was discarded. Changes: the setup path is
now absolute, the environment command records the function packages' own version and date fields, and both packages are
removed from this machine before the run so the setup step has to install them. Nothing else changed.
