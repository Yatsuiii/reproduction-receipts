# Receipt generator

Step two of a reproduction check. Given a spec (repository, commit, the exact commands, the outputs each command should
write), [`rerun.py`](rerun.py) clones the repository into an empty directory, checks out the commit, hashes every tracked
file, runs each command with a time limit, compares each declared output with the committed file of the same path, and
writes the receipt in a fixed template with every log attached.

```sh
python receiptgen/rerun.py path/to/spec.json --out some-receipt/
```

It writes `RECEIPT.md`, `results.json` (every number behind the receipt) and `evidence/` (file hashes, environment, one log
per command, every regenerated output). Stdlib only, Python 3.10+. It runs package code, so run it where that is acceptable.

## What it will and will not call reproduced

An output counts as reproduced only when all of these hold:

- the run wrote it (its modification time or content changed during the command), so a committed result that is merely
  read back is never counted;
- the command that wrote it exited 0;
- that command did not read a committed intermediate file (one the spec lists under `committed_intermediates`) that
  this run had not regenerated first. Reads are traced with `strace`; without it, nothing in such a spec counts;
- it equals the committed file byte for byte, or has the same text with every number equal within the spec's relative
  tolerance (default 1e-12).

Binary outputs can name a converter (for example an `Rscript` one-liner that prints an `.rds` file); when the bytes
differ, the converter's text output of both files is compared instead, and a match is reported as equal after conversion,
never as identical.

Everything else is reported by what happened: numbers that did not regenerate (each listed with both values), text that
differs, not rewritten, not produced, no committed file to compare with, or (for figures declared `hash-only`) rewritten
and hashed but not compared. A commit that is not in the repository stops the run before any package code runs. Changes
to tracked files that are not declared outputs are listed as deviations. The receipt refuses to render if its text says
a paper is wrong.

## How it was built

Same rules as the other receipts here.

1. **Failure injections first.** [`fixtures/`](fixtures/) holds 16 small packages, each with one way a rerun can go that a
   receipt must not misreport (cache replay, a command that writes its output and then fails, a timeout, a missing commit,
   an undeclared edit, last-digit float noise, a changed number, a changed label, a binary file whose header names the
   writer's version, a table formatted from a committed intermediate). [`fixtures/EXPECTED.json`](fixtures/EXPECTED.json)
   fixes the outcome for each. Both were committed before `rerun.py` existed.
2. **Frozen.** [`FROZEN.json`](FROZEN.json) pins every fixture and the two entry points by SHA-256; the pre-commit hook runs
   [`check_frozen.py`](check_frozen.py). Every change is logged in [`FROZEN_CHANGES.md`](FROZEN_CHANGES.md).
3. **Cheap baseline next to the number.** The receipt most people would write by hand says an output reproduced whenever
   its command exited 0.

| | Cases right |
|---|---|
| `rerun.py` | 16/16 ([`results/fixtures.json`](results/fixtures.json)) |
| Receipt text rules (no "wrong", reproduced column matches, failed runs listed with logs, environment and cost named) | 16/16 |
| Naive baseline, "exit 0 means reproduced" | 10/16 |

The naive baseline is wrong on a changed number, a cache replay, a missing output, an output with nothing to compare,
a changed label, and a table formatted from a committed intermediate. That last case was found on a real package (Conlon
and Rao, JPE), where the first version of `rerun.py` made the same mistake; the injection was added before the fix. Fixture scores measure what the author thought to inject, not accuracy on real packages; real runs
are the [receipts](../README.md) themselves.

## Tests

```sh
python -m unittest discover -s receiptgen/tests
```
