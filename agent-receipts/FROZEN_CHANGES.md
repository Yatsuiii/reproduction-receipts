# Changes to frozen agent-receipts files

Every change to a file pinned in `FROZEN.json` is logged here before the registry is updated, with the date, the files, the reason
and whether results had already been seen when the change was made.

- 2026-11-21: registry created. `FORMAT.md`, `injections/injections.py` and `injections/EXPECTED.json` written before
  `agent_receipts/` existed. No results seen.
- 2026-11-21, adapters: added `adapter_injections/` (`EXPECTED.json`, `tamper.py`) for the LangGraph, OpenAI Agents SDK and
  CrewAI adapters, written before any adapter code. No existing frozen file changed. v0 results had been seen; these cases test
  the adapters' fidelity (failures recorded as errors, nothing missed) and the frameworks' own records as the baseline.
