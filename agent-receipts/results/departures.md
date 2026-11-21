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

## CrewAI: the receipt has 9 calls where the plan, and CrewAI's own record, have 4

Expected (`adapter_injections/EXPECTED.json`, frozen before the adapters): statuses `ok, ok, error, ok`, the recorded calls
equal to the plan, and the receipt's calls equal to the calls in CrewAI's own record.

Got, with crewai 1.15.44: statuses `ok, ok, error, error, error, error, error, error, ok`. The receipt holds six attempts at
`lookup_order`. CrewAI's step callback, the framework's own record of the run, holds one.

Why: CrewAI re-ran the failing tool by itself. A counter inside the tool function confirmed six real executions in that run,
so the receipt is right and the frozen expectation was wrong about the framework. The adapter is not double-counting: it now
records at the tool function, which every CrewAI call path reaches exactly once (the first adapter draft recorded at `_run`,
which `@tool` tools bypass on some paths; it gave the same count here).

This is the kind of thing a receipt is for. CrewAI's record shows one failed lookup; the machine ran it six times. For a
read that is harmless. For a tool that charges a card or sends an email, it is six charges or six emails.
