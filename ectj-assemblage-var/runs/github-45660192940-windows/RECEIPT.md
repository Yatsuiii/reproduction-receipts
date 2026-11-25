# Receipt: Barrette, Goulet Coulombe and Reinicke, "Building Macroeconomically Relevant Climate Indices via the Assemblage VAR" (Econometrics Journal, forthcoming)

**Status, 2026-11-25 17:06 UTC: 1 of 1 commands exited 0. 0 of 7 declared outputs reproduced. 7 did not regenerate the committed file, 43 values in all; the committed materials did not reproduce those values here, reason unknown.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on this machine. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' repository [timmy-o-toole/Assemblage_VAR](https://github.com/timmy-o-toole/Assemblage_VAR), not the Zenodo deposit 10.5281/zenodo.23976450, which this machine cannot reach, commit `199c5f8c432c9571e601ce68ada49ab3d1819e55`.
- Paper: Barrette, Goulet Coulombe and Reinicke, Building Macroeconomically Relevant Climate Indices via the Assemblage VAR, The Econometrics Journal, forthcoming (arXiv 2610.10043).
- 78 tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256) (SHA-256 of that list `f6ae9483669ced80…`).
- Protocol and comparison rule, committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md).
- Comparison: each declared output, after the run, against the committed file of the same path. Numbers are compared one by one with relative tolerance 1e-12; all other text must be identical.
- Fast mode only, the README's default (`Rscript run_all.R`, about 10 minutes): it re-estimates the aggregation weights at the published penalties, recomputes the point impulse responses, redraws the figures and rewrites the numbers quoted in the paper. It reads the shipped bootstrap bands and appendix bootstrap results; those are not recomputed, so nothing here speaks to them.
- Figures are git-ignored in this package, so there is nothing committed to compare them with. The paper's PDF was not compared.

## Result

| Command | Exit | Time | Output | Outcome | Reproduced |
|---|---|---|---|---|---|
| `Rscript run_all.R` | 0 | 4 min 11 s | `results/point_estimates/comp_national.rds` | binary file differs from the committed file; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/comp_noaa.rds` | binary file differs from the committed file; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/comp_regional.rds` | binary file differs from the committed file; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/rank_national.rds` | binary file differs from the committed file; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/rank_noaa.rds` | binary file differs from the committed file; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/rank_regional.rds` | binary file differs from the committed file; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/summary_numbers.txt` | did not regenerate the committed values: 43 of 1267 numbers | no |

### Values that did not regenerate

The committed materials did not reproduce these values on this machine, reason unknown. Line numbers are lines of the output file. The full list is in `results.json`.

| Output | Line | Committed | Regenerated |
|---|---|---|---|
| `results/summary_numbers.txt` | 18 | 3.1e-03 | 8.5e-04 |
| `results/summary_numbers.txt` | 19 | -0.313 | -0.314 |
| `results/summary_numbers.txt` | 19 | 5.2e-03 | 6.3e-03 |
| `results/summary_numbers.txt` | 22 | 2.2e-03 | 3.3e-03 |
| `results/summary_numbers.txt` | 38 | 9.1 | 9.2 |
| `results/summary_numbers.txt` | 38 | 8.8 | 8.7 |
| `results/summary_numbers.txt` | 38 | 18.2 | 18.3 |
| `results/summary_numbers.txt` | 39 | 28.6 | 28.5 |
| `results/summary_numbers.txt` | 40 | 15.9 | 16.0 |
| `results/summary_numbers.txt` | 42 | 35.9 | 35.8 |
| `results/summary_numbers.txt` | 43 | 87 | 105 |
| `results/summary_numbers.txt` | 51 | 9.5 | 9.4 |
| `results/summary_numbers.txt` | 51 | 0.4 | 0.3 |
| `results/summary_numbers.txt` | 53 | 0.2 | 0.3 |
| `results/summary_numbers.txt` | 54 | 16.8 | 16.9 |
| `results/summary_numbers.txt` | 55 | 36.16 | 36.10 |
| `results/summary_numbers.txt` | 55 | 27.45 | 27.47 |
| `results/summary_numbers.txt` | 65 | 2.921 | 2.910 |
| `results/summary_numbers.txt` | 65 | 2.585 | 2.564 |
| `results/summary_numbers.txt` | 65 | 2.947 | 2.935 |
| `results/summary_numbers.txt` | 65 | 2.591 | 2.570 |
| `results/summary_numbers.txt` | 65 | 2.921 | 2.910 |
| `results/summary_numbers.txt` | 66 | 75.2 | 75.4 |
| `results/summary_numbers.txt` | 66 | 0.17 | 0.16 |
| `results/summary_numbers.txt` | 66 | 0.43 | 0.48 |
| `results/summary_numbers.txt` | 66 | 3.30 | 3.41 |
| `results/summary_numbers.txt` | 67 | 19.1 | 19.0 |
| `results/summary_numbers.txt` | 67 | 49.0 | 49.3 |
| `results/summary_numbers.txt` | 67 | 49.2 | 49.4 |
| `results/summary_numbers.txt` | 67 | 49.2 | 49.4 |
| `results/summary_numbers.txt` | 67 | 49.2 | 49.5 |
| `results/summary_numbers.txt` | 67 | 51.4 | 51.1 |
| `results/summary_numbers.txt` | 67 | 64.5 | 64.3 |
| `results/summary_numbers.txt` | 67 | 82.8 | 82.9 |
| `results/summary_numbers.txt` | 89 | 9.1 | 9.2 |
| `results/summary_numbers.txt` | 89 | 8.8 | 8.7 |
| `results/summary_numbers.txt` | 89 | 18.2 | 18.3 |
| `results/summary_numbers.txt` | 90 | 16.8 | 16.9 |
| `results/summary_numbers.txt` | 93 | 2.95 | 2.94 |
| `results/summary_numbers.txt` | 102 | 99.8 | 99.7 |
| `results/summary_numbers.txt` | … | 3 more in `results.json` | |

## Environment

| | |
|---|---|
| OS | Windows |
| CPU | Intel64 Family 6 Model 207 Stepping 2, GenuineIntel |
| Cores | 4 |
| RAM | None GB |
| GPU | none |
| git | git version 2.56.1.windows.1 |
| python3 | Python 3.12.10 |
| R | R version 4.6.2 (2026-10-29 ucrt) -- "Diversified Portfolio" |
| julia | julia version 1.12.0 |

Full environment listings: [`evidence/environment.json`](evidence/environment.json).

## Wall clock and cost

Commands ran for 4 min 14 s in all, one after another, from 2026-11-25T17:02:04Z to 2026-11-25T17:06:31Z.
At 0.2 USD an hour for this machine (typical on-demand price for a 4 vCPU, 16 GB cloud machine), that is about 0.01 USD.

## Deviations, in order

None. No package file was edited before or between commands.

## Failed, stopped or killed runs

None.

## Evidence

- [`results.json`](results.json): every number above, with each command's start, end and exit code.
- [`evidence/logs/`](evidence/logs/): stdout and stderr of every command.
- [`evidence/outputs/`](evidence/outputs/): every output this run wrote.
- Generated by `receiptgen/rerun.py` from the spec in `results.json`.
