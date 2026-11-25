All three committed files came back byte for byte, including `mseopt_bw.txt`, the MSE-optimal tuning parameters picked
from 150,000 seeded Monte Carlo draws (about 9 minutes here).

The one change from the package as found is an environment setting, not a code change: with the current Rcpp, `Hhat.cpp`
does not compile because R's old `PI` macro is hidden by default ([`../run1/`](../run1/RECEIPT.md) shows the error). Setting
Rcpp's documented opt-out, `RCPP_NO_STRICT_R_HEADERS`, through a Makevars file outside the clone, is enough. Anyone rerunning
the package with a recent Rcpp will hit the same compile error; replacing `PI` with `M_PI` in `Hhat.cpp` would be the
one-line fix in the package itself.

Out of scope, as set in the protocol: the bootstrap simulation behind the paper's table (`main_maxscore.R`), which is
cluster-scale.
