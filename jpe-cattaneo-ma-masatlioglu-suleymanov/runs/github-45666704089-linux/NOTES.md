The script writes no file, so the generator's own count is 0 of 0. The comparison fixed in the protocol, done by hand from
the last lines of [`evidence/logs/simulation.log`](evidence/logs/simulation.log) against the result written in the
script's own comments:

| Hypothesis | Script comment | This run | Difference in repetitions (of 1,000) |
|---|---|---|---|
| 1, 2, 3, 4, 5 (null) | 0.000 | 0.000 | 0 |
| 2, 3, 4, 5, 1 (null) | 0.004 | 0.004 | 0 |
| 3, 4, 5, 2, 1 (alternative) | 0.144 | 0.143 | 1 |
| 4, 5, 3, 2, 1 (alternative) | 0.275 | 0.277 | 2 |
| 5, 4, 3, 2, 1 (alternative) | 0.351 | 0.352 | 1 |

Two of five match. The other three did not regenerate here, reason unknown; each is off by one or two of the 1,000
simulated datasets. The two null rates, which are the size result, match. This run used `ramchoice` 3.0.0 and R 4.6.2; the
script is dated 20 October 2021 and names no version, so an older `ramchoice` is one candidate explanation, not a
finding. A second run with the `ramchoice` release current at that date is set out in the protocol.
