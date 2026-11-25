# Receipt: Barrette, Goulet Coulombe and Reinicke, "Building Macroeconomically Relevant Climate Indices via the Assemblage VAR" (Econometrics Journal, forthcoming)

**Status, 2026-11-25 16:57 UTC: 1 of 1 commands exited 0. 0 of 7 declared outputs reproduced. 7 did not regenerate the committed file, 89 values in all; the committed materials did not reproduce those values here, reason unknown.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on this machine. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' repository [timmy-o-toole/Assemblage_VAR](https://github.com/timmy-o-toole/Assemblage_VAR), not the Zenodo deposit 10.5281/zenodo.23976450, which this machine cannot reach, commit `199c5f8c432c9571e601ce68ada49ab3d1819e55`.
- Paper: Barrette, Goulet Coulombe and Reinicke, Building Macroeconomically Relevant Climate Indices via the Assemblage VAR, The Econometrics Journal, forthcoming (arXiv 2610.10043).
- 78 tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256) (SHA-256 of that list `0a9af5448cf42a7e…`).
- Protocol and comparison rule, committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md).
- Comparison: each declared output, after the run, against the committed file of the same path. Numbers are compared one by one with relative tolerance 1e-12; all other text must be identical.
- Fast mode only, the README's default (`Rscript run_all.R`, about 10 minutes): it re-estimates the aggregation weights at the published penalties, recomputes the point impulse responses, redraws the figures and rewrites the numbers quoted in the paper. It reads the shipped bootstrap bands and appendix bootstrap results; those are not recomputed, so nothing here speaks to them.
- Figures are git-ignored in this package, so there is nothing committed to compare them with. The paper's PDF was not compared.

## Result

| Command | Exit | Time | Output | Outcome | Reproduced |
|---|---|---|---|---|---|
| `Rscript run_all.R` | 0 | 2 min 9 s | `results/point_estimates/comp_national.rds` | text differs from the committed file; same count of numbers, 599 of 35112 differ; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/comp_noaa.rds` | text differs from the committed file; same count of numbers, 676 of 80398 differ; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/comp_regional.rds` | text differs from the committed file; same count of numbers, 629 of 52200 differ; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/rank_national.rds` | text differs from the committed file; same count of numbers, 599 of 39804 differ; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/rank_noaa.rds` | text differs from the committed file; same count of numbers, 676 of 130498 differ; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/point_estimates/rank_regional.rds` | text differs from the committed file; same count of numbers, 629 of 73954 differ; compared after `Rscript -e 'dput(readRDS(commandArgs(TRUE)[1]), control = c("keepNA", "keepInteger", "niceNames", "showAttributes", "digits17"))' {in}` | no |
|  |  |  | `results/summary_numbers.txt` | did not regenerate the committed values: 89 of 1267 numbers | no |

### Values that did not regenerate

The committed materials did not reproduce these values on this machine, reason unknown. Line numbers are lines of the output file. The full list is in `results.json`.

| Output | Line | Committed | Regenerated |
|---|---|---|---|
| `results/summary_numbers.txt` | 16 | 1.6e-14 | 2.9e-15 |
| `results/summary_numbers.txt` | 17 | 0.0e+00 | 1.5e-06 |
| `results/summary_numbers.txt` | 18 | -0.239 | -0.242 |
| `results/summary_numbers.txt` | 18 | 3.1e-03 | 1.4e-02 |
| `results/summary_numbers.txt` | 19 | -0.313 | -0.314 |
| `results/summary_numbers.txt` | 19 | 5.2e-03 | 6.6e-03 |
| `results/summary_numbers.txt` | 20 | 5.7e-07 | 6.5e-07 |
| `results/summary_numbers.txt` | 21 | 1.1e-03 | 1.7e-05 |
| `results/summary_numbers.txt` | 22 | -0.314 | -0.312 |
| `results/summary_numbers.txt` | 22 | 2.2e-03 | 1.4e-02 |
| `results/summary_numbers.txt` | 38 | 24.4 | 24.7 |
| `results/summary_numbers.txt` | 38 | 9.1 | 9.2 |
| `results/summary_numbers.txt` | 38 | 8.8 | 8.5 |
| `results/summary_numbers.txt` | 38 | 18.2 | 18.4 |
| `results/summary_numbers.txt` | 38 | 39.4 | 39.3 |
| `results/summary_numbers.txt` | 39 | 0.0 | 0.1 |
| `results/summary_numbers.txt` | 39 | 28.6 | 28.1 |
| `results/summary_numbers.txt` | 39 | 2.8 | 2.9 |
| `results/summary_numbers.txt` | 39 | 8.0 | 8.2 |
| `results/summary_numbers.txt` | 40 | 2.3 | 2.5 |
| `results/summary_numbers.txt` | 41 | 7.3 | 7.5 |
| `results/summary_numbers.txt` | 42 | 13.7 | 13.8 |
| `results/summary_numbers.txt` | 42 | 3.7 | 4.0 |
| `results/summary_numbers.txt` | 42 | 35.9 | 35.6 |
| `results/summary_numbers.txt` | 42 | 12.8 | 12.9 |
| `results/summary_numbers.txt` | 42 | 12.0 | 12.1 |
| `results/summary_numbers.txt` | 42 | 21.9 | 21.7 |
| `results/summary_numbers.txt` | 43 | 87 | -1353 |
| `results/summary_numbers.txt` | 43 | 0 | 4 |
| `results/summary_numbers.txt` | 43 | 80 | 79 |
| `results/summary_numbers.txt` | 43 | 67 | 68 |
| `results/summary_numbers.txt` | 48 | 1.6 | 1.5 |
| `results/summary_numbers.txt` | 48 | 10.6 | 10.5 |
| `results/summary_numbers.txt` | 48 | 4.6 | 4.7 |
| `results/summary_numbers.txt` | 49 | 12.2 | 12.3 |
| `results/summary_numbers.txt` | 51 | 9.5 | 9.4 |
| `results/summary_numbers.txt` | 51 | 0.4 | 0.3 |
| `results/summary_numbers.txt` | 51 | 26.7 | 26.6 |
| `results/summary_numbers.txt` | 53 | 0.2 | 0.3 |
| `results/summary_numbers.txt` | 54 | 16.8 | 17.0 |
| `results/summary_numbers.txt` | … | 49 more in `results.json` | |

## Environment

| | |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| CPU | Intel(R) Xeon(R) 6975P-C |
| Cores | 4 |
| RAM | 15.3 GB |
| GPU | none |
| git | git version 2.56.1 |
| python3 | Python 3.12.10 |
| R | R version 4.6.2 (2026-10-29) -- "Diversified Portfolio" |
| julia | julia version 1.13.4 |

Full environment listings: [`evidence/environment.json`](evidence/environment.json).

## Wall clock and cost

Commands ran for 4 min 24 s in all, one after another, from 2026-11-25T16:49:38Z to 2026-11-25T16:57:21Z.
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
