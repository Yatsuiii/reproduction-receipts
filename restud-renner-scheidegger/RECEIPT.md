# Receipt: Renner and Scheidegger, "Machine Learning for Dynamic Incentive Problems" (REStud, 2026)

**Status, 2026-11-22 05:30 UTC: Steps 1, 2 and 4 complete. Steps 3 and 5 (solving from scratch) not run.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on these machines. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' public repository
  [GaussianProcessesForDynamicEcon/DynamicIncentiveProblems](https://github.com/GaussianProcessesForDynamicEcon/DynamicIncentiveProblems),
  commit `374fe17a6a21bb137c469260a7e1f72f2c6246ed` (4 Sep 2026). Not the journal's own deposit, which this machine could
  not reach (deviation 1).
- 125 regular tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256). Every fresh
  clone (three on machine 1, one on machine 2) was re-hashed against that list and matched.
- The protocol and comparison rule were committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md).

## Result

| Step (README numbering) | What it does, per the README | Outcome |
|---|---|---|
| 1 `1_install.sh` | conda env, Python 3.9.23, pinned `requirements.txt` | exit 0 on both machines, unchanged |
| 2 `2_replicate_original.sh` | paper tables and figures from the deposited checkpoints | exit 0, unchanged. **5 of 5 numeric tables match the printed values in every cell (34 cells), on both machines, byte-identical `.tex` across machines** |
| 4 `4_validate_BE.sh` | restart five deposited solutions for 10 iterations, re-simulate, recompute the error checks | exit 0 in 3 h 3 min on 4 cores (deviations 4 to 7). **Recomputed at the deposited solutions: 16 of 16 cells of Tables 7 and 8 match the printed values.** Its own tables, at the restarted solutions, differ (below) |
| 3 and 5 | solve from scratch (about 17 h at 16 processes; about 346 h on a cluster) | not run, no claim |

### Step 2 is a replay

The README says Step 2 does not run solvers or simulations. Tables 2, 7 and 8, and the second row of Table 4, are
formatted from committed error and simulation files; Table 5 and the first row of Table 4 come from metrics stored in
the committed checkpoints. A match there shows the committed files produce the printed tables in a fresh pinned
environment, not that the code produces those files.

### Step 4 recomputes, at the deposited solutions

Inside Step 4, `2D_simulation_and_error.ipynb` and `4D_simulation_and_error.ipynb` take the four deposited Section 5
solutions, re-simulate 10,000 periods with the deposited fixed shock lists (criterion 3), and append a freshly computed
error row to each `V_func_error_*.txt` (criterion 2). [`recompute_check.py`](recompute_check.py) builds Tables 7 and 8 from
those recomputed files and from the committed ones, formatted the way the paper's notebooks format them
([output](evidence/recompute_check.md)):

| Table | Row | C2 L2 | C2 Linf | C3 L2 | C3 Linf |
|---|---|---|---|---|---|
| 7 | Benchmark | 1.2e-06 = | 4.1e-06 = | 5.3e-06 = | 1.1e-05 = |
| 7 | Overreporting | 1.6e-06 = | 8.7e-06 = | 4.4e-06 = | 3.7e-05 = |
| 8 | Benchmark | 2.9e-05 = | 7.5e-05 = | 3.4e-05 = | 1.9e-04 = |
| 8 | Overreporting | 4.0e-05 = | 2.0e-04 = | 7.1e-05 = | 6.8e-04 = |

"=" means the recomputed value equals the committed one and the paper's printed value at the paper's precision. The
recomputed numbers are not bit-identical (the appended error rows differ from the committed rows from about the 6th
significant digit; the 2D simulated paths differ by at most 1.9e-4 in any entry). In the 4D runs the simulated state
paths themselves separate: in the 4D benchmark, 9,236 of 10,000 periods differ by more than 1e-3 in `w_3`, with a largest
difference of 147.5 against a typical value of 152.5. The summary errors the paper reports from those paths still agree
at printed precision. Why the paths separate is not known.

`recompute_check.py` was written after Step 4 finished, to apply the protocol's cell-by-cell rule to these files. It
was not frozen in advance.

### Step 4's own tables, at the restarted solutions

The tables Step 4 writes come from the newest checkpoints, which are the deposited solutions run for 10 more value
function iterations with 4 MPI ranks instead of the authors' 16. The README says rank count changes random draws, and
calls these outputs validation. They are not the paper's numbers, and the protocol said a difference here is expected,
unless the order of magnitude changes ([full comparison](evidence/step4-vs-paper.txt)):

| Cell | Paper | Step 4, restarted | Ratio |
|---|---|---|---|
| Table 5, all 10 cells | | | same |
| Table 4, C2 L2 / Linf | 1.6e-06 / 1.4e-04 | 8.8e-07 / 4.4e-05 | 0.6 / 0.3 |
| Table 4, C3 L2 / Linf | 7.8e-05 / 4.1e-04 | 7.7e-05 / 4.3e-04 | 1.0 / 1.0 |
| Table 7 Benchmark, C2 L2 / Linf | 1.2e-06 / 4.1e-06 | 2.6e-07 / 7.8e-07 | 0.2 / 0.2 |
| Table 7 Benchmark, C3 L2 / Linf | 5.3e-06 / 1.1e-05 | 1.1e-06 / 1.9e-06 | 0.2 / 0.2 |
| Table 7 Overreporting, C2 L2 / Linf | 1.6e-06 / 8.7e-06 | 9.2e-06 / 1.5e-04 | 5.8 / **17** |
| Table 7 Overreporting, C3 L2 / Linf | 4.4e-06 / 3.7e-05 | 2.8e-06 / 1.1e-05 | 0.6 / 0.3 |
| Table 8 Benchmark, all four | 2.9e-05 to 1.9e-04 | 3.0e-05 to 1.9e-04 | 1.0 |
| Table 8 Overreporting, C2 L2 / Linf | 4.0e-05 / 2.0e-04 | 1.1e-07 / 4.3e-07 | **0.003 / 0.002** |
| Table 8 Overreporting, C3 L2 / Linf | 7.1e-05 / 6.8e-04 | 4.1e-07 / 2.5e-06 | **0.006 / 0.004** |

Five cells move by more than a factor of ten: one larger (Table 7 overreporting, C2 Linf) and four smaller (Table 8
overreporting). Reason unknown. This receipt does not say the restarted values are better or worse, only that the
restart with 4 ranks did not land on the printed values, and the README never said it would.

## Environment

| | Machine 1 | Machine 2 |
|---|---|---|
| What | cloud container | GitHub-hosted runner `ubuntu-24.04` |
| OS | Ubuntu 24.04.5 LTS | Ubuntu 24.04 |
| CPU | 4 vCPU, Intel Xeon @ 2.10GHz | 4 vCPU, Intel Xeon 6975P-C |
| RAM | 15 GB | 15 GB |
| GPU | none | none |
| Installer | Miniforge 26.9.4-2, SHA-256 `bbaf16b3…bdf` | same bytes, checked |
| Steps run | 1, 2, 4 | 1, 2 |

Python 3.9.23 (conda-forge). Key packages as the authors pin them: torch 2.4.0, gpytorch 1.13, linear-operator 0.5.3,
scipy 1.13.1, numpy 2.0.2, hydra-core 1.3.2, mpi4py 4.1.2, Tasmanian 8.2. OpenMPI 5.0.11 and GNU parallel 20260922 from
conda-forge. The full `pip freeze` (149 lines) is in [`evidence/env-pip-freeze.txt`](evidence/env-pip-freeze.txt) and was
identical on machine 2. The conda list is in [`evidence/env-conda-explicit.txt`](evidence/env-conda-explicit.txt).

## Wall clock and cost

| Run | Wall clock |
|---|---|
| Step 1 | 312 s (machine 1), 167 s (machine 2) |
| Step 2 | 105 s, 107 s and 89 s (machine 1, three checkouts), 70 to 92 s (machine 2) |
| Step 4, final run | 10,992 s: solver restarts 1 h 36 min, post-processing 30 min, notebooks 57 min |

Machine 2 is a GitHub runner on a public repository: no charge. Machine 1 is a 4 vCPU, 15 GB container; at a typical
on-demand price for that size, around $0.20 an hour, the final Steps 1, 2 and 4 cost about $0.65. Counting the stopped
and killed attempts below, machine 1 ran for about 11 hours in total, about $2.20.

## Deviations, in order

1. **Source.** The journal's deposit could not be fetched: this machine's network allows GitHub and PyPI only, so
   Zenodo was refused. The authors' GitHub repository was used. Whether it is byte-identical to the deposit is not known.
2. **GNU parallel version.** The README names 20231122; `1_install.sh` installs it unpinned, which gave 20260922.
3. **Step 2 cleanup messages.** The scripts first delete files a clean checkout does not have, printing 70
   `rm: cannot remove` lines. Exit code and outputs are unaffected.
4. **Step 4 process count.** `N_PROCS=16` changed to `N_PROCS=4` ([diff](evidence/deviation-1-nprocs.diff)), as the README
   allows. This also makes its post-processing step run 4 jobs at once instead of 16.
5. **Running as root.** OpenMPI needed `OMPI_ALLOW_RUN_AS_ROOT=1` and `OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1`. No file edited.
6. **`OMP_NUM_THREADS=1` in the final Step 4 run.** Without it, four post-processing jobs on four cores barely moved
   (attempt 3 below). The same command run alone finished in 322 s. With the variable set, the whole step finished in
   about 3 hours. No file edited. It may change floating-point summation order.
7. **Step 4 output folder.** Step 4 writes through 14 committed symlinks into the deposited data folders and overwrites
   committed files there (`git status` after the run: [`run3-status-after-step4.txt`](evidence/run3-status-after-step4.txt)).
   That is the package's design, not an edit. It means Step 2 must not be rerun in the same tree afterwards, as the README
   warns for Steps 3 and 5. `recompute_check.py` reads the committed versions with `git show HEAD:`.

## Failed, stopped or killed runs

1. Machine 2, first workflow run: failed in my own hashing line before any package code ran (14 tracked entries are
   symlinks to directories). Fixed by hashing regular files only.
2. Step 4 attempt 1 (fresh clone): stopped by me after 17 minutes, because I ran `git stash` and `git stash pop` in its
   working tree while it ran. [Log](evidence/logs/4_validate_BE.run1-aborted.log).
3. Step 4 attempt 2 (fresh clone): all five solver restarts finished (1 h 47 min). My own 2-hour job limit then
   stopped post-processing; I resumed the script's remaining lines unchanged. After about 5 hours the 4 parallel
   post-processing jobs had written 925 of 10,000 simulation steps for the first model, and the machine restarted, which
   killed them. [Logs](evidence/logs/). Its outputs are not used anywhere above.
4. Timing check: the first post-processing command alone in attempt 2's tree, 322 s, exit 0, and the package's
   `simulate()` on one deposited checkpoint in a separate clone, about 4 minutes ([`sim_bench.py`](evidence/sim_bench.py)).
   Used only to find deviation 6.
5. Step 4 attempt 3 (fresh clone, [`run3.sh`](evidence/run3.sh)): the run reported above. Exit 0.

The README says Step 4 takes about 1 hour at 16 processes. On 4 cores it took 3 hours once threads were limited, and
did not finish in 5 hours without that.

## Triage got this package wrong

Before the rerun, [`triage.py`](../triage/README.md) said **blocked**: Mathematica required, plus 16 absolute paths. A
hand reading says neither holds. The README says the Mathematica notebooks are reference only, and the "absolute paths"
are `os.path.abspath` calls on relative paths. It also listed `hydra` as undeclared, though `hydra-core` is pinned. It did
flag the run time and the committed outputs correctly. Kept as found in
[`evidence/triage-verdict.md`](evidence/triage-verdict.md); triage is parked and is not being fixed here.

## Evidence

- [`evidence/logs/`](evidence/logs/): stdout and stderr of every run, with start, end, exit code and seconds;
  [`SUMMARY.txt`](evidence/logs/SUMMARY.txt) is the running log of what happened, in order.
- [`evidence/step2/`](evidence/step2/), [`evidence/step4/`](evidence/step4/): everything Steps 2 and 4 wrote, with hashes.
- [`evidence/step4-recomputed-files.sha256`](evidence/step4-recomputed-files.sha256): hashes of the recomputed simulation
  and error files (about 60 MB, not committed).
- [`.github/workflows/restud-renner-scheidegger.yml`](../.github/workflows/restud-renner-scheidegger.yml): the machine 2
  procedure. Anyone with a GitHub account can rerun it.
