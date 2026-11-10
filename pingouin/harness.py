"""Local, stdlib-only provenance wrapper. Never edits upstream analysis code."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import tomllib
import traceback

ROOT = Path(__file__).resolve().parent
BASE_PYTHON = Path(r"C:\Users\lenovo\AppData\Local\Programs\Python\Python312\python.exe")


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode("utf-8").strip()


def setup_command(run, name, command, cwd):
    start = time.perf_counter()
    result = subprocess.run(command, cwd=cwd, capture_output=True)
    (run / f"setup-{name}.stdout.txt").write_bytes(result.stdout)
    (run / f"setup-{name}.stderr.txt").write_bytes(result.stderr)
    record = {"command": command, "cwd": str(cwd), "exit_code": result.returncode,
              "wall_seconds": time.perf_counter() - start}
    path = run / "setup.json"
    records = json.loads(path.read_text()) if path.exists() else []
    records.append(record)
    write_json(path, records)
    print(f"setup {run.name}/{name}: exit {result.returncode}, {record['wall_seconds']:.3f}s", flush=True)
    if result.returncode:
        raise RuntimeError(f"Setup failed at {name}; see the captured logs. No analysis repair attempted.")
    return result.stdout


def prepare(number):
    run = ROOT / f"run-{number}"
    repo = run / "repo"
    plan = json.loads((ROOT / "PLAN.json").read_text())
    run.mkdir(exist_ok=True)
    if number == 2:
        if repo.exists():
            raise RuntimeError("Second checkout already exists; refusing to reuse it")
        setup_command(run, "clone", ["git", "-c", "core.autocrlf=false", "clone",
                      plan["repo_url"], str(repo)], ROOT)
        setup_command(run, "checkout", ["git", "checkout", "--detach", plan["commit_sha"]], repo)
    assert git(repo, "rev-parse", "HEAD") == plan["commit_sha"]
    assert not git(repo, "status", "--porcelain", "--untracked-files=all")
    write_json(run / "checkout.json", {"sha": plan["commit_sha"], "initial_status": "clean",
                                      "origin": git(repo, "remote", "get-url", "origin")})
    venv = run / "env"
    if venv.exists():
        raise RuntimeError("Environment already exists; refusing to reuse it")
    setup_command(run, "venv", ["uv", "venv", "--python", str(BASE_PYTHON), str(venv)], repo)
    python = venv / "Scripts/python.exe"
    if number == 1:
        build = tomllib.loads((repo / "pyproject.toml").read_text())["build-system"]["requires"]
        (ROOT / "build-requirements.in").write_text("\n".join(build) + "\n", encoding="utf-8")
        setup_command(run, "build-lock", ["uv", "pip", "compile", "--quiet", "--generate-hashes",
                      str(ROOT / "build-requirements.in"), "--output-file", str(ROOT / "BUILD.lock.txt")], repo)
    setup_command(run, "sync", ["uv", "pip", "sync", "--python", str(python), "--require-hashes",
                  str(ROOT / "DEPENDENCIES.lock.txt"), str(ROOT / "BUILD.lock.txt")], repo)
    setup_command(run, "install", ["uv", "pip", "install", "--python", str(python),
                  "--no-deps", "--no-build-isolation", "."], repo)
    frozen = setup_command(run, "freeze", ["uv", "pip", "freeze", "--python", str(python)], repo)
    (run / "environment.freeze.txt").write_bytes(frozen)
    assert not git(repo, "diff", "HEAD", "--name-only")
    print(f"Prepared {run.name}; upstream tracked files unchanged.", flush=True)


def example(readme):
    start = readme.index("5. One-way ANOVA using a pandas DataFrame")
    end = readme.index("6. Repeated measures ANOVA", start)
    match = re.search(r"\.\. code-block:: python\n\n((?:  .*(?:\n|$)|\n)+)", readme[start:end])
    return "\n".join(line[2:] if line.startswith("  ") else line
                     for line in match.group(1).rstrip().splitlines()) + "\n"


def execute(number):
    run = ROOT / f"run-{number}"
    if (run / "result.json").exists():
        raise RuntimeError("Analysis already attempted; refusing a retry")
    repo, venv = run / "repo", run / "env"
    python = venv / "Scripts/python.exe"
    plan = json.loads((ROOT / "PLAN.json").read_text())
    assert git(repo, "rev-parse", "HEAD") == plan["commit_sha"]
    assert not git(repo, "diff", "HEAD", "--name-only")
    assert example((repo / "README.rst").read_text()) == plan["readme_code"]
    actual_module = venv / "Lib/site-packages/pingouin/parametric.py"
    assert sha(actual_module) == sha(repo / "src/pingouin/parametric.py")
    for rel in plan["scientific_data_inputs"]:
        installed = venv / "Lib/site-packages" / Path(rel).relative_to("src")
        assert sha(installed) == sha(repo / rel)
    runtime = run / "runtime"
    env = {k: os.environ[k] for k in ["SystemRoot", "WINDIR", "COMSPEC", "PATHEXT"] if k in os.environ}
    env["PATH"] = str(venv / "Scripts") + os.pathsep + str(BASE_PYTHON.parent) + os.pathsep + os.path.join(os.environ["SystemRoot"], "System32")
    for key, subdir in {"HOME": "home", "USERPROFILE": "home", "APPDATA": "appdata", "LOCALAPPDATA": "localappdata",
                        "MPLCONFIGDIR": "mpl", "XDG_CACHE_HOME": "cache", "TEMP": "temp", "TMP": "temp"}.items():
        folder = runtime / subdir
        folder.mkdir(parents=True, exist_ok=True)
        env[key] = str(folder)
    command = [str(python), "-I", "-B", str(ROOT / "harness.py"), "worker", str(number)]
    entries = {}

    def add(path, role, logical):
        path = Path(path).resolve()
        if path.is_file():
            entries[str(path)] = {"role": role, "logical_path": logical,
                                  "bytes": path.stat().st_size, "sha256": sha(path)}

    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=repo).decode().split("\0")
    for name in filter(None, tracked):
        add(repo / name, "upstream_tracked_file", name)
    for path in venv.rglob("*"):
        if path.is_file():
            add(path, "isolated_environment", str(path.relative_to(venv)))
    base = BASE_PYTHON.parent
    for top in [base / "Lib", base / "DLLs"]:
        for path in top.rglob("*"):
            if path.is_file() and "site-packages" not in path.relative_to(base).parts:
                add(path, "python_runtime", str(path.relative_to(base)))
    for path in base.iterdir():
        if path.is_file() and path.suffix.lower() in {".exe", ".dll", ".zip", ".pth"}:
            add(path, "python_runtime", path.name)
    for name in ["harness.py", "PLAN.json", "DEPENDENCIES.lock.txt", "BUILD.lock.txt", "build-requirements.in"]:
        add(ROOT / name, "harness_or_dependency_specification", name)
    manifest = {"schema": "harness-input-manifest/1", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                "repo_url": plan["repo_url"], "commit_sha": plan["commit_sha"], "entrypoint": plan["analysis_entrypoint"],
                "entrypoint_sha256": sha(repo / "src/pingouin/parametric.py"),
                "command": command, "command_windows": subprocess.list2cmdline(command), "cwd": str(repo),
                "environment": env, "platform": platform.platform(), "python": sys.version,
                "inventory_rule": "All tracked upstream files; all files in the fresh venv; base Python stdlib excluding user site-packages, DLLs and interpreter binaries; harness and lock files. Sealed before starting the analysis process.",
                "audit_scope": "Python open audit events and imported module files, not an OS-kernel trace of native DLL/registry/font I/O.",
                "files": entries}
    write_json(run / "manifest.json", manifest)
    print(f"Sealed {run.name} manifest: {len(entries)} files. Starting one analysis invocation.", flush=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    start = time.perf_counter()
    result = subprocess.run(command, cwd=repo, env=env, capture_output=True)
    elapsed = time.perf_counter() - start
    (run / "stdout.txt").write_bytes(result.stdout)
    (run / "stderr.txt").write_bytes(result.stderr)
    paths = ["stdout.txt", "stderr.txt", "analysis.csv", "worker.json", "file-access.json"]
    artifacts = {name: {"sha256": sha(run / name), "bytes": (run / name).stat().st_size}
                 for name in paths if (run / name).is_file()}
    write_json(run / "result.json", {"started_utc": started, "command": command,
               "manifest_sha256": sha(run / "manifest.json"), "exit_code": result.returncode,
               "wall_seconds": elapsed, "artifacts": artifacts,
               "tracked_status_after": git(repo, "status", "--porcelain", "--untracked-files=no")})
    print(f"{run.name}: exit {result.returncode}, wall {elapsed:.6f}s", flush=True)
    print(result.stdout.decode("utf-8", "replace"), end="")
    if result.stderr:
        print(result.stderr.decode("utf-8", "replace"), file=sys.stderr, end="")


def worker(number):
    run = ROOT / f"run-{number}"
    repo = run / "repo"
    plan = json.loads((ROOT / "PLAN.json").read_text())
    manifest = json.loads((run / "manifest.json").read_text())
    opened, writes, connects = {}, set(), []
    active = True

    def audit(event, args):
        if not active:
            return
        if event == "open" and isinstance(args[0], (str, bytes)):
            path = str(Path(os.fsdecode(args[0])).resolve())
            flags = args[2] or 0
            mode = args[1] or ""
            writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)) or any(c in mode for c in "wax+")
            reading = not (flags & os.O_WRONLY) or "+" in mode
            if reading:
                opened.setdefault(path, {"read_before_write": path not in writes})
            if writing:
                writes.add(path)
        elif event == "socket.connect":
            connects.append(repr(args[1]))

    sys.addaudithook(audit)
    error = None
    module_path = None
    try:
        # README examples share this import from the preceding quick-start examples.
        import pingouin as pg
        module_path = pg.__file__
        namespace = {"pg": pg}
        code = example((repo / "README.rst").read_text())
        assert code == plan["readme_code"]
        exec(compile(code, "README.rst::one-way-ANOVA-example", "exec"), namespace)
        namespace["aov"].to_csv(run / "analysis.csv", index=False, lineterminator="\n")
    except BaseException:
        error = traceback.format_exc()
        raise
    finally:
        active = False
        access = []
        for name, event in sorted(opened.items()):
            path = Path(name)
            if not path.is_file():
                continue
            previous = manifest["files"].get(name)
            access.append({"path": name, **event, "presealed": previous is not None,
                           "generated_during_run": not event["read_before_write"],
                           "sha256_after": sha(path), "sha256_before": previous["sha256"] if previous else None})
        imported = sorted({str(Path(m.__file__).resolve()) for m in list(sys.modules.values())
                           if getattr(m, "__file__", None) and Path(m.__file__).is_file()})
        unsealed = [r for r in access if not r["presealed"] and r["read_before_write"]]
        changed = [r for r in access if r["presealed"] and r["sha256_before"] != r["sha256_after"]]
        write_json(run / "file-access.json", {"read_files": access, "writes": sorted(writes),
                    "network_connections": connects, "imported_module_files": imported,
                    "unsealed_existing_read_files": unsealed, "changed_presealed_inputs": changed})
        write_json(run / "worker.json", {"error": error, "pingouin_import_path": module_path,
                    "python_executable": sys.executable, "sys_path": sys.path,
                    "readme_block_executed_verbatim": error is None,
                    "existing_read_files_not_presealed": len(unsealed),
                    "changed_presealed_inputs": len(changed)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "execute", "worker"])
    parser.add_argument("number", type=int, choices=[1, 2])
    args = parser.parse_args()
    {"prepare": prepare, "execute": execute, "worker": worker}[args.action](args.number)
