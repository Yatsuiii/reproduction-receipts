# CrewAI runs a failing tool more times than its record shows

A lead from [`agent-receipts`](https://github.com/yatsuiii/reproduction-receipts/pull/5): in the CrewAI worked example, a
failing tool ran six times while CrewAI's own record showed one call. This folder checks that on its own, at a 10/10 bar,
with a negative control and a patch.

**Result: it reproduces 10 of 10, the patch fixes the hidden re-run 10 of 10, and it is already reported upstream.**
[crewAIInc/crewAI#9341](https://github.com/crewAIInc/crewAI/issues/9341) (open, 11 Nov 2026) describes the same code path
with the same counts, and [#9345](https://github.com/crewAIInc/crewAI/pull/9345) is an open fix. An earlier report,
[#7449](https://github.com/crewAIInc/crewAI/issues/7449), was closed with its fix PR [#7452](https://github.com/crewAIInc/crewAI/pull/7452)
still open. So there is nothing new to file. What this adds is a full-runtime reproduction (a real `Crew`, not a unit call
into `ToolUsage`) and the transient-failure arm below, which shows the first failure disappearing from every record.

## Setup

`check.py`: one agent, one task, one planned call to a tool `charge_card`. The model is a scripted `BaseLLM` (no API call,
$0) that asks for the tool once and then answers. A counter inside the tool counts real executions. crewai 1.15.44,
Python 3.12.3, Linux x86_64 (4 vCPU cloud container), 10 trials per arm. Wall clock under 5 seconds for all 30 trials; cost $0.

| arm | tool behaviour |
|---|---|
| `ok` | returns normally (negative control) |
| `always` | raises `TimeoutError` every time |
| `transient` | raises on the first execution only, the shape of a payment call that times out after the charge went through |

## Results, 10 of 10 trials identical in every cell

| arm | model asked | tool actually ran | step_callback tool steps | `ToolUsageStartedEvent` | `ToolUsageErrorEvent` |
|---|---:|---:|---:|---:|---:|
| ok, unpatched | 1 | 1 | 1 | 1 | 0 |
| always, unpatched | 1 | **6** | 1 | 3 | 3 |
| transient, unpatched | 1 | **2** | 1 | **1** | **0** |
| ok, patched | 1 | 1 | 1 | 1 | 0 |
| always, patched | 1 | 3 | 1 | 3 | 3 |
| transient, patched | 1 | 2 | 1 | 2 | 1 |

Raw trials: [`results/unpatched.json`](results/unpatched.json), [`results/patched.json`](results/patched.json).

Read it this way. In the `transient` arm the model asked for one charge, the card was charged twice, and no record CrewAI
keeps says anything failed: the step shows one successful call and the event bus shows one start and no error. In the
`always` arm even the event bus undercounts by half.

## Cause

`lib/crewai/src/crewai/tools/tool_usage.py`, in both `_ause` (lines 355-372) and `_use` (612-629) at commit
`56c26a7fb3ece62c64de52e8b4228d15c9c81492`: the fallback that retries with unfiltered arguments wraps the tool call itself,
so an exception raised *by the tool* is caught and the tool is run again. That doubles every failing execution, and when
the second run succeeds the first failure is never reported. On top of that, a raising tool is retried by `ToolUsage` up to
`_max_parsing_attempts` (3) times. The second layer is deliberate code; neither layer is described in the CrewAI docs
(`docs/edge/en/concepts/tools.mdx`, `agents.mdx` mention `max_retry_limit` for agent errors and `tool_failure_policy`,
not tool re-execution).

## Patch

[`run-tool-once.patch`](run-tool-once.patch) moves the tool call out of the fallback, so only the schema lookup can fall back
and the tool runs once per attempt. With it, executions equal `ToolUsageStartedEvent` count in every trial of every arm, and
the transient failure shows up as an error event. It leaves the deliberate three-attempt retry alone. It was applied to the
installed 1.15.44 package (the installed `tool_usage.py` is byte-identical to the file at the pinned commit).

## The second half of the lead: failed calls not flagged

Also checked: neither the OpenAI Agents SDK nor CrewAI's step record marks a failed tool call as failed, only as error text.
For the Agents SDK this is documented and intended (`docs/tools.md`, `failure_error_function`: a crashing tool returns an
error message to the model). CrewAI now documents `ToolFailure` and `tool_failure_policy` for this. Not a bug in either.

## Reproduce

```
pip install crewai==1.15.44
python crewai-tool-retry/check.py -n 10 --out unpatched.json
# apply the patch to site-packages/crewai/tools/tool_usage.py (patch -p4 from site-packages)
python crewai-tool-retry/check.py -n 10 --out patched.json
```
