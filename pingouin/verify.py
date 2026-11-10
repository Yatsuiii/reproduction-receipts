"""Compare the two saved runs and write the receipt. Does not execute the analysis."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def main():
    plan = load(ROOT / "PLAN.json")
    runs = []
    for n in (1, 2):
        folder = ROOT / f"run-{n}"
        result = load(folder / "result.json")
        manifest = load(folder / "manifest.json")
        assert digest(folder / "manifest.json") == result["manifest_sha256"], "Manifest changed after execution"
        assert manifest["commit_sha"] == plan["commit_sha"]
        assert not result["tracked_status_after"], "Upstream tracked files were changed"
        for name, artifact in result["artifacts"].items():
            assert digest(folder / name) == artifact["sha256"], f"Recorded output changed: {n}/{name}"
        access = load(folder / "file-access.json")
        runs.append({"folder": folder, "result": result, "manifest": manifest, "access": access})
    comparisons = []
    for r in runs:
        path = r["folder"] / "analysis.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8", newline=""))) if path.exists() else []
        checks = []
        for expected in plan["expected_readme_rows"]:
            row = next((x for x in rows if x["Source"] == expected["Source"]), None)
            for key, stated in expected.items():
                if key == "Source":
                    continue
                raw = row.get(key) if row else None
                if row is None:
                    matched = False
                elif stated is None:
                    matched = raw in ("", "nan", "NaN")
                elif key == "DF":
                    matched = float(raw) == stated
                else:
                    matched = f"{float(raw):.3f}" == f"{stated:.3f}"
                checks.append({"row": expected["Source"], "column": key,
                               "stated": stated, "produced": raw, "matches_readme_precision": matched})
        comparisons.append(checks)
    artifact_checks = {}
    for name in ["analysis.csv", "stdout.txt", "stderr.txt", "worker.json", "file-access.json"]:
        paths = [r["folder"] / name for r in runs]
        if all(p.is_file() for p in paths):
            first, second = [p.read_bytes() for p in paths]
            difference = None
            if first != second:
                offset = next((i for i, (a, b) in enumerate(zip(first, second)) if a != b), min(len(first), len(second)))
                difference = {"first_differing_byte_zero_based": offset,
                              "context_run_1": first[max(0, offset-45):offset+80].decode("utf-8", "replace"),
                              "context_run_2": second[max(0, offset-45):offset+80].decode("utf-8", "replace")}
            artifact_checks[name] = {"sha256_run_1": digest(paths[0]), "sha256_run_2": digest(paths[1]),
                                    "bytes_match": first == second, "difference": difference}
        else:
            artifact_checks[name] = {"bytes_match": False, "missing": [str(p) for p in paths if not p.exists()]}
    upstream = [{v["logical_path"]: v["sha256"] for v in r["manifest"]["files"].values()
                 if v["role"] == "upstream_tracked_file"} for r in runs]
    assert upstream[0] == upstream[1], "Checkouts have different tracked source/input bytes"
    envs = [{(v["role"], v["logical_path"]): v["sha256"] for v in r["manifest"]["files"].values()
             if v["role"] in ("isolated_environment", "python_runtime")} for r in runs]
    env_diffs = [{"role": key[0], "logical_path": key[1], "sha256_run_1": envs[0].get(key),
                  "sha256_run_2": envs[1].get(key)}
                 for key in sorted(set(envs[0]) | set(envs[1])) if envs[0].get(key) != envs[1].get(key)]
    versions = [re.sub(r"pingouin @ file://[^\r\n]+", "pingouin @ <this run's pinned checkout>",
                       (r["folder"] / "environment.freeze.txt").read_text()) for r in runs]
    assert versions[0] == versions[1], "Installed package versions differ"
    coverage_ok = all(not r["access"]["unsealed_existing_read_files"]
                      and not r["access"]["changed_presealed_inputs"]
                      and not r["access"]["network_connections"] for r in runs)
    readme_ok = all(all(c["matches_readme_precision"] for c in checks) for checks in comparisons)
    outcome = (all(r["result"]["exit_code"] == 0 for r in runs)
               and artifact_checks["analysis.csv"]["bytes_match"] and coverage_ok and readme_ok)
    summary = {"success": outcome, "scientific_artifact": artifact_checks["analysis.csv"],
               "readme_comparisons": comparisons, "artifact_comparisons": artifact_checks,
               "identical_tracked_upstream_files": len(upstream[0]), "package_versions_match": True,
               "presealed_environment_byte_differences": env_diffs,
               "python_visible_input_coverage_ok": coverage_ok,
               "scope": "One README ANOVA example, same Windows/Python platform, independent clones and virtual environments; not an operating-system-level I/O audit or a scientific study replication."}
    save(ROOT / "comparison.json", summary)
    sha = plan["commit_sha"]
    base_url = f"https://github.com/raphaelvallat/pingouin/blob/{sha}"
    lines = ["# Verification receipt", "", f"**Outcome: {'PASS for this README example and observed Python input coverage' if outcome else 'FAIL / DEVIATION RECORDED'}.**",
             "", "## Repository and claim", "", f"- Repository: {plan['repo_url']}",
             f"- Exact commit: `{sha}`.",
             f"- [Stated result]({base_url}/README.rst): section 5, one-way ANOVA on the committed `mixed_anova` dataset: Group F = **5.244**, p = **0.023**, DF = **1, 178**, partial eta-squared = **0.029** (README precision).",
             f"- Entry point: [`src/pingouin/parametric.py::anova`]({base_url}/src/pingouin/parametric.py#L812).",
             f"- Entry-point file SHA-256: `{runs[0]['manifest']['entrypoint_sha256']}`.",
             "- Data: `src/pingouin/datasets/mixed_anova.csv`; its loader also reads `src/pingouin/datasets/datasets.csv`.",
             "- Repository license: GPL-3.0-only. No trained model, model weights, TRIBE or Meta package was used.",
             "", "## What was executed", "",
             "The harness imported the package from each fresh virtual environment, then extracted and executed the README's section-5 Python block verbatim. The preceding README examples supply `import pingouin as pg`; the harness supplied that same import. The upstream function, loader, dataset and parameters were unchanged.",
             "", "```python", "import pingouin as pg", plan["readme_code"].rstrip(), "```", "",
             "The harness saved the returned dataframe as `analysis.csv` with `index=False` and LF endings. That serialization is the harness's output adapter; the README itself prints the dataframe and does not supply a CSV artifact or reference artifact hash.",
             "", "Both clones were initially clean and checked out at the same SHA. `git -c core.autocrlf=false clone` preserved committed line endings. No upstream tracked file changed, no bug was repaired, and neither clone was committed or pushed.",
             "", "## Dependencies and environment", "",
             "Two separate fresh `uv venv` environments used Python 3.12.10 on Windows. Runtime requirements came only from upstream `pyproject.toml`; build requirements came only from its `[build-system]` declaration. The upstream declares minimum versions rather than a lock. The harness resolved them once into hashed `DEPENDENCIES.lock.txt` and `BUILD.lock.txt`, synchronized both fresh environments with `--require-hashes`, and installed each local checkout using `--no-deps --no-build-isolation`.",
             "", "`-I -B` isolated Python from user-site packages/PYTHONPATH and prevented bytecode writes during analysis. HOME, profile, app-data, temp and Matplotlib cache directories were empty, separate directories per run. No packages were imported from StillHere's environment or source tree. Setup commands, their stdout/stderr, exit codes and wall times are in each run's `setup.json` and `setup-*.txt` files. Isolation here means separate working directories and virtual environments, not a container or VM security sandbox.",
             "", "Installed package versions (the sole location-dependent Pingouin URL is normalized here):", "", "```text", versions[0].strip(), "```", "",
             "## Runs and output", "", "| Run | Analysis exit code | Wall time (seconds) | Scientific CSV SHA-256 |", "|---|---:|---:|---|"]
    for n, r in enumerate(runs, 1):
        csv_hash = r["result"]["artifacts"].get("analysis.csv", {}).get("sha256", "MISSING")
        lines.append(f"| {n} | {r['result']['exit_code']} | {r['result']['wall_seconds']:.6f} | `{csv_hash}` |")
    lines += ["", "Wall times include process startup, imports, the upstream analysis, serialization and audit-log writing; dependency installation and pre-run inventory hashing are excluded.",
              "", "Exact commands, also stored in the manifests:", ""]
    for n, r in enumerate(runs, 1):
        lines += [f"Run {n} (cwd `{r['manifest']['cwd']}`):", "", "```powershell", r["manifest"]["command_windows"], "```", ""]
    lines += ["### README versus produced values", "", "| Row / metric | README | Run 1 (unrounded) | Run 2 (unrounded) | At README precision |", "|---|---:|---:|---:|---|"]
    for first, second in zip(*comparisons):
        stated = "NaN" if first["stated"] is None else (str(first["stated"]) if first["column"] == "DF" else f"{first['stated']:.3f}")
        produced = lambda c: c["produced"] if c["produced"] not in (None, "") else "NaN / empty CSV field"
        matched = first["matches_readme_precision"] and second["matches_readme_precision"]
        lines.append(f"| {first['row']} / {first['column']} | {stated} | {produced(first)} | {produced(second)} | {'match' if matched else 'DIFFERS'} |")
    lines += ["", "### Scientific input hashes", "", "| Committed input | SHA-256 (both checkouts and installed copies) |", "|---|---|"]
    for name in plan["scientific_data_inputs"]:
        value=upstream[0][name]
        for r in runs:
            installed=r["folder"] / "env/Lib/site-packages" / Path(name).relative_to("src")
            assert digest(installed)==value
            assert any(x["path"]==str(installed.resolve()) for x in r["access"]["read_files"])
        lines.append(f"| `{name}` | `{value}` |")
    lines += ["", "## Repeatability and deviations", ""]
    if artifact_checks["analysis.csv"]["bytes_match"]:
        lines.append("- The two raw scientific CSV files are byte-for-byte identical. No numerical normalization was used to obtain that match.")
    else:
        lines.append("- The scientific CSV files do not match (or are missing). Exact byte offsets and context are recorded in `comparison.json`.")
    lines.append(f"- All displayed README values {'match' if readme_ok else 'do not all match'} at its stated precision. Full-precision values are reported above, so README rounding is explicit.")
    for name in ["stdout.txt", "stderr.txt"]:
        lines.append(f"- `{name}` {'matches byte-for-byte' if artifact_checks[name]['bytes_match'] else 'differs; see exact first differing byte and context in comparison.json'}.")
    lines += ["- Missing numeric values printed as NaN are empty fields in the harness CSV; this is pandas CSV serialization, not a changed result.",
              "- Run metadata/audit files differ because each checkout/environment has a distinct path. The first differing byte and context for every compared metadata file are in `comparison.json`.",
              f"- The presealed Python/environment inventories differ at {len(env_diffs)} logical file paths; every path and both hashes are listed in `comparison.json`. Package versions and all {len(upstream[0])} tracked upstream files match. These installation/runtime differences are not hidden by the scientific-artifact comparison.",
              "- This runs one library README example on a bundled demonstration dataset. It does not reproduce a neuroimaging paper, establish cross-platform reproducibility, or validate an entire repository.",
              "", "## Input hashing and observation boundary", "",
              "Before each analysis subprocess, `manifest.json` sealed SHA-256 and byte length for every tracked upstream file, every fresh-environment file, base Python stdlib/runtime files, the harness, plan and dependency locks. This is a conservative superset of analysis inputs. Installed entry-point and dataset bytes were checked against the committed source copies before either run.",
              "", "| Run | Presealed files | Observed Python file reads | Existing observed reads absent from manifest | Changed presealed reads | Network connections observed |", "|---|---:|---:|---:|---:|---:|"]
    for n, r in enumerate(runs, 1):
        ac = r["access"]
        lines.append(f"| {n} | {len(r['manifest']['files'])} | {len(ac['read_files'])} | {len(ac['unsealed_existing_read_files'])} | {len(ac['changed_presealed_inputs'])} | {len(ac['network_connections'])} |")
    lines += ["", "The Python audit hook observes `open` events after bootstrap and imported-module paths. Files generated and reread during imports (for example a new Matplotlib cache) are identified as generated outputs in `file-access.json`, not silently treated as preexisting inputs. The manifest/plan and harness are recorded explicitly even though they are loaded before the hook.",
              "", "**Coverage limitation:** this is not a kernel-level filesystem/network trace. Native library reads, operating-system DLL loads, registry access and accesses before Python instrumentation may not emit Python audit events. The receipt therefore verifies all explicit scientific data inputs and all observed Python reads; it does not certify that every OS-level read was traced. No claim of complete native-I/O coverage is made.",
              "", "## Evidence files", "",
              "- `PLAN.json`: analysis, expected README values and comparison policy written before either analysis run.",
              "- `CLONE.json`, `run-*/checkout.json`: upstream origin, SHA and initial clean state.",
              "- `run-*/manifest.json`: pre-run hashes, exact command, cwd and isolated environment variables.",
              "- `run-*/stdout.txt`, `stderr.txt`, `result.json`: captured output, exit code, measured time and artifact hashes.",
              "- `run-*/analysis.csv`: raw returned scientific table.",
              "- `run-*/file-access.json`, `worker.json`: runtime file observations, package import location and coverage findings.",
              "- `DEPENDENCIES.lock.txt`, `BUILD.lock.txt`, `run-*/environment.freeze.txt`: actual dependency selection.",
              "- `comparison.json`: all metric comparisons, artifact hashes/byte differences, and environment-inventory differences.",
              "- `harness.py`: the external wrapper; `verify.py`: this receipt generator. Neither file resides in or modifies the upstream clone.",
              "- `ARTIFACTS.sha256`: integrity index for the plan, harness, locks, receipt, manifests, results and setup logs.", ""]
    (ROOT / "RECEIPT.md").write_text("\n".join(lines), encoding="utf-8")
    paths = [p for p in ROOT.iterdir() if p.is_file() and p.name != "ARTIFACTS.sha256"]
    for r in runs:
        paths.extend(p for p in r["folder"].iterdir() if p.is_file())
    index = "\n".join(f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in sorted(paths)) + "\n"
    (ROOT / "ARTIFACTS.sha256").write_text(index, encoding="utf-8")
    print(json.dumps({"success": outcome, "csv": artifact_checks["analysis.csv"],
                      "readme_values_match": readme_ok, "coverage_ok": coverage_ok,
                      "environment_file_differences": len(env_diffs), "receipt": str(ROOT / "RECEIPT.md")}, indent=2))


if __name__ == "__main__":
    main()
