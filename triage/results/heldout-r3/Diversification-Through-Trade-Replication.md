# Triage verdict: BLOCKED

- Package: `https://github.com/korenmiklos/Diversification-Through-Trade-Replication` at commit `5e286506a97fbf60c344879110fb7c38efb0b8fc`
- Triaged: 2026-11-21T12:12:21Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.598 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 1 blockers, 6 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `$sigma/results.jld2` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `experiments/CES/scenario.jl:18`, `save.jl:4`

## Deviations a rerun would have to log

- **PYTHON2_SYNTAX**: 5 Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 interpreter (end of life since 2020) or a port, and either is a logged deviation.
  Evidence: `notebooks/Admissible EOS.ipynb`, `notebooks/Compare S100 to S500.ipynb`, `notebooks/Compare scenarios.ipynb`, `notebooks/Create Figure 2.ipynb`, `notebooks/Volatility by decade.ipynb`
- **NO_DEPENDENCY_SPEC**: Python code imports GR but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `notebooks/Admissible EOS.ipynb`, `notebooks/Compare S100 to S500.ipynb`, `notebooks/Compare scenarios.ipynb`, `notebooks/Create Figure 2.ipynb`, `notebooks/Volatility by decade.ipynb`
- **NO_DEPENDENCY_SPEC**: Julia code without a Manifest.toml: package versions are not pinned.
  Evidence: `calibrate_params.jl`, `calibration_utils.jl`, `equilibrium.jl`, `experiments/CES/init_parameters.jl`, `experiments/CES/scenario.jl`
- **MISSING_INPUT_SOURCE_LISTED**: `$sigma/common_parameters.jld2` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (README.md: 15 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `experiments/CES/init_parameters.jl:26`, `experiments/CES0.5/actual/scenario.jl:7`, `experiments/CES0.5/init_parameters.jl:21`, `experiments/CES0.5/kappa1972/scenario.jl:7`, `experiments/CES0.5/nosectoral/scenario.jl:7`
- **ABSOLUTE_PATH**: 2 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `notebooks/aws-julia.sh:6`, `notebooks/aws-julia.sh:7`
- **LONG_COMPUTE**: The documentation claims a run time of about 27 hours, over this desk's budget of 24 hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.

## Notes

- **UNRESOLVED_PATHS**: 2 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `output.jl:94`, `output.jl:128`
- **LINK_UNREACHABLE**: 22 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `https://doi.org/10.1093/qje/qjz028`, `https://creativecommons.org/licenses/by/4.0/`, `http://www.euklems.net/`, `http://data.un.org/`, `https://stat.unido.org/content/dataset_description/indstat-2-2018%252c-isic-revision-3`, `http://databank.worldbank.org/data/download/WDI_csv.zip`, `https://datacatalog.worldbank.org/public-licenses#cc-by`, `https://comtrade.un.org/`, `https://comtrade.un.org/db/help/PolicyOnUseAndRedissemination.pdf`, `http://www.euklems.net/euk08i.shtml`

## What triage looked at

- 257 files, 89,011,321 bytes. Languages: julia (139), python (5), shell (4).
- Documentation read: LICENSE.md, README.md, notebooks/aws-recipe.md. Licences named: CC BY.
- Master scripts: Makefile.
- File reads traced: 301; writes: 4; unresolved paths: 2; missing: common_parameters.jld2, results.jld2.
- Links found: 23; checked: yes.
  - http://creativecommons.org/policies: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://data.un.org/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://data.un.org/Data.aspx?d=SNA&f=group_code%3a201: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://data.un.org/Handlers/DownloadHandler.ashx?DataFilter=group_code:201;fiscal_year:$year&DataMartId=SNA&Format=csv: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://databank.worldbank.org/data/download/WDI_csv.zip: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://databank.worldbank.org/data/download/archive/WDI_excel_2015_10.zip: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://wiki.creativecommons.org/Considerations_for_licensors_and_licensees#Considerations_for_licensees: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://wiki.creativecommons.org/Considerations_for_licensors_and_licensees#Considerations_for_licensors: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.euklems.net/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.euklems.net/euk08i.shtml: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://comtrade.un.org/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://comtrade.un.org/db/help/PolicyOnUseAndRedissemination.pdf: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://creativecommons.org/licenses/by/4.0/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://datacatalog.worldbank.org/public-licenses#cc-by: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://doi.org/10.1093/qje/qjz028: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://eu-central-1.console.aws.amazon.com/ec2/v2/home?region=eu-central-1#Instances:instanceId=i-0892e3c38c5d6f7d7;sort=instanceId: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://eu-central-1.console.aws.amazon.com/ec2/v2/home?region=eu-central-1#LaunchTemplates:sort=launchTemplateId|: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://julialang.org/research/julia-fresh-approach-BEKS.pdf: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://raw.githubusercontent.com/korenmiklos/impvol-julia/master/notebooks/aws-julia.sh: ok (200)
  - https://stat.unido.org/content/dataset_description/indstat-2-2018%252c-isic-revision-3: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.rug.nl/ggdc/docs/pwt71_11302012version.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt-7.1: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.unido.org/researchers/statistical-databases: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
