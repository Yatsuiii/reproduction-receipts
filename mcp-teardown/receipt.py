"""Render one receipt per CONFIRMED target. Sends nothing.

    python mcp-teardown/receipt.py --results /var/tmp/mcpt-results/<run> --out mcp-teardown/receipts/<run>

Each receipt is addressed to that one repository's maintainers and carries only
their own finding. Wording rules, from the project's receipt rules:
- never say the server is wrong; say what the process table showed;
- never claim anything a trial in this run did not produce;
- name the artefact, environment, versions, hardware, wall clock and cost;
- list every deviation and every failed or dead run;
- close with one question, and ask for nothing else.

Prior-art search is NOT automated. Each receipt carries an unchecked box, and
a receipt with that box unchecked is not ready to send.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TEMPLATE = """\
# Teardown receipt: {name}

To the maintainers of [{repo}](https://github.com/{repo}). This was run unasked; nothing here is a request.

## What was observed

When an MCP client shut down `{artefact_spec}` over stdio, using the sequence in the MCP lifecycle spec
(close stdin, wait {eof}s, SIGTERM, wait {term}s, SIGKILL) and sending those signals to the server's
own pid, processes the server had started were still running {settle}s later in
**{pid_leaks} of {pid_n} trials**.

Sending the same signals to the server's whole process group instead left none in
**{grp_leaks} of {grp_n} trials**. Nothing else differed between the two arms.

This is a description of the process table, not a judgement on the code. The reason the processes
outlive the server is not established by this run.

Residue from one representative trial (pid arm):

```
{residue}
```

How the server exited in the pid arm: {exit_stages}.

## What ran

| | |
|---|---|
| Package | `{artefact_spec}` (resolved `{resolved}`) |
| Artefact | {artefact_id} |
| Launch command | `{argv}` |
| Registry entry | `{registry_name}` version `{registry_version}`, registry snapshot sha256 `{snapshot}` |
| Handshake | initialize, notifications/initialized, tools/list; all {total} trials answered ({tools} tools listed) |
| Runner | `mcp-teardown/runner.py` sha256 `{runner_sha}` |
| Environment | {os}; {cpu} ({cpus} vCPU, {mem} GB); node {node}; npm {npm}; Python {python}; {uv} |
| Wall clock | {wall}s for this target, {run_wall}s for the whole batch of {n_targets} |
| Cost | No paid API or model calls. Compute was a shared cloud container; marginal cash cost of this run: $0. |

## Deviations from a normal install

- Installed with lifecycle scripts disabled (`npm --ignore-scripts`, or wheels only on PyPI), so no package
  code ran outside the sandbox.
- The entry point was launched directly, not through `npx` or `uvx`, so a wrapper's behaviour is not
  counted against the server.
- Ran as user `nobody`, with no network (`unshare --net`) and an empty environment apart from HOME,
  TMPDIR, PATH and the trial tag `SHUTDOWN_INTEGRITY_TRIAL`.
{env_deviation}- No tool was called. Only start-up and shutdown were exercised.

## Every run

| # | Arm | Handshake | Exit | Teardown returned (s) | Residual processes |
|---|---|---|---|---:|---:|
{trial_rows}

## How to check this yourself

```
git clone https://github.com/Yatsuiii/reproduction-receipts
cd reproduction-receipts
echo '{target_line}' > one.jsonl
sudo python3 mcp-teardown/runner.py --targets one.jsonl --workers 1
```

Linux only (it reads `/proc`). The runner first proves its own controls: a fixture that leaks must be
CONFIRMED and one that cleans up must pass 10 of 10, or it reports nothing.

## Limits

One machine, one package version, start-up and shutdown only. A residual process here may be harmless
by design. No stated teardown contract was looked for in the project.

- [ ] Prior-art search on the repository's issues done before sending (not automated)

Is this useful?
"""


def render(r: dict, run: dict) -> str:
    t = r["target"]
    inst = r["install"]
    a = inst["artefact"]
    env = run["environment"]
    trials = r["trials"]
    conf = trials[1:]
    pid = [x for x in conf if x["arm"] == "pid"]
    grp = [x for x in conf if x["arm"] == "group"]
    rep = next((x for x in pid if x["residuals"]), None)
    residue = "\n".join(f"pid={p['pid']} ppid={p['ppid']} state={p['state']} {p['cmdline']}" for p in rep["residuals"])
    stages: dict[str, int] = {}
    for x in pid:
        stages[x["exit_stage"]] = stages.get(x["exit_stage"], 0) + 1
    if a.get("registry") == "npm":
        artefact_id = f"npm integrity `{a.get('integrity')}`"
    else:
        files = a.get("published_files") or []
        artefact_id = "; ".join(f"`{f['filename']}` sha256 `{f['sha256']}`" for f in files) or "PyPI digests not retrieved"
    env_dev = ""
    if t.get("required_env"):
        env_dev = (f"- Required environment variables were set to a placeholder, not a real credential: "
                   f"{', '.join('`' + n + '`' for n in t['required_env'])}.\n")
    rows = "\n".join(
        f"| {i} | {x['arm']}{' (screen)' if i == 0 else ''} | {'ok' if x['handshake_ok'] else 'FAILED'} | "
        f"{x['exit_stage']} | {x['teardown_return_s']} | {len(x['residuals'])} |"
        for i, x in enumerate(trials))
    line = json.dumps({k: v for k, v in t.items()}, sort_keys=True).replace("'", "'\\''")
    tm = env["timeouts"]
    return TEMPLATE.format(
        name=t["name"], repo=t["repo"], artefact_spec=a.get("spec"), resolved=a.get("resolved_version"),
        eof=tm["eof_wait_s"], term=tm["term_wait_s"], settle=tm["settle_s"],
        pid_leaks=r["counts"]["pid_with_residue"], pid_n=r["counts"]["pid_trials"],
        grp_leaks=r["counts"]["group_with_residue"], grp_n=r["counts"]["group_trials"],
        residue=residue, exit_stages=", ".join(f"{k} x{v}" for k, v in sorted(stages.items())),
        artefact_id=artefact_id, argv=" ".join(inst["argv"]), registry_name=t["name"],
        registry_version=t.get("version"), snapshot=t.get("registry_snapshot_sha256"),
        total=len(trials), tools=trials[0].get("tool_count"), runner_sha=env["runner_sha256"],
        os=env["os"], cpu=env["cpu"], cpus=env["cpus"], mem=env["mem_gb"], node=env["node"], npm=env["npm"],
        python=env["python"], uv=env["uv"], wall=r.get("wall_clock_s"), run_wall=run.get("wall_clock_s"),
        n_targets=run.get("n_targets"), env_deviation=env_dev, trial_rows=rows, target_line=line)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    run = json.loads((args.results / "run.json").read_text())
    args.out.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(args.results.glob("*/result.json")):
        if f.parent.name.startswith("_"):
            continue
        r = json.loads(f.read_text())
        if r.get("verdict") != "CONFIRMED":
            continue
        (args.out / f"{f.parent.name}.md").write_text(render(r, run))
        n += 1
    print(f"{n} receipts written to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
