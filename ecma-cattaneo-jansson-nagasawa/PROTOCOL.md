# Protocol, written before the receipt runs

Written 2026-11-25 ~17:33 UTC, after reading the README files and every script, and after one scratch probe described
below. The runs are driven by [`spec.json`](spec.json) and [`spec2.json`](spec2.json) through
[`receiptgen/rerun.py`](../receiptgen/README.md).

Package: [mdcattaneo/replication-CJN_2020_ECMA](https://github.com/mdcattaneo/replication-CJN_2020_ECMA) at commit
`b03241cf302c3ddb1881bcec864b29fd27097890` (28 May 2023), the authors' simulation files for Cattaneo, Jansson and Nagasawa,
"Bootstrap-Based Inference for Cube Root Asymptotics", *Econometrica* 88(5), 2020.

Why this one: free software only (base R plus Rcpp), no data download, and the scripts write text files that are committed,
so there is something to compare against. Fourth on the [candidate list](../candidates/README.md).

## What will run

1. `Rscript DGP_constants.R`: closed-form values of H0 for the three designs. Writes `H0.txt`.
2. `Rscript AMSE.R`: AMSE-optimal tuning parameters by numerical integration. Writes `AMSEopt_bw.txt`.
3. `Rscript mse_opt_simulation.R`: 50,000 Monte Carlo draws per design, with a fixed seed per draw, picking the tuning
   parameter on a grid that minimises simulated MSE. Reads `H0.txt` (rewritten by step 1 first), compiles `Hhat.cpp` with
   Rcpp, writes `mseopt_bw.txt`.

Not run: `main_maxscore.R` and `collect_tables_ms.R`, the bootstrap simulation behind the paper's table. Its settings
(2,000 bootstrap draws for each of 2,000 simulations, on a cluster) are beyond this machine, so the receipt says nothing about
`table_maxscore.txt`.

Environment: R 4.3.3 and Rcpp 1.0.12 from Ubuntu 24.04 packages, g++ 13. No package file is edited.

## The scratch probe, and why there are two specs

Before writing this, step 3 was timed in a scratch copy with 200 draws for one design. `Hhat.cpp` did not compile:
`Hhat.cpp:7:29: error: 'PI' was not declared in this scope`. Recent Rcpp versions define `STRICT_R_HEADERS` by default,
which hides R's old `PI` macro; Rcpp documents `RCPP_NO_STRICT_R_HEADERS` as the opt-out. With that flag set through a
user Makevars file outside the package, the file compiled and 200 draws took about 1.2 s, so the full step should take
about 15 minutes here.

- Run 1, [`spec.json`](spec.json): the package exactly as found. Step 3 is expected to fail at compilation; that is
  recorded, not hidden.
- Run 2, [`spec2.json`](spec2.json): identical, except that a setup step writes
  `CPPFLAGS += -DRCPP_NO_STRICT_R_HEADERS` to a Makevars file outside the clone and step 3 runs with
  `R_MAKEVARS_USER` pointing at it. This is an environment setting, not a code change, and the receipt lists it.

## Comparison rule, fixed now

- `H0.txt`, `AMSEopt_bw.txt`, `mseopt_bw.txt`: byte comparison, then every number against the committed file at relative
  tolerance 1e-12 with all other text identical. A difference is listed with both values as "did not regenerate here,
  reason unknown".
- `mseopt_bw.txt` holds grid points (multiples of 0.01), so it either matches exactly or picks a different grid point.
  R's generators for `rnorm`, `rlogis` and `rt` have not changed since the package was written, so with the package's fixed
  seeds an exact match is the expectation; a different grid point would be reported as is.
- `H0.txt` is declared a committed intermediate: if step 3 read the committed copy rather than step 1's, its output would
  not count as reproduced.
- The receipt does not say whether the paper is right. It says what the committed materials did on this machine.
