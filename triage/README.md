# Package triage

Step one of a reproduction check. Given a replication package, `triage.py` decides in about a second whether it can run at all on
this desk, and why not, before anyone spends a day on it.

```sh
python triage/triage.py path/to/package            # a directory
python triage/triage.py package.zip --have stata   # a .zip or .tar.gz; declare the proprietary software the desk has
python triage/triage.py https://github.com/o/r --commit SHA --check-links --json verdict.json --md verdict.md
```

It prints one of three verdicts, each with the findings behind it and `file:line` evidence:

- **runnable**: nothing found that stops an as-is run.
- **runnable-with-deviations**: it can probably run, after changes a receipt must log (choosing versions, editing paths,
  downloading data, choosing a run order).
- **blocked**: something the desk cannot supply is missing: restricted data, proprietary software it lacks, a required input
  that is not in the package, or a data link that fails.

What it checks: languages and proprietary software; pinned versions (requirements, conda, lockfiles, `renv.lock`, Stata `version`
and `ssc install`, Julia manifests); APIs removed from current releases; Python 2 code; every file the code reads, whether the
package has it, writes it, or documents where it comes from; restricted-data language in the README; data fetched at run time;
links (with `--check-links`); absolute paths; a master script or documented run order; claimed run time and GPUs; licences; and
committed outputs that a run might replay instead of recompute.

It never executes package code, and it is stdlib-only Python 3.10+, so a desk can run it on its own machine with nothing installed
and nothing leaving its network (only `--check-links` and git URLs touch the network). The verdict says whether the committed
materials can run here. It says nothing about whether a paper's results are correct.

## How it was built

Same rules as the receipts.

1. **Failure injections first.** [`fixtures/`](fixtures/) holds small packages, each with one injected reason it cannot run (or
   none), and [`fixtures/EXPECTED.json`](fixtures/EXPECTED.json) the verdict each must get. They were committed before `triage.py`
   existed ([commit history](https://github.com/Yatsuiii/reproduction-receipts/commits/main/triage)).
2. **Frozen.** [`FROZEN.json`](FROZEN.json) pins every fixture by SHA-256. `scripts/hooks/pre-commit` runs
   [`check_frozen.py`](check_frozen.py) and blocks a commit that changes one without updating the registry; every change is logged
   in [`FROZEN_CHANGES.md`](FROZEN_CHANGES.md). Install with `git config core.hooksPath scripts/hooks`.
3. **Cheap baselines next to every number.** [`run_fixtures.py`](run_fixtures.py) scores triage against always-runnable and
   readme-and-code on the same cases.
4. **Failures stay visible.** v1's misses are kept in `results/*.v1.*`; held-out failures are listed in
   [`results/heldout_review.md`](results/heldout_review.md) and not fixed in the same round.

## Results so far

| Set | Triage | always-runnable | readme-and-code | File |
|---|---|---|---|---|
| Round 1 fixtures, v1 | 16/16 | 5/16 | 6/16 | commit 52fb824 (tests) |
| Round 1 + 2 fixtures, v1 | 17/21 | 7/21 | 8/21 | [`fixtures.v1.json`](results/fixtures.v1.json) |
| Round 1 + 2 fixtures, v2 | 21/21 | 7/21 | 8/21 | `results/fixtures.json` at commit 3350bd0 |
| Six held-out journal packages, v2, verdict | 4/6 | 0/6 | 0/6 | [`heldout_review.md`](results/heldout_review.md) |
| Same six, verdict and main reason | 3/6 | n/a | n/a | [`heldout_review.md`](results/heldout_review.md) |
| Round 3 fixtures (13 cases from held-out failures), v2 | 23/34* | 12/34 | 13/34 | [`fixtures.v2.json`](results/fixtures.v2.json) |
| Round 3 fixtures, v3 | 36/36 | 14/36 | 15/36 | [`fixtures.json`](results/fixtures.json) |
| Six new held-out packages, v3, verdict | 4/6 | 0/6 (always-blocked 3/6) | 0/6 | [`heldout_r3_review.md`](results/heldout_r3_review.md) |
| Same six, verdict and main reason | 2/6 | n/a | n/a | [`heldout_r3_review.md`](results/heldout_r3_review.md) |

\* Scored on the first 34 cases. The last two were written after the v3 draft (see `FROZEN_CHANGES.md`); that draft scored 34/36 ([`fixtures.v3draft.json`](results/fixtures.v3draft.json)).

Fixture scores measure whether triage catches what its author thought to inject; they are not accuracy on real packages. The
held-out rows are the ones that count. In round 2, **an always-blocked baseline also got 4/6**, because most economics packages are
blocked by confidential data and the verdict alone is cheap to guess. In round 3, triage got 4/6 against 3/6 for always-blocked, but
its stated reason was right only 2 times in 6, down from 3 in 6. What round 3 did fix is a false claim: a refused connection is no
longer called a dead link. Every known failure is listed in the two reviews.

[frontiers2013](results/frontiers2013.md), the repository's next reproduction target, is a development case: v1 missed its
committed score caches, run-time downloads and removed APIs, and round 2 was written from those misses.

## Tests

```sh
python -m unittest discover -s triage/tests
```
