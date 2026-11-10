# Check the result without the original harness

The checksum index is an integrity check, not independent attestation that the original runs happened. A matching checksum alone cannot establish that a scientific result is correct.

The check below clones the upstream repository again, checks out its recorded commit, installs its declared dependencies at the recorded versions, invokes its own ANOVA function, and hashes the resulting CSV with PowerShell's built-in `Get-FileHash`. It does not import or execute the original `harness.py` or `verify.py`.

## Inspect the scientific computation

Read the [upstream README, section 5](https://github.com/raphaelvallat/pingouin/blob/1ffb923219c636a396c3f749eac7092b00e80e8d/README.rst) and [the unmodified implementation](https://github.com/raphaelvallat/pingouin/blob/1ffb923219c636a396c3f749eac7092b00e80e8d/src/pingouin/parametric.py#L812).

The entire calculation is:

```python
import pingouin as pg
df = pg.read_dataset('mixed_anova')
aov = pg.anova(data=df, dv='Scores', between='Group', detailed=True)
print(aov)
```

The only output adapter is:

```python
aov.to_csv('independent-analysis.csv', index=False, lineterminator='\n')
```

Expected unrounded Group values: F = `5.243655749705594`, p = `0.023200326227690037`. The README displays `5.244` and `0.023`.

## Reproduce with standard commands

Prerequisites: Windows, Git, Python 3.12.10, and uv (the recorded runs used uv 0.12.24). Choose an unused scratch directory. None of these commands calls the original harness.

Run from this bundle's root; replace the scratch path as needed:

```powershell
$scratch = 'C:\Temp\pingouin-independent-check'
New-Item -ItemType Directory -Path $scratch
git -c core.autocrlf=false clone https://github.com/raphaelvallat/pingouin.git "$scratch\upstream"
git -C "$scratch\upstream" checkout --detach 1ffb923219c636a396c3f749eac7092b00e80e8d
uv venv --python 3.12.10 "$scratch\env"
uv pip sync --python "$scratch\env\Scripts\python.exe" --require-hashes .\pingouin\DEPENDENCIES.lock.txt .\pingouin\BUILD.lock.txt
Push-Location "$scratch\upstream"
uv pip install --python "$scratch\env\Scripts\python.exe" --no-deps --no-build-isolation .
Pop-Location
Push-Location $scratch
& "$scratch\env\Scripts\python.exe" -I -B -c "import pingouin as pg; df=pg.read_dataset('mixed_anova'); aov=pg.anova(data=df,dv='Scores',between='Group',detailed=True); print(aov); aov.to_csv('independent-analysis.csv',index=False,lineterminator='\n')"
Get-FileHash -Algorithm SHA256 .\independent-analysis.csv
Pop-Location
```

Check each command's exit code before continuing. A fail-fast form of those same commands is [`IndependentCheck.ps1`](IndependentCheck.ps1):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\IndependentCheck.ps1 -Scratch 'C:\Temp\pingouin-independent-check'
```

That process-level PowerShell policy flag runs this inspectable local script; it does not change a persisted execution policy. The manual commands above avoid the script entirely.

The expected CSV SHA-256 is:

```text
bb7b390027087569e4baa58ab9664fa739aaad9f5e62f41258dcd49ea7bfe0a0
```

To verify the supplied original CSV without running any custom verification code:

```powershell
Get-FileHash -Algorithm SHA256 .\pingouin\run-1\analysis.csv
Get-FileHash -Algorithm SHA256 .\pingouin\run-2\analysis.csv
```

Same-platform byte identity is the recorded claim. Different Python/package/OS versions may produce different bytes. Preserve and report differences rather than rounding or normalizing them away. A failed install is an environment failure, not evidence that the paper or statistic is false.

## Public automation

The included GitHub Actions workflow runs `IndependentCheck.ps1` on a fresh Windows runner and uploads the resulting CSV. It never calls the original harness. Its result is **not yet available**: the bundle has not been published and no public CI execution has been requested. A successful local independent check is still execution on the original operator's machine; public CI would supply a separate machine and a publicly inspectable log.
