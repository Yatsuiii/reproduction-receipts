"""Client teardown runner.

Question: when an MCP client, agent framework or agent CLI closes a stdio MCP
server through its own documented API, is anything that server started still
running afterwards?

Each target is a *driver*: a small program, in the target's own language, that
uses the target's public API to connect to one stdio server, list its tools,
call `ping`, and close the session the way the target's docs say to. The driver
then prints one `CLOSED {json}` line and stays alive, because a real host (an
IDE, an agent server) keeps running after it closes a session. The runner waits
SETTLE seconds, reads /proc, and only then lets the driver exit.

The server command is chosen by the runner, per scenario, from fixtures/:

    clean        exits on stdin EOF            negative control, must leave nothing
    eof-ignore   ignores EOF, exits on SIGTERM spec shutdown step 2
    term-ignore  ignores EOF and SIGTERM       spec shutdown step 3 (SIGKILL)
    wrapped      wrapper.mjs -> eof-ignore     launcher between client and server

Residue is any process whose argv carries the trial tag. The tag is in argv
because several clients hand the server a reduced environment.

Nothing reports unarmed: `--arm` runs three reference clients written here
(no kill, spec sequence on the pid, spec sequence on the process group) and
the batch refuses to score targets unless every reference cell comes out as
expected in every trial.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
NODE = shutil.which("node") or "node"

SCENARIOS = ("clean", "eof-ignore", "term-ignore", "wrapped")
EARLY = 3.0   # first read of the process table after CLOSED (recorded, not scored)
SETTLE = 10.0  # scored read: the spec sequence (EOF, wait, SIGTERM, wait, SIGKILL) fits well inside this
DRIVER_TIMEOUT = 90.0


def server_command(scenario: str, tag: str, marker_dir: str) -> tuple[str, list[str]]:
    server = str(FIXTURES / "server.mjs")
    if scenario == "wrapped":
        return NODE, [str(FIXTURES / "wrapper.mjs"), NODE, server, "eof-ignore", tag, marker_dir]
    return NODE, [server, scenario, tag, marker_dir]


def tagged(tag: str) -> list[dict]:
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            raw = Path(f"/proc/{pid}/cmdline").read_bytes()
            stat = Path(f"/proc/{pid}/stat").read_text()
        except OSError:
            continue
        if tag.encode() not in raw:
            continue
        state = stat.rsplit(")", 1)[1].split()[0]
        if state == "Z":
            continue  # a zombie holds no resources beyond its slot; its parent is alive
        out.append({"pid": int(pid), "cmd": raw.replace(b"\0", b" ").decode(errors="replace").strip()[:200]})
    return out


def kill_tagged(tag: str) -> None:
    for _ in range(3):
        procs = tagged(tag)
        if not procs:
            return
        for p in procs:
            try:
                os.kill(p["pid"], signal.SIGKILL)
            except OSError:
                pass
        time.sleep(0.2)


def run_trial(driver: list[str], scenario: str, env_extra: dict | None = None, cwd: str | None = None) -> dict:
    tag = "cttrial-" + uuid.uuid4().hex[:12]
    marker_dir = tempfile.mkdtemp(prefix="ct-")
    command, args = server_command(scenario, tag, marker_dir)
    env = dict(os.environ)
    env.update(env_extra or {})
    env["CT_SPEC"] = json.dumps({"command": command, "args": args, "tag": tag})
    trial = {"tag": tag, "scenario": scenario}
    t0 = time.monotonic()
    errf = open(Path(marker_dir) / "driver.stderr", "w+")
    proc = subprocess.Popen(driver, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errf,
                            env=env, cwd=cwd, text=True, start_new_session=True)
    closed = None
    lines = []
    try:
        while True:
            if time.monotonic() - t0 > DRIVER_TIMEOUT:
                trial["error"] = "driver timeout before CLOSED"
                break
            line = proc.stdout.readline()
            if not line:
                trial["error"] = "driver exited before CLOSED"
                break
            lines.append(line.rstrip())
            if line.startswith("CLOSED"):
                body = line[len("CLOSED"):].strip() or "{}"
                try:
                    closed, _ = json.JSONDecoder().raw_decode(body)
                except json.JSONDecodeError:
                    closed = {"unparsed": body[:200]}
                break
        trial["closed"] = closed
        if closed is not None:
            time.sleep(EARLY)
            trial["residue_early"] = tagged(tag)
            time.sleep(SETTLE - EARLY)
            trial["residue"] = tagged(tag)
    finally:
        try:
            proc.stdin.close()
        except OSError:
            pass
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
        time.sleep(0.5)
        trial["residue_after_host_exit"] = tagged(tag)
        errf.seek(0)
        trial["stderr_tail"] = errf.read()[-600:]
        errf.close()
        trial["stdout_tail"] = lines[-5:]
        kill_tagged(tag)
        markers = Path(marker_dir) / f"{tag}.log"
        trial["markers"] = markers.read_text().split("\n")[:-1] if markers.exists() else []
        shutil.rmtree(marker_dir, ignore_errors=True)
    trial["seconds"] = round(time.monotonic() - t0, 2)
    trial["connected"] = any(m.startswith("initialize") for m in trial["markers"])
    return trial


def verdict(trial: dict) -> str:
    if trial.get("closed") is None or not trial["connected"]:
        return "DEAD"
    return "RESIDUE" if trial["residue"] else "CLEAN"


def run_cell(driver: list[str], scenario: str, n: int, **kw) -> dict:
    trials = [run_trial(driver, scenario, **kw) for _ in range(n)]
    counts: dict[str, int] = {}
    for t in trials:
        v = verdict(t)
        t["verdict"] = v
        counts[v] = counts.get(v, 0) + 1
    return {"scenario": scenario, "n": n, "counts": counts, "trials": trials}


REFERENCE = {
    # driver name -> expected verdict per scenario
    "ref-none": {"clean": "CLEAN", "eof-ignore": "RESIDUE", "term-ignore": "RESIDUE", "wrapped": "RESIDUE"},
    "ref-spec-pid": {"clean": "CLEAN", "eof-ignore": "CLEAN", "term-ignore": "CLEAN", "wrapped": "RESIDUE"},
    "ref-spec-group": {"clean": "CLEAN", "eof-ignore": "CLEAN", "term-ignore": "CLEAN", "wrapped": "CLEAN"},
}


def load_targets() -> dict:
    return json.loads((HERE / "targets.json").read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", action="store_true", help="run the reference clients and check the gate")
    ap.add_argument("--target", action="append", default=[], help="target id from targets.json (repeatable)")
    ap.add_argument("--scenario", action="append", default=[])
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=1, help="targets run in parallel (trials within a target stay serial)")
    ap.add_argument("--variant", default="", help="label for a patched run, stored in the result")
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    scenarios = a.scenario or list(SCENARIOS)
    targets = load_targets()
    ok = True
    if a.arm:
        for name, expected in REFERENCE.items():
            driver = [sys.executable, "-I", str(HERE / "drivers" / "reference.py"), name.removeprefix("ref-")]
            res = {"target": name, "cells": []}
            for sc in scenarios:
                cell = run_cell(driver, sc, a.n)
                cell["expected"] = expected[sc]
                cell["armed"] = cell["counts"].get(expected[sc], 0) == a.n
                ok &= cell["armed"]
                res["cells"].append(cell)
                print(f"{name:16} {sc:12} {cell['counts']} expected {expected[sc]} {'ok' if cell['armed'] else 'NOT ARMED'}", flush=True)
            (a.out / f"{name}.json").write_text(json.dumps(res, indent=1))
        if not ok:
            print("ARMING FAILED: targets are not scored", flush=True)
            return 1
    def run_target(tid: str) -> None:
        t = targets[tid]
        driver = [os.path.expandvars(x.replace("{here}", str(HERE))) for x in t["driver"]]
        res = {"target": tid, "variant": a.variant, "driver": t["driver"], "env": t.get("env"), "cells": []}
        for sc in scenarios:
            cell = run_cell(driver, sc, a.n, env_extra=t.get("env"),
                            cwd=t.get("cwd", "").replace("{here}", str(HERE)) or None)
            res["cells"].append(cell)
            print(f"{tid:28} {a.variant:10} {sc:12} {cell['counts']}", flush=True)
        name = tid + (f"--{a.variant}" if a.variant else "")
        (a.out / f"{name}.json").write_text(json.dumps(res, indent=1))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        list(ex.map(run_target, a.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
