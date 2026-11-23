# Receipt: Lee and Weidner, "Bounding Treatment Effects by Pooling Limited Information across Observations" (Journal of Econometrics, forthcoming)

**Status, 2026-11-23: complete. Four of five README commands regenerate their committed output byte for byte on two
machines. One, `Examples/Table3_NSW.R`, regenerates 99 of its 139 printed numbers. Panel B matches in full; 40 of the 48
bound and interval values in Panel A come out different, the same way on every machine and R version tried. The committed materials did not regenerate those 40 values here, reason
unknown.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on these machines. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' repository [ATbounds/ATbounds-replication](https://github.com/ATbounds/ATbounds-replication),
  commit `67c2c4d403d3dfbbfa4cfb25f72fe88d7d0f00da` (7 May 2026). Not a journal deposit. 15 tracked files, each hashed in
  [`evidence/package-files.sha256`](evidence/package-files.sha256); every fresh clone was re-hashed against that list
  and matched.
- The protocol and comparison rule were committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md),
  [`compare_results.py`](compare_results.py). How this package was chosen: [`CANDIDATES.md`](CANDIDATES.md).
- What is compared: each script overwrites its committed file under `Results/`; the regenerated file is compared with the
  committed one, every printed number exact or not, no tolerance. **The paper's PDF was not compared.**
- Workflow: [`.github/workflows/jeconom-lee-weidner.yml`](../.github/workflows/jeconom-lee-weidner.yml), one fresh clone
  per command per machine. First complete run:
  [45231977655](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/45231977655); repeated after the compare
  fix in [45235594687](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/45235594687). Logs, regenerated files and
  comparison output are in that run's artifacts.

## Result

| README command | Output | ubuntu-22.04 | ubuntu-24.04 | Outcome |
|---|---|---|---|---|
| `Rscript MC/Table1_MonteCarlo.R` (full `n_sim = 1000`) | `MC/Results/Table1_MonteCarlo.tex` | exit 0 | exit 0 | **byte-identical** to committed |
| `Rscript Examples/Table2_RHC.R` | `Table2_RHC.tex`, `RHC_ATT_summary.txt` | exit 0 | exit 0 | **byte-identical** to committed |
| `Rscript Examples/Table3_NSW.R` | `Examples/Results/Table3_NSW.tex` | exit 0 | exit 0 | **99 of 139 numbers exact, 40 differ**, all in Panel A, same 40 on both machines |
| `Rscript MC/AppendixTable_MonteCarloInference.R` (full) | `MC/Results/AppendixTable_MonteCarloInference.tex` | exit 0 | exit 0 | **byte-identical** to committed |
| `Rscript Examples/NSW_main_text.R` | `Examples/Results/NSW_results_in_main_text.txt` | exit 0 | exit 0 | **byte-identical** to committed |

"Byte-identical" means `git status` in the clone showed no change after the script had rewritten its file (each script
opens its output with `sink(..., append = FALSE)`), so the regenerated file equals the committed one exactly.

The Monte Carlo matches are fresh computation from the scripts' fixed seed (`234235`), not a read-back of committed files.

### Table 3, the 40 values that did not regenerate

All 40 are in Panel A (Dehejia-Wahba subsample: NSWRE treated and NSWRE controls). Panel B (NSW treated and PSID2
controls), which uses the same treated file, matches in all 48 values. In Panel A the L = 5, 10 and 20 rows with Q = 1
differ only in the confidence limits; most rows with Q = 2 to 4 differ in all four columns, by 0.001 to 0.038. Line
numbers are lines of the `.tex` file. Full list in the run's `compare-committed.txt`.

| Line | Committed | Regenerated |
|---|---|---|
| 10 | -0.628, 0.659 | -0.631, 0.658 |
| 11 | 0.040, -0.073, 0.173 | 0.034, -0.067, 0.157 |
| 12 | 0.109, 0.008, -0.055, 0.180 | 0.108, 0.003, -0.048, 0.168 |
| 13 | 0.093, 0.021, -0.088, 0.204 | 0.090, 0.017, -0.084, 0.193 |
| 15 | -0.788, 0.804 | -0.750, 0.779 |
| 16 | 0.079, 0.092, -0.017, 0.197 | 0.083, 0.101, -0.014, 0.212 |
| 17 | 0.100, 0.069, -0.014, 0.184 | 0.105, 0.078, -0.010, 0.195 |
| 18 | 0.127, 0.030, -0.038, 0.191 | 0.133, 0.042, -0.033, 0.203 |
| 20 | -0.893, 0.885 | -0.860, 0.859 |
| 21 | 0.084, 0.087, -0.010, 0.192 | 0.087, 0.089, -0.002, 0.190 |
| 22 | 0.098, 0.077, -0.007, 0.183 | 0.101, 0.079, 0.001, 0.181 |
| 23 | 0.066, 0.067, -0.052 | 0.070, 0.071, -0.045 |

One confidence limit changes sign (line 22, CI-LB -0.007 to 0.001). Whether any of this matters for the paper is for the authors to say; this receipt compares numbers only.

### Separate check: is it the R version or the ATbounds build?

Not part of the as-is rerun, run afterwards as a labelled extra
([workflow](../.github/workflows/jeconom-lee-weidner-table3-check.yml),
[run 45233855574](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/45233855574)). `Table3_NSW.R` has no
random draws, and ATbounds' `atebounds()` is deterministic for this call (complete-linkage `hclust` on `dist(X)`, then
`cutree`), so the same inputs should give the same table anywhere.

| R | ATbounds | Table 3 result |
|---|---|---|
| 4.1.3, 4.2.3, 4.3.3, 4.4.3, 4.5.2, release | CRAN 0.1.1 (Posit binaries) | 99 exact, 40 differ, identical list each time |
| release | built from [ATbounds-r](https://github.com/ATbounds/ATbounds-r) `2333425` | 99 exact, 40 differ, identical list |

So across five years of R releases and both ways of installing ATbounds, the regenerated table is the same and the
difference does not move. Between the released 0.1.1 and the code before it, the only change to `atebounds()` is a
comment.

What that leaves, untested: the script reads its data from Rajeev Dehejia's NBER page at run time, and the package does
not include or hash those files, so a change in an input since the committed table was made would explain it; so would
a different version of the script. Two facts narrow it without settling it. Panel B, which uses the same
`nswre74_treated.txt` with `psid2_controls.txt`, matches in full. And `NSW_main_text.R`, which reads `nswre74_control.txt`
for its outcome and treatment columns (not the covariates), regenerated byte for byte. The five files as downloaded on
23 Nov are hashed in [`evidence/nber-data.sha256`](evidence/nber-data.sha256). **Reason unknown.**

## Environment

| | Machine 1 | Machine 2 |
|---|---|---|
| What | GitHub-hosted runner `ubuntu-22.04` | GitHub-hosted runner `ubuntu-24.04` |
| OS | Ubuntu 22.04.5 LTS | Ubuntu 24.04.5 LTS |
| CPU | Intel Xeon Platinum 8573C, 4 vCPU | AMD EPYC 9V74, 4 vCPU |
| RAM | 15 GB | 15 GB |
| R | 4.6.2 (2026-10-29), the runner's own | 4.3.3 (2024-02-29), Ubuntu's `r-base-core` from apt (the runner has no R) |

Packages, the same on both: ATbounds 0.1.1, FNN 1.1.4.1, xtable 1.8.8, ggplot2 4.0.4, sandwich 3.1.3, lmtest 0.9.40.
The README names no R version and pins no package versions, so these are what installed on 23 Nov 2026. The four
byte-identical outputs came out the same under two R versions and two CPU vendors.

## Wall clock and cost

The README says the Monte Carlo scripts "can take substantially longer"; they did not take long here.

| Script | Run step, 22.04 | Run step, 24.04 |
|---|---|---|
| `MC/Table1_MonteCarlo.R` | about 4.4 min | about 3 min |
| `MC/AppendixTable_MonteCarloInference.R` | about 2.3 to 3 min | about 2.3 to 3 min |
| `Examples/Table2_RHC.R` | about 1.1 min | about 1.1 min |
| `Examples/Table3_NSW.R`, `NSW_main_text.R` | about 1 s each | about 1 s each |

Ten jobs, about 7 minutes end to end including R and package installs. GitHub runners on a public repository: no charge.
On a paid 4-vCPU runner at list price it would be well under $1.

## Cheap baseline

The triage script's "assume blocked" baseline would have been wrong here: the package ran with no edits. The triage
verdict was "runnable with deviations", flagging unpinned CRAN packages and the run-time NBER download. That flag is the
one input this receipt cannot pin, and the one table that uses the NSWRE control covariates is the one that did not
fully regenerate. That is a lead, not a finding, until someone checks the files.

## Deviations, in order

1. **Binary package mirror.** Packages were installed from Posit's prebuilt Linux binaries of CRAN
   (`p3m.dev/cran/__linux__/<codename>/latest`) instead of building CRAN sources, to save time. Same CRAN versions.
2. **Comparison step did not fail the job at first.** In run 45231977655 the compare step printed the 40 differences but
   exited 0, because of a shell pipe. Fixed after that run so a difference turns the job red; the comparison itself was
   unchanged.
3. **Extra check added after the result.** The R-version check above was written after Table 3 failed to regenerate. It
   is labelled and kept apart from the as-is result.

Nothing in the package was edited. No environment variables were set; the Monte Carlo scripts ran at the full size.
