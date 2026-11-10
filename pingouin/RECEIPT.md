# Verification receipt

**Outcome: PASS for this README example and observed Python input coverage.**

## Repository and claim

- Repository: https://github.com/raphaelvallat/pingouin.git
- Exact commit: `1ffb923219c636a396c3f749eac7092b00e80e8d`.
- [Stated result](https://github.com/raphaelvallat/pingouin/blob/1ffb923219c636a396c3f749eac7092b00e80e8d/README.rst): section 5, one-way ANOVA on the committed `mixed_anova` dataset: Group F = **5.244**, p = **0.023**, DF = **1, 178**, partial eta-squared = **0.029** (README precision).
- Entry point: [`src/pingouin/parametric.py::anova`](https://github.com/raphaelvallat/pingouin/blob/1ffb923219c636a396c3f749eac7092b00e80e8d/src/pingouin/parametric.py#L812).
- Entry-point file SHA-256: `c828a3a8cd390ba6c1eb4d98f509a879b440ba047d5a02d36a94be9d1f8e4202`.
- Data: `src/pingouin/datasets/mixed_anova.csv`; its loader also reads `src/pingouin/datasets/datasets.csv`.
- Repository license: GPL-3.0-only. No trained model, model weights, TRIBE or Meta package was used.

## What was executed

The harness imported the package from each fresh virtual environment, then extracted and executed the README's section-5 Python block verbatim. The preceding README examples supply `import pingouin as pg`; the harness supplied that same import. The upstream function, loader, dataset and parameters were unchanged.

```python
import pingouin as pg
# Read an example dataset
df = pg.read_dataset('mixed_anova')

# Run the ANOVA
aov = pg.anova(data=df, dv='Scores', between='Group', detailed=True)
print(aov)
```

The harness saved the returned dataframe as `analysis.csv` with `index=False` and LF endings. That serialization is the harness's output adapter; the README itself prints the dataframe and does not supply a CSV artifact or reference artifact hash.

Both clones were initially clean and checked out at the same SHA. `git -c core.autocrlf=false clone` preserved committed line endings. No upstream tracked file changed, no bug was repaired, and neither clone was committed or pushed.

## Dependencies and environment

Two separate fresh `uv venv` environments used Python 3.12.10 on Windows. Runtime requirements came only from upstream `pyproject.toml`; build requirements came only from its `[build-system]` declaration. The upstream declares minimum versions rather than a lock. The harness resolved them once into hashed `DEPENDENCIES.lock.txt` and `BUILD.lock.txt`, synchronized both fresh environments with `--require-hashes`, and installed each local checkout using `--no-deps --no-build-isolation`.

`-I -B` isolated Python from user-site packages/PYTHONPATH and prevented bytecode writes during analysis. HOME, profile, app-data, temp and Matplotlib cache directories were empty, separate directories per run. No packages were imported from StillHere's environment or source tree. Setup commands, their stdout/stderr, exit codes and wall times are in each run's `setup.json` and `setup-*.txt` files. Isolation here means separate working directories and virtual environments, not a container or VM security sandbox.

Installed package versions (the sole location-dependent Pingouin URL is normalized here):

```text
cloudpickle==3.1.2
contourpy==1.4.0
cycler==0.12.1
fonttools==4.68.0
joblib==1.6.0
kiwisolver==1.5.1
matplotlib==3.11.2
narwhals==2.28.0
numpy==2.5.4
packaging==26.3
pandas==3.1.1
pillow==13.0.0
pingouin @ <this run's pinned checkout>
pyparsing==3.3.3
python-dateutil==4.0.0
scikit-learn==1.9.1
scipy==1.18.1
seaborn==0.13.2
setuptools==84.2.1
tabulate==0.10.0
threadpoolctl==3.8.0
tzdata==2026.6
wheel==0.48.0
```

## Runs and output

| Run | Analysis exit code | Wall time (seconds) | Scientific CSV SHA-256 |
|---|---:|---:|---|
| 1 | 0 | 10.618728 | `bb7b390027087569e4baa58ab9664fa739aaad9f5e62f41258dcd49ea7bfe0a0` |
| 2 | 0 | 10.566851 | `bb7b390027087569e4baa58ab9664fa739aaad9f5e62f41258dcd49ea7bfe0a0` |

Wall times include process startup, imports, the upstream analysis, serialization and audit-log writing; dependency installation and pre-run inventory hashing are excluded.

Exact commands, also stored in the manifests:

Run 1 (cwd `C:\Users\lenovo\harness-verification-20261110\run-1\repo`):

```powershell
C:\Users\lenovo\harness-verification-20261110\run-1\env\Scripts\python.exe -I -B C:\Users\lenovo\harness-verification-20261110\harness.py worker 1
```

Run 2 (cwd `C:\Users\lenovo\harness-verification-20261110\run-2\repo`):

```powershell
C:\Users\lenovo\harness-verification-20261110\run-2\env\Scripts\python.exe -I -B C:\Users\lenovo\harness-verification-20261110\harness.py worker 2
```

### README versus produced values

| Row / metric | README | Run 1 (unrounded) | Run 2 (unrounded) | At README precision |
|---|---:|---:|---:|---|
| Group / SS | 5.460 | 5.459963286855937 | 5.459963286855937 | match |
| Group / DF | 1 | 1 | 1 | match |
| Group / MS | 5.460 | 5.459963286855937 | 5.459963286855937 | match |
| Group / F | 5.244 | 5.243655749705594 | 5.243655749705594 | match |
| Group / p_unc | 0.023 | 0.023200326227690037 | 0.023200326227690037 | match |
| Group / np2 | 0.029 | 0.02861575604488026 | 0.02861575604488026 | match |
| Within / SS | 185.343 | 185.3427287088636 | 185.3427287088636 | match |
| Within / DF | 178 | 178 | 178 | match |
| Within / MS | 1.041 | 1.0412512848812563 | 1.0412512848812563 | match |
| Within / F | NaN | NaN / empty CSV field | NaN / empty CSV field | match |
| Within / p_unc | NaN | NaN / empty CSV field | NaN / empty CSV field | match |
| Within / np2 | NaN | NaN / empty CSV field | NaN / empty CSV field | match |

### Scientific input hashes

| Committed input | SHA-256 (both checkouts and installed copies) |
|---|---|
| `src/pingouin/datasets/datasets.csv` | `d75fb9e9e4274e91f1190a382287752f35055491df44acbf6ec8f5e14314113c` |
| `src/pingouin/datasets/mixed_anova.csv` | `cfd3728ee86c48728f1f4a59bebc79aa8f6e34e9ee12b9113832ef20d1221b61` |

## Repeatability and deviations

- The two raw scientific CSV files are byte-for-byte identical. No numerical normalization was used to obtain that match.
- All displayed README values match at its stated precision. Full-precision values are reported above, so README rounding is explicit.
- `stdout.txt` matches byte-for-byte.
- `stderr.txt` matches byte-for-byte.
- Missing numeric values printed as NaN are empty fields in the harness CSV; this is pandas CSV serialization, not a changed result.
- Run metadata/audit files differ because each checkout/environment has a distinct path. The first differing byte and context for every compared metadata file are in `comparison.json`.
- The presealed Python/environment inventories differ at 157 logical file paths; every path and both hashes are listed in `comparison.json`. Package versions and all 118 tracked upstream files match. These installation/runtime differences are not hidden by the scientific-artifact comparison.
- This runs one library README example on a bundled demonstration dataset. It does not reproduce a neuroimaging paper, establish cross-platform reproducibility, or validate an entire repository.

## Input hashing and observation boundary

Before each analysis subprocess, `manifest.json` sealed SHA-256 and byte length for every tracked upstream file, every fresh-environment file, base Python stdlib/runtime files, the harness, plan and dependency locks. This is a conservative superset of analysis inputs. Installed entry-point and dataset bytes were checked against the committed source copies before either run.

| Run | Presealed files | Observed Python file reads | Existing observed reads absent from manifest | Changed presealed reads | Network connections observed |
|---|---:|---:|---:|---:|---:|
| 1 | 10876 | 926 | 0 | 0 | 0 |
| 2 | 10876 | 926 | 0 | 0 | 0 |

The Python audit hook observes `open` events after bootstrap and imported-module paths. Files generated and reread during imports (for example a new Matplotlib cache) are identified as generated outputs in `file-access.json`, not silently treated as preexisting inputs. The manifest/plan and harness are recorded explicitly even though they are loaded before the hook.

**Coverage limitation:** this is not a kernel-level filesystem/network trace. Native library reads, operating-system DLL loads, registry access and accesses before Python instrumentation may not emit Python audit events. The receipt therefore verifies all explicit scientific data inputs and all observed Python reads; it does not certify that every OS-level read was traced. No claim of complete native-I/O coverage is made.

## Evidence files

- `PLAN.json`: analysis, expected README values and comparison policy written before either analysis run.
- `CLONE.json`, `run-*/checkout.json`: upstream origin, SHA and initial clean state.
- `run-*/manifest.json`: pre-run hashes, exact command, cwd and isolated environment variables.
- `run-*/stdout.txt`, `stderr.txt`, `result.json`: captured output, exit code, measured time and artifact hashes.
- `run-*/analysis.csv`: raw returned scientific table.
- `run-*/file-access.json`, `worker.json`: runtime file observations, package import location and coverage findings.
- `DEPENDENCIES.lock.txt`, `BUILD.lock.txt`, `run-*/environment.freeze.txt`: actual dependency selection.
- `comparison.json`: all metric comparisons, artifact hashes/byte differences, and environment-inventory differences.
- `harness.py`: the external wrapper; `verify.py`: this receipt generator. Neither file resides in or modifies the upstream clone.
- `ARTIFACTS.sha256`: integrity index for the plan, harness, locks, receipt, manifests, results and setup logs.
