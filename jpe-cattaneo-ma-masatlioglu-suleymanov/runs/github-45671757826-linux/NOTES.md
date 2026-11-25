With `ramchoice` 2.0, the release current on 2021-10-20, the five printed rates are exactly the same as in run 1 with 3.0.0:
0.000, 0.004, 0.143, 0.277, 0.352. Against the script's stated result (0.000, 0.004, 0.144, 0.275, 0.351), the two null
rates match and the three alternative rates differ by one, two and one of the 1,000 simulated datasets.

So the package version does not explain the gap. It remains "did not regenerate here, reason unknown". The R version
(4.6.2 here), the random number stream or the numerical libraries are candidates that were not tested. The size result
(the two null hypotheses) reproduces; the power figures are within 0.002 of those stated.
