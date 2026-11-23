# Triage verdict: BLOCKED

- Package: `pkgs/floswald__LandUse-REStud` at commit `5b7f48c533dff10d5658e842820332c5c3228542`
- Triaged: 2026-11-21T18:16:58Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.205 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 11 blockers, 7 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `baseline-aggregated.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/LandUse.jl/src/running.jl:670`
- **MISSING_INPUT_UNDOCUMENTED**: `cd2019-19_tableaux_VVT_mapping.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/LandUseR/R/petite-region-agricole.R:2693`
- **MISSING_INPUT_UNDOCUMENTED**: `d1d220.jld2` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/LandUse.jl/src/experiments.jl:549`
- **MISSING_INPUT_UNDOCUMENTED**: `d1d2detail.csv` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/LandUse.jl/src/plotly.jl:7`
- **MISSING_INPUT_UNDOCUMENTED**: `../data/raw/FRA_base.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/stata/figure1.do:2`, `code/stata/generatethetas.do:3`
- **MISSING_INPUT_UNDOCUMENTED**: `../data/raw/historicalcommute_paris.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/stata/commutingparis.do:4`
- **MISSING_INPUT_UNDOCUMENTED**: `../out/multistarts.bson` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/LandUse.jl/src/running.jl:1311`
- **MISSING_INPUT_UNDOCUMENTED**: `../data/raw/NPLH_FRA.dta` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/stata/figure6.do:30`
- **MISSING_INPUT_UNDOCUMENTED**: `../data/raw/PikettyZucman.xls` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/stata/figure6.do:4`
- **MISSING_INPUT_UNDOCUMENTED**: `Referentiel_CommuneRA_PRA_2017_mapping.xls` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/LandUseR/R/petite-region-agricole.R:2687`
- **MISSING_INPUT_UNDOCUMENTED**: `../data/raw/spending_shares.xlsx` is read by the code but is not in the package, and the documentation does not say where it comes from.
  Evidence: `code/stata/figureA5.do:3`

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **UNDECLARED_DEPENDENCIES**: R code loads LandUseR, grateful, libpath, project, usethis, version, which code/LandUseR/renv.lock does not pin.
  Evidence: `code/LandUseR/renv.lock`
- **RUNTIME_DOWNLOAD**: Code downloads https://www.statistiques.developpement-durable.gouv.fr/sites/default/files/2018-12/Q_tcm_menage_0.csv at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `code/LandUseR/R/ENTD.R:12`
- **RUNTIME_DOWNLOAD**: Code downloads https://www.statistiques.developpement-durable.gouv.fr/sites/default/files/2019-01/Q_tcm_individu.csv at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `code/LandUseR/R/ENTD.R:13`
- **RUNTIME_DOWNLOAD**: Code downloads https://www.statistiques.developpement-durable.gouv.fr/sites/default/files/2019-01/Q_ind_lieu_teg.csv at run time. The content may have changed since publication; a receipt must record its SHA-256 (link not checked).
  Evidence: `code/LandUseR/R/ENTD.R:14`
- **ABSOLUTE_PATH**: 5 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `.devcontainer/validate-setup.sh:10`, `README.qmd:377`, `README.qmd:890`, `README.qmd:934`, `package.sh:4`
- **GPU_REQUIRED**: The package refers to GPUs or CUDA. A CPU rerun may be slower or numerically different and must say so.

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `code/stata/commutingparis.do`, `code/stata/figure1.do`, `code/stata/figure6.do`, `code/stata/figureA5.do`, `code/stata/generatethetas.do`
- **ENVIRONMENT_IMAGE**: The package ships a container definition. A rerun can build it, but image tags and base images must be pinned by digest to be reproducible.
  Evidence: `.devcontainer/Dockerfile`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: data-moments.csv, population.csv. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `data-moments.csv`, `population.csv`
- **SYSTEM_FILE_READS**: Code reads system files (/etc/redhat-release), usually to detect the operating system. Not package inputs; a rerun on another OS may take a different branch.
  Evidence: `code/LandUseR/renv/activate.R:850`
- **UNRESOLVED_PATHS**: 1 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/LandUse.jl/src/experiments.jl:613`

## What triage looked at

- 228 files, 1,580,728 bytes. Languages: julia (52), r (25), shell (5), stata (7).
- Documentation read: README.md. Licences named: CC BY, CC0.
- Master scripts: code/LandUse.jl/run.jl, code/run_all.sh.
- File reads traced: 76; writes: 90; unresolved paths: 1; missing: baseline-aggregated.csv, cd2019-19_tableaux_vvt_mapping.xlsx, d1d220.jld2, d1d2detail.csv, fra_base.dta, historicalcommute_paris.xlsx, multistarts.bson, nplh_fra.dta, pikettyzucman.xls, referentiel_communera_pra_2017_mapping.xls, spending_shares.xlsx.
- Links found: 11; checked: no.
