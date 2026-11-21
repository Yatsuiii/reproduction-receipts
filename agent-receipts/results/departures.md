# Departures from the frozen expectations

`EXPECTED.json` was written before the implementation. Where a verifier did something else, it is listed here and left in the
results rather than fitted away. `EXPECTED.json` is unchanged.

## reorder, unsigned hash chain baseline: caught when expected to pass

Expected: an outsider swaps two calls and recomputes the unsigned chain, so the baseline should pass it.
Got: the baseline failed it with `clock_backwards`.

Why: the injection's repair step recomputes `seq`, `prev`, `session` and the close count, but not timestamps. After the swap a
later call sits before an earlier one, and the clock check fires. A real outsider editing an unsigned file can rewrite the
timestamps too, so this is a gap in the simulated attacker, not a strength of the baseline. It makes the baseline look one
detection better than it is (5/14 instead of 4/14). The comparison still stands with the extra point given to the baseline.
