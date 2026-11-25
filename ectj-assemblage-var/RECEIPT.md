# Receipt: Barrette, Goulet Coulombe and Reinicke, "Building Macroeconomically Relevant Climate Indices via the Assemblage VAR" (Econometrics Journal, forthcoming)

**Status, 2026-11-25 17:20 UTC: complete for the README's default run. `Rscript run_all.R` exits 0 and the package's own
validation passes on Linux and on Windows. The numbers the paper quotes do not all regenerate: 89 of 1,267 numbers in
`results/summary_numbers.txt` differ from the committed file on Linux, 43 on Windows. The cumulative impulse-response
troughs in Sec. 3.2.1 regenerate on both. Most differences are in the last printed digit of aggregation-weight shares.
Reason unknown.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed materials
did on these machines. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' repository [timmy-o-toole/Assemblage_VAR](https://github.com/timmy-o-toole/Assemblage_VAR),
  commit `199c5f8c432c9571e601ce68ada49ab3d1819e55` (12 Nov 2026), 78 tracked files hashed. Not the Zenodo deposit,
  which this machine cannot reach.
- Commands, unchanged: `Rscript install_packages.R`, then `Rscript run_all.R` (fast mode, the README default: re-estimates
  the aggregation weights at the published penalties, recomputes point impulse responses, rewrites the quoted numbers;
  reads the shipped bootstrap bands, which are not recomputed).
- Protocol and comparison rule, committed before any package code ran, with two addenda: [`PROTOCOL.md`](PROTOCOL.md).
  Every run was made by [`receiptgen/rerun.py`](../receiptgen/README.md) from [`spec.json`](spec.json).

## Runs

| Run | Machine | R | Outcome |
|---|---|---|---|
| [`run1/`](run1/) | cloud container | 4.3.3 | stopped at step 1: this container's network refuses CRAN, so no package installed. No result |
| [`runs/github-45655687005`](runs/github-45655687005/RECEIPT.md) | GitHub `ubuntu-24.04` runner | 4.6.2 | exit 0 in 2 min; 89 of 1,267 quoted numbers differ |
| [`runs/github-45657860371-linux`](runs/github-45657860371-linux/RECEIPT.md) | same, again | 4.6.2 | exit 0; `summary_numbers.txt` **byte-identical to the run above** |
| [`runs/github-45660192940-windows`](runs/github-45660192940-windows/RECEIPT.md) | GitHub `windows-2025` runner | 4.6.2 (ucrt) | exit 0 in 4 min; 43 of 1,267 quoted numbers differ |

The same platform repeats exactly. Linux and Windows differ from each other and from the committed file.

## Which numbers differ

`summary_numbers.txt` is written by `code/06_summary_numbers.R` and labels each block with its place in the paper.

- **Cumulative IRF troughs (Sec. 3.2.1, Figs. 1-2):** the trough value, horizon and 68% band of all seven specifications
  regenerate on both platforms. What differs on those lines is the package's own diagnostic "re-fit from step 1 ... (max
  |diff| ...)". In the committed file that diagnostic already reports differences up to 5.2e-3 between a re-fit and the
  stored weights, so the package records that its own re-estimation does not land exactly on the stored weights.
- **Weight shares (regional and NOAA decompositions, rank-space tail masses, appendix tables):** differ mostly by 0.1 in the
  last printed digit, for example Regional Rx5Day 24.4% committed, 24.7% Linux, 24.4% Windows; NOAA Ohio Valley thermal
  block 36.16% committed, 36.08% Linux, 36.10% Windows.
- **One large number, from a near-zero denominator:** "wind share within each region's own weight" for CEA is 87% committed,
  -1353% on Linux and 105% on Windows. CEA's total weight is printed as 0.0% in all three, so this is a share of a weight that
  is close to zero.
- **`results/point_estimates/*.rds`:** the committed files record a Windows (ucrt) R session in their metadata. Printed with
  `dput`, about 600 of 35,000 to 130,000 numbers per file differ on Linux, median relative difference 1.6e-6. On Windows
  the converter command failed (a quoting problem in this tool on Windows), so those six files were compared only by bytes
  and differ.

What these runs cannot tell apart: the constrained weight estimation (`NlcOptim` SQP) may be sensitive to the BLAS, the
compiler or package versions; the committed files may come from a slightly different state of the code. Nothing here says
which. Package versions were the current CRAN releases on 25 Nov 2026, at or above those in `requirements.csv` (listed in
each run's `evidence/environment.json`).

## Cost

Three GitHub-hosted runs on a public repository: no charge. Total compute about 10 minutes, plus R package installs.

## Deviations

1. Run 1's machine could not reach CRAN; runs 2 to 4 moved to GitHub runners, with R 4.6.2 instead of 4.3.3 (protocol
   addendum 1).
2. The Windows run was added after the first Linux result, to separate platform from package (protocol addendum 2).
3. The first Windows attempt failed in 0 s because this tool's `bash` resolved to the WSL stub. That was a fault of the
   tool, logged in `receiptgen/FROZEN_CHANGES.md`, and its directory was deleted.

No package file was edited.
