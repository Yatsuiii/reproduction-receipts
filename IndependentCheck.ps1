param(
    [Parameter(Mandatory=$true)][string]$Scratch
)
$ErrorActionPreference = 'Stop'
$bundleRoot = $PSScriptRoot
$evidence = Join-Path $bundleRoot 'pingouin'
if (Test-Path -LiteralPath $Scratch) { throw 'Scratch path already exists; choose a new directory.' }
New-Item -ItemType Directory -Path $Scratch | Out-Null
$repo = Join-Path $Scratch 'upstream'
$venv = Join-Path $Scratch 'env'
$python = Join-Path $venv 'Scripts\python.exe'
$expectedCommit = '1ffb923219c636a396c3f749eac7092b00e80e8d'
$expectedCsv = 'bb7b390027087569e4baa58ab9664fa739aaad9f5e62f41258dcd49ea7bfe0a0'

git -c core.autocrlf=false clone https://github.com/raphaelvallat/pingouin.git $repo
if ($LASTEXITCODE -ne 0) { throw 'Clone failed' }
git -C $repo checkout --detach $expectedCommit
if ($LASTEXITCODE -ne 0) { throw 'Checkout failed' }
$actualCommit = git -C $repo rev-parse HEAD
if ($actualCommit.Trim() -ne $expectedCommit) { throw 'Unexpected upstream commit' }

uv venv --python 3.12.10 $venv
if ($LASTEXITCODE -ne 0) { throw 'Environment creation failed' }
uv pip sync --python $python --require-hashes (Join-Path $evidence 'DEPENDENCIES.lock.txt') (Join-Path $evidence 'BUILD.lock.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
Push-Location $repo
try {
    uv pip install --python $python --no-deps --no-build-isolation .
    if ($LASTEXITCODE -ne 0) { throw 'Upstream package installation failed' }
} finally { Pop-Location }

$entry = Join-Path $repo 'src\pingouin\parametric.py'
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $entry).Hash.ToLowerInvariant() -ne 'c828a3a8cd390ba6c1eb4d98f509a879b440ba047d5a02d36a94be9d1f8e4202') {
    throw 'Upstream analysis file hash differs'
}
# This invokes only the upstream package. It never imports harness.py or verify.py.
# The computation and arguments are the README's section-5 example; the final call serializes its returned table.
$analysis = "import pingouin as pg; df = pg.read_dataset('mixed_anova'); aov = pg.anova(data=df, dv='Scores', between='Group', detailed=True); print(aov); aov.to_csv('independent-analysis.csv', index=False, lineterminator='\n')"
Push-Location $Scratch
try {
    & $python -I -B -c $analysis
    if ($LASTEXITCODE -ne 0) { throw 'Upstream analysis failed; no repair or retry performed' }
} finally { Pop-Location }
$csv = Join-Path $Scratch 'independent-analysis.csv'
$actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $csv).Hash.ToLowerInvariant()
Write-Output "Upstream commit: $actualCommit"
Write-Output "CSV SHA256: $actualHash"
if ($actualHash -ne $expectedCsv) { throw "CSV differs. Preserve it at $csv; do not normalize it to obtain a match." }
$changed = git -C $repo status --porcelain --untracked-files=all
if ($changed) { throw 'Upstream checkout changed' }
Write-Output 'Independent byte match. Upstream checkout remains clean.'
