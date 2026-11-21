"""Run the frozen task against pinned weights with the network off, and write everything a third party needs to check it.

Order of checks, each one a refusal with its own exit code before any weights are loaded:
  5  the checkout has modified tracked files (unless --allow-dirty, which is then recorded with the diff)
  2  the task files differ from FROZEN.json, or the weights directory differs from MODEL.json in any file, byte or name
  3  a network interface other than lo exists, or a probe connection does not fail
Then a socket audit hook is installed, the runtime is imported, and every item is scored. Any connect, DNS lookup or
sendto during the run is blocked and listed in run.json, and the run ends with exit 4. The audit hook sees Python-level
socket calls only; the network namespace is the real guarantee, the hook is the record.

The output directory must not exist. run.json is written on every outcome, refusals included.

usage: python -I offline-model/harness.py --weights DIR --out DIR [--runtime FILE] [--allow-dirty]"""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
import platform
import resource
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAT = "offline-run/1"
NETWORK_EVENTS = {"socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyname_ex",
                  "socket.gethostbyaddr", "socket.sendto", "socket.sendmsg"}


class Refusal(Exception):
    def __init__(self, code: int, reason: str):
        super().__init__(reason)
        self.code, self.reason = code, reason


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(top: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(top), *args], capture_output=True, text=True, check=True).stdout


def check_checkout(top: Path, allow_dirty: bool, rec: dict):
    rec["checkout"] = {"commit": git(top, "rev-parse", "HEAD").strip()}
    dirty = git(top, "status", "--porcelain", "--untracked-files=no").strip()
    rec["checkout"]["dirty"] = bool(dirty)
    if dirty:
        rec["checkout"]["status"] = dirty.splitlines()
        rec["checkout"]["diff"] = git(top, "diff", "HEAD")
        if not allow_dirty:
            raise Refusal(5, f"checkout has modified tracked files: {dirty.splitlines()}")


def check_task(rec: dict):
    pinned = json.loads((HERE / "FROZEN.json").read_text(encoding="utf-8"))["files"]
    rec["task"] = {}
    for name in ("task/items.jsonl", "task/prompt.json"):
        digest = sha256_file(HERE / name)
        rec["task"][name] = digest
        if pinned.get(name) != digest:
            raise Refusal(2, f"{name} is {digest}, FROZEN.json pins {pinned.get(name)}")


def check_weights(weights: Path, rec: dict):
    model = json.loads((HERE / "MODEL.json").read_text(encoding="utf-8"))
    rec["model"] = {"repo": model["repo"], "revision": model["revision"], "licence": model.get("licence"),
                    "model_json_sha256": sha256_file(HERE / "MODEL.json"), "files": {}}
    if not weights.is_dir():
        raise Refusal(2, f"weights directory {weights} does not exist")
    present = {p.relative_to(weights).as_posix() for p in weights.rglob("*") if p.is_file()}
    expected = set(model["files"])
    if present - expected:
        raise Refusal(2, f"unlisted files in weights directory: {sorted(present - expected)}")
    if expected - present:
        raise Refusal(2, f"files in MODEL.json missing from weights directory: {sorted(expected - present)}")
    for name in sorted(expected):
        digest = sha256_file(weights / name)
        rec["model"]["files"][name] = digest
        if digest != model["files"][name]["sha256"]:
            raise Refusal(2, f"{name} is {digest}, MODEL.json pins {model['files'][name]['sha256']}")


def check_network(rec: dict):
    names = sorted(n for _, n in socket.if_nameindex())
    probe = "connected"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect(("1.1.1.1", 443))
    except OSError as e:
        probe = f"failed: {e}"
    finally:
        s.close()
    rec["network"] = {"interfaces": names, "probe_1.1.1.1:443": probe}
    if names != ["lo"]:
        raise Refusal(3, f"network interfaces other than lo present: {names}")
    if probe == "connected":
        raise Refusal(3, "probe connection to 1.1.1.1:443 succeeded")


def install_socket_guard(attempts: list):
    def hook(event, args):
        if event in NETWORK_EVENTS:
            attempts.append({"event": event, "args": repr(args[1:] if event.startswith("socket.connect")
                                                          or event.startswith("socket.send") else args)[:300]})
            raise PermissionError(f"network call blocked by offline harness: {event}")
    sys.addaudithook(hook)


def environment() -> dict:
    env = {"python": sys.version, "executable": sys.executable, "platform": platform.platform(),
           "machine": platform.machine(), "cpu_count": os.cpu_count(), "uid": os.getuid() if hasattr(os, "getuid") else None}
    try:
        cpu = Path("/proc/cpuinfo").read_text()
        env["cpu_model"] = next((l.split(":", 1)[1].strip() for l in cpu.splitlines() if l.startswith("model name")), None)
        flags = next((l.split(":", 1)[1].split() for l in cpu.splitlines() if l.startswith("flags")), [])
        env["cpu_flags_simd"] = sorted(f for f in flags if f.startswith(("avx", "sse4", "fma", "amx")))
        mem = Path("/proc/meminfo").read_text().splitlines()[0]
        env["mem_total"] = mem.split(":", 1)[1].strip()
        env["os_release"] = dict(l.split("=", 1) for l in Path("/etc/os-release").read_text().splitlines() if "=" in l).get("PRETTY_NAME", "").strip('"')
    except OSError:
        pass
    from importlib import metadata
    env["packages"] = sorted(f"{d.metadata['Name']}=={d.version}" for d in metadata.distributions())
    return env


def load_runtime(path: Path):
    spec = importlib.util.spec_from_file_location("offline_runtime", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(a) -> int:
    started = time.time()
    t0 = time.perf_counter()
    rec = {"format": FORMAT, "argv": sys.argv, "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "status": None, "exit_code": None, "blocked_network_attempts": []}
    out: Path = a.out
    if out.exists():
        print(f"refuse: {out} already exists; every run gets a new directory", file=sys.stderr)
        return 6
    out.mkdir(parents=True)
    for k in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_DATASETS_OFFLINE"):
        os.environ[k] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    try:
        check_checkout(HERE.parent, a.allow_dirty, rec)
        check_task(rec)
        check_weights(a.weights, rec)
        check_network(rec)
        install_socket_guard(rec["blocked_network_attempts"])
        rec["environment"] = environment()
        runtime_path = a.runtime.resolve()
        rec["runtime_file"] = {"path": runtime_path.relative_to(HERE).as_posix() if runtime_path.is_relative_to(HERE)
                               else str(runtime_path), "sha256": sha256_file(runtime_path)}
        rec["harness_sha256"] = sha256_file(Path(__file__))
        prompt = json.loads((HERE / "task/prompt.json").read_text(encoding="utf-8"))
        items = [json.loads(l) for l in (HERE / "task/items.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        t_load = time.perf_counter()
        rt = load_runtime(runtime_path).Runtime(str(a.weights))
        rec["load_seconds"] = round(time.perf_counter() - t_load, 3)
        rec["runtime"] = rt.info()
        rows = []
        t_score = time.perf_counter()
        for it in items:
            ly, ln, prompt_sha, n_tokens = rt.score(prompt["system"], prompt["user_template"].format(text=it["text"]))
            rows.append({"id": it["id"], "label": it["label"], "pred": "YES" if ly > ln else "NO",
                         "logit_yes": ly, "logit_no": ln, "prompt_sha256": prompt_sha, "prompt_tokens": n_tokens})
        rec["score_seconds"] = round(time.perf_counter() - t_score, 3)
        if rec["blocked_network_attempts"]:
            raise Refusal(4, f"{len(rec['blocked_network_attempts'])} network call(s) attempted during the run")
        pred = io.StringIO(newline="")
        w = csv.writer(pred, lineterminator="\n")
        w.writerow(["id", "label", "pred"])
        for r in rows:
            w.writerow([r["id"], r["label"], r["pred"]])
        logits = io.StringIO(newline="")
        w = csv.writer(logits, lineterminator="\n")
        w.writerow(["id", "logit_yes", "logit_no", "margin", "prompt_tokens", "prompt_sha256"])
        for r in rows:
            w.writerow([r["id"], repr(r["logit_yes"]), repr(r["logit_no"]), repr(r["logit_yes"] - r["logit_no"]),
                        r["prompt_tokens"], r["prompt_sha256"]])
        (out / "predictions.csv").write_bytes(pred.getvalue().encode("utf-8"))
        (out / "logits.csv").write_bytes(logits.getvalue().encode("utf-8"))
        correct = sum(r["label"] == r["pred"] for r in rows)
        conf = {f"label_{l}_pred_{p}": sum(r["label"] == l and r["pred"] == p for r in rows)
                for l in ("YES", "NO") for p in ("YES", "NO")}
        rec["result"] = {"items": len(rows), "correct": correct, "accuracy": round(correct / len(rows), 6), "confusion": conf}
        rec["outputs"] = {n: sha256_file(out / n) for n in ("predictions.csv", "logits.csv")}
        rec["status"], rec["exit_code"] = "ok", 0
    except Refusal as r:
        rec["status"] = "failed" if r.code == 4 else "refused"
        rec["exit_code"], rec["reason"] = r.code, r.reason
        print(f"{rec['status']}: {r.reason}", file=sys.stderr)
    except Exception as e:  # anything else is a failed run, recorded, never hidden
        rec["status"], rec["exit_code"], rec["reason"] = "failed", 1, f"{type(e).__name__}: {e}"
        print(f"failed: {rec['reason']}", file=sys.stderr)
    ru = resource.getrusage(resource.RUSAGE_SELF)
    rec["wall_seconds"] = round(time.perf_counter() - t0, 3)
    rec["cpu_seconds"] = round(ru.ru_utime + ru.ru_stime, 3)
    rec["max_rss_kib"] = ru.ru_maxrss
    rec["ended_utc"] = datetime.fromtimestamp(started + rec["wall_seconds"], timezone.utc).isoformat(timespec="seconds")
    (out / "run.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")
    if rec["status"] == "ok":
        print(f"ok: {rec['result']['correct']}/{rec['result']['items']} correct, wall {rec['wall_seconds']} s")
    return rec["exit_code"]


def main(argv: list) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--runtime", type=Path, default=HERE / "runtime_transformers.py")
    ap.add_argument("--allow-dirty", action="store_true")
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
