# Receipt: Renner and Scheidegger, "Machine Learning for Dynamic Incentive Problems" (REStud, 2026)

**Status, 2026-11-22 00:00 UTC: Steps 1 and 2 complete on two machines. Step 4 is still running and nothing below
claims a Step 4 result.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on these machines. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' public repository
  [GaussianProcessesForDynamicEcon/DynamicIncentiveProblems](https://github.com/GaussianProcessesForDynamicEcon/DynamicIncentiveProblems),
  commit `374fe17a6a21bb137c469260a7e1f72f2c6246ed` (4 Sep 2026). Not the journal's own deposit, which this machine could
  not reach (see deviation 1).
- 125 regular tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256). The
  second machine re-hashed a fresh clone and got the same list.
- The protocol and the comparison rule were committed before any package code ran:
  [`PROTOCOL.md`](PROTOCOL.md), first commit of this folder.

## Result

| Step (README numbering) | What it does, per the README | Ran | Outcome |
|---|---|---|---|
| 1 `1_install.sh` | conda env, Python 3.9.23, `pip install -r requirements.txt` | unchanged, both machines | exit 0; 312 s and 167 s |
| 2 `2_replicate_original.sh` | paper figures and tables from the deposited checkpoints; "does not run simulations or solvers" | unchanged; two clean checkouts on machine 1, one on machine 2 | exit 0; 105 s, 107 s and 70 s. **5 of 5 paper tables match the printed values, every cell** |
| 4 `4_validate_BE.sh` | restart five deposited solutions for 10 iterations, recompute the error checks | `N_PROCS` 16 to 4, machine 1 only | all five solver restarts finished; post-processing still running |
| 3 and 5 | solve from scratch (about 17 h at 16 processes; about 346 h on a cluster) | not run | no claim |

Tables compared cell by cell at the precision the paper prints, with
[`compare_tables.py`](compare_tables.py) (its failure injections are in [`tests/`](tests/)):

| Paper table | Cells | Machine 1 | Machine 2 |
|---|---|---|---|
| Table 2 (2D Fernandes-Phelan errors) | 4 | match | match |
| Table 4 (10D errors) | 4 | match | match |
| Table 5 (10D max values) | 10 | match | match |
| Table 7 (2D overreporting errors) | 8 | match | match |
| Table 8 (4D overreporting errors) | 8 | match | match |

All nine `.tex` files Step 2 writes (the five tables plus four supplementary error tables) were byte-identical across
the two machines ([public log](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/44935730364)). The six
figure PDFs differ in bytes between runs, as the protocol expected; they were not compared and no claim is made about them.

## What Step 2 does not show

Step 2 is a replay, and the README says so. Tables 2, 7 and 8, and the second row of Table 4, are formatted from error
and simulation files committed in the package (`V_func_error_*.txt`, `simulation_*.txt`). Table 5 and the first row of
Table 4 are read from metrics stored inside the committed checkpoints. A match therefore shows that the committed
intermediate files produce the printed tables in a fresh pinned environment, not that the solver produces those files.
Step 4 is the part that recomputes.

## Environment

| | Machine 1 | Machine 2 |
|---|---|---|
| What | cloud container | GitHub-hosted runner `ubuntu-24.04` |
| OS | Ubuntu 24.04.5 LTS | Ubuntu 24.04 |
| CPU | 4 vCPU, Intel Xeon @ 2.10GHz | 4 vCPU, Intel Xeon 6975P-C |
| RAM | 15 GB | 15 GB |
| GPU | none | none |
| Installer | Miniforge 26.9.4-2, SHA-256 `bbaf16b3…bdf` | same bytes, checked |

Python 3.9.23 (conda-forge). Key packages as the authors pin them: torch 2.4.0, gpytorch 1.13, linear-operator 0.5.3,
scipy 1.13.1, numpy 2.0.2, hydra-core 1.3.2, mpi4py 4.1.2, Tasmanian 8.2. OpenMPI 5.0.11 and GNU parallel 20260922 from
conda-forge. The full `pip freeze` (149 lines) is in [`evidence/env-pip-freeze.txt`](evidence/env-pip-freeze.txt) and was
identical on machine 2. The conda list is in [`evidence/env-conda-explicit.txt`](evidence/env-conda-explicit.txt).

## Deviations, in order

1. **Source.** The journal's deposit could not be fetched: this machine's network allows GitHub and PyPI only, so
   Zenodo was refused. The authors' GitHub repository was used. Whether it is byte-identical to the deposit is not known.
2. **GNU parallel version.** The README names 20231122; `1_install.sh` installs it unpinned, which gave 20260922. Not
   edited. It is only used in Step 4.
3. **Step 2 cleanup messages.** The script's first lines delete files that a clean checkout does not have, so it prints
   70 `rm: cannot remove` lines. They do not change the exit code or the outputs. Not edited.
4. **Step 4 process count.** `N_PROCS=16` changed to `N_PROCS=4` ([diff](evidence/deviation-1-nprocs.diff)), as the README
   allows. The README says rank count changes random draws, so Step 4 numbers are not expected to be bit-identical.
5. **Running as root.** The container runs as root, so OpenMPI needed `OMPI_ALLOW_RUN_AS_ROOT=1` and
   `OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1` in the environment. No file edited.
6. **Step 4, first attempt aborted by me.** About 17 minutes in, I ran `git stash` and `git stash pop` in its working
   tree while it ran. That could have changed what it read, so I stopped it and started again from a fresh clone. The
   aborted log is kept in `evidence/logs/`.
7. **Step 4, second attempt stopped by my own time limit.** I launched it with a 2-hour limit. All five solver restarts
   had finished (last at 20:11 UTC); the limit stopped the post-processing step at 20:22. I ran the script's remaining
   lines, from `parallel` onward, unchanged in the same tree, from
   [`4_validate_BE.resume-from-postprocess.sh`](evidence/4_validate_BE.resume-from-postprocess.sh).
8. **Step 4 is much slower here than the README says.** The README gives about 1 hour at 16 processes. Here, on 4
   cores, the solver restarts took 1 h 47 min and post-processing had run for over 3.5 hours at the time of writing.
   The simulation inside post-processing writes one line per step, which is how progress was read.

## Failed or stopped runs

- Machine 2, first workflow run: failed in my own hashing line before any package code ran. 14 tracked entries are
  symlinks to directories, which `sha256sum` cannot hash. Fixed by hashing regular files only.
- Step 4 attempts 1 and 2: deviations 6 and 7.

## Triage got this package wrong

Before the rerun, [`triage.py`](../triage/README.md) said **blocked**: Mathematica required, plus 16 absolute paths. A
hand reading says neither holds. The README says the Mathematica notebooks are reference material and not needed for
any table, and the "absolute paths" are `os.path.abspath` calls on relative paths. It also listed `hydra` as an
undeclared dependency, though `hydra-core` is pinned. Kept as found in
[`evidence/triage-verdict.md`](evidence/triage-verdict.md); triage is parked and is not being fixed here.

## Cost

Machine 2 was a GitHub runner on a public repository: no charge. Machine 1 is a 4 vCPU, 15 GB container. At a typical
on-demand price for that size, around $0.20 an hour, Steps 1 and 2 cost about 2 cents. Step 4 so far is about 6 hours, so
about $1.20. Total wall clock: about 2 minutes for Step 2, plus about 5 minutes of install the first time.

## Evidence

- [`evidence/logs/`](evidence/logs/): full stdout and stderr of every step, with start, end, exit code and seconds.
- [`evidence/step2/`](evidence/step2/): everything Step 2 wrote, with hashes in `evidence/step2.sha256`.
- [`evidence/`](evidence/): package hashes, the environment, the triage verdict and the Step 4 diff.
- [`.github/workflows/restud-renner-scheidegger.yml`](../.github/workflows/restud-renner-scheidegger.yml): the machine 2
  procedure. Anyone with a GitHub account can rerun it.
