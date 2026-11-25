The generator had no committed file to compare, so its own count of reproduced outputs is 0 of 0. The comparison fixed in
the protocol was done by hand, from the `part1.inp` log above against Table 4 (p. 12) of the working paper version
(FEEM Nota di Lavoro 2021-019), not the published article:

| Block | VAR length (paper / run) | Coint. rank (paper / run) | Common trends (paper / run) |
|---|---|---|---|
| Base metals | 2 / 2 | 1 / 1 | 5 / 5 |
| Precious metals | 2 / 2 | 1 / 1 | 2 / 2 |
| Energy | 2 / 2 | 3 / 3 | 1 / 1 |
| Livestock | 2 / 2 | 2 / 2 | 4 / 4 |
| Raw materials | 2 / 2 | 1 / 1 | 7 / 7 |
| Food | 2 / 2 | 9 / 9 | 1 / 1 |
| Total | | 17 / 17 | 20 / 20 |

All 20 printed cells match. These are integers chosen by tests (lag length by Hannan-Quinn, rank by the Johansen trace test
at 1%), so a match says the same choices were made here, not that every underlying statistic agrees to many digits.

Reported, not scored: in `part2.log`, the Bai and Ng (2007) criteria suggest q = 1, 2, 2, 1 for the four variants, and
the script takes the largest, 2, which is the q = 2 stated in the paper. The DFM estimation converged by EM in 208
iterations.

`part3.inp` exited 0 but its last command asks gretl to draw a plot on screen, which this headless machine cannot do; the log
shows `Unable to initialize GTK+` there. The numbers it prints before that are in the log and were not compared.
