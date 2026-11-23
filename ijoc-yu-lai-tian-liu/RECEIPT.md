# Receipt: Yu, Lai, Tian and Liu, "Solving Markov Decision Processes via Largest-size Average Estimator" (IJOC, 2026)

**Status, 2026-11-23 09:05 UTC: three of six README commands complete on two machines. The other three are still running
on machine 1; what they have printed so far is compared below. This receipt will be updated when they finish.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on these machines. It does not say anything about whether the paper is right.

## What was checked

- Package: the journal's own code and data archive,
  [INFORMSJoC/2024.0863](https://github.com/INFORMSJoC/2024.0863), commit `325bb7d99908de5df94c9c709bcf37ccbdbff5ae`
  (1 Oct 2026), archive DOI 10.1287/ijoc.2024.0863.cd.
- 16 tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256). Every fresh clone (six on
  machine 1, five on machine 2) was re-hashed against that list and matched.
- The protocol and comparison rule were committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md). The addendum
  there, written after two minutes of the first command, explains the change of run order.
- What is compared: each regenerated `results/*.csv` against the committed one, cell by cell. The README says those CSVs hold
  the numerical results of the experiments. This machine could not reach the journal's website, so **the paper's printed
  tables were not compared.**

## Result

| README command | Machine 1 | Machine 2 | Outcome |
|---|---|---|---|
| `ttt4x4_softmax.py` (policy performance, softmax Player 1) | exit 0, 914 s | exit 0, 251 s | **320 of 320 cells match.** 317 identical text; 3 differ only in the last digit of a double (relative 2e-16) |
| `ttt4x4_random.py` (policy performance, random Player 1) | exit 0, 1,335 s | exit 0, 422 s | **320 of 320 cells match.** 316 identical text; 4 last-digit |
| `ttt3x3_value_estimation.py` | exit 0, 2,651 s | exit 0, 1,314 s | **189 of 189 cells match.** 179 identical text; 10 last-digit (at most 3.4e-16) |
| `inventory_control.py` | running | cancelled by my 5-hour job limit | so far 58 of 160 rows printed; **232 of 232 printed values match** at printed precision |
| `ttt4x4_value_estimation.py` | running | cancelled by my 5-hour job limit | so far 3 of 15 rows printed; **12 of 12 printed values match** at printed precision |
| `intruder_monitor.py` | waiting to run | not run | a first run stopped after 4 of 288 rows; **16 of 16 printed values match** |

"Match" for a full CSV means every cell is either the same text or the same double to 1e-12 relative. No cell was in the
"close" or "differs" class. On both machines the same cells differed in the last digit, with the same regenerated values,
although the two machines ran different Python versions and different CPUs.

"Printed precision" means the value the script prints while running (6 decimals for mean, bias and standard deviation, 8 for
MSE), compared with the committed CSV rounded the same way, by [`compare_printed.py`](compare_printed.py). It is weaker than a
CSV match. These scripts write their CSV only at the very end.

The scripts seed every replication, so an exact match is what a correct rerun should give here. The matches are fresh
computation: nothing is read from the committed CSVs, which each script overwrites at the end.

## How long it takes

The README gives no run times. This is the main thing a desk would want to know before starting:

| Script | Cost growth seen | Projected on 4 cores |
|---|---|---|
| three short scripts | | 4 to 22 min each on a 4-vCPU GitHub runner |
| `inventory_control.py` | per-cell time grows about as N^3 (6.6 s at N=100, 486 s at N=400) | about 13 h |
| `ttt4x4_value_estimation.py` | about 2 h for the N=50 cell of the first estimator | well over a day |
| `intruder_monitor.py` | 1.5, 6.0, 17.3, 41.9 s for N=8 to 14 (about N^6) | about 3 days |

## Environment

| | Machine 1 | Machine 2 |
|---|---|---|
| What | cloud container | GitHub-hosted runner `ubuntu-24.04` |
| OS | Ubuntu 24.04.5 LTS | Ubuntu 24.04 |
| CPU | 4 vCPU, Intel Xeon @ 2.10GHz | 4 vCPU, Intel Xeon 6975P-C |
| RAM | 15 GB | 15 GB |
| GPU | none | none |
| Python | 3.13.18 | 3.12.3 |

Both machines: a fresh venv, then `pip install -r requirements.txt` unchanged, which resolved to the same versions on both:
numpy 2.5.5, numba 0.68.1, llvmlite 0.50.0, tqdm 4.70.1 ([`evidence/env-pip-freeze.txt`](evidence/env-pip-freeze.txt)).
The requirements file names no versions and the README names no Python version, so another day may install something else.

## Wall clock and cost

Machine 2 is a GitHub runner on a public repository: no charge. Machine 1 is a 4 vCPU, 15 GB container; at a typical
on-demand price for that size, around $0.20 an hour, the three short scripts cost about $0.25 and everything so far
(about 5.3 hours of machine time) about $1.10. A full run of all six scripts on this machine would be about five days, about
$25.

## Deviations, in order

1. **Run order.** `intruder_monitor.py` is first in the README. I stopped it after 2 minutes, once its per-cell times showed
   it would take about 3 days, and moved it last ([addendum](PROTOCOL.md)). Its first run's log is kept.
2. **Concurrent runs on machine 1.** To save time, the three short scripts ran at the same time as `inventory_control.py`,
   and then `ttt4x4_value_estimation.py` joined it. That shares 4 cores, so the machine 1 wall clocks above are longer than a
   run alone. The scripts seed each replication, and the outputs matched machine 2, where each ran alone.
3. **Numba cache files.** The 4x4 and 3x3 scripts use `@njit(cache=True)` and write `.nbi`/`.nbc` files into
   `scripts/*/__pycache__/` in the checkout. That is the package's design, not an edit. No tracked file other than the
   script's own CSV changed.
4. **Two comparison scripts written after runs started.** [`compare_csv.py`](compare_csv.py) was committed with the protocol.
   [`compare_printed.py`](compare_printed.py) was written after the first stopped run, then widened to the two other long
   scripts' print formats. Both were checked by changing one value and seeing it reported
   ([`evidence/compare-selftest.txt`](evidence/compare-selftest.txt)).

No package file was edited and nothing extra was installed.

## Failed, stopped or killed runs

1. `intruder_monitor.py`, first run (fresh clone): stopped by me after 2 minutes and 4 rows, to change the order.
   [Log](evidence/logs/intruder_monitor.run1-stopped.log).
2. Machine 2, `inventory_control.py` and `ttt4x4_value_estimation.py`: cancelled at 09:01 UTC by the 5-hour job limit I set
   in the workflow. Their outputs are not used anywhere above. The workflow now runs only the three short scripts, so it
   finishes; the long ones are left to machine 1.

## Triage

Before the rerun, [`triage.py`](../triage/README.md) said **runnable with deviations**: requirements without versions. That
held. It did not warn about run time, because the README states none.

## Evidence

- [`evidence/logs/`](evidence/logs/): stdout and stderr of every machine 1 run with start, end, exit code and seconds;
  [`SUMMARY.txt`](evidence/logs/SUMMARY.txt) is the running log, in order.
- [`evidence/printed-compare-0905.txt`](evidence/printed-compare-0905.txt): the printed-precision comparisons for the three long scripts as of 09:05 UTC.
- [`evidence/machine1/`](evidence/machine1/): the three regenerated CSVs, hashes, and the cell-by-cell comparisons.
- [`.github/workflows/ijoc-yu-lai-tian-liu.yml`](../.github/workflows/ijoc-yu-lai-tian-liu.yml): the machine 2 procedure. Anyone
  with a GitHub account can rerun it; [run 45109284444](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/45109284444)
  holds the first run's logs, including the two cancelled jobs.
