# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `https://github.com/korenmiklos/Volatility-and-Development-replication` at commit `ea6fe0748160c7262d5ee038575370213284d303`
- Triaged: 2026-11-21T12:12:34Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.307 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 0 blockers, 2 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **STATA_VERSION_MISSING**: No `version` statement in any do-file. Stata's behaviour depends on the version, so a rerun must choose one and log it.
- **LFS_POINTERS**: 7 files are Git LFS pointers, not data. The data must be fetched with git lfs, which may need the host's quota or credentials.
  Evidence: `data/derived/Jt.dta`, `data/pwt/pwt1.dta`, `data/pwt/pwt_prices.dta`, `data/unido/unido-dollar.dta`, `data/wdi/wdiilo.dta`, `data/wdi/wdinew.dta`, `stanwdi.dta`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata; the desk says it has it.
  Evidence: `createallgraphs.do`, `data/wdi/wdisectors.do`, `drawgraphs.do`, `meanreturns.do`, `preparefactors.do`
- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: data/derived/allfactors.dta, data/derived/meanlaborprod_wide.dta, data/derived/preparedshares.dta, data/derived/shares.dta, data/derived/specmeasures.dta. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `data/derived/allfactors.dta`, `data/derived/meanlaborprod_wide.dta`, `data/derived/preparedshares.dta`, `data/derived/shares.dta`, `data/derived/specmeasures.dta`
- **UNRESOLVED_PATHS**: 5 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `data/wdi/wdisectors.do:46`, `preparefactors.do:27`, `preparefactors.do:38`, `preparefactors.do:45`, `specmeasures.do:93`
- **LINK_UNREACHABLE**: 8 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `https://opensource.org/licenses/BSD-3-Clause`, `https://opendatacommons.org/licenses/odbl/1-0/`, `https://stat.unido.org/content/legal/Terms%20and%20Conditions`, `https://data.worldbank.org/summary-terms-of-use`, `https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt-6.1`, `https://zenodo.org/record/1441497`, `http://stat.unido.org`, `http://datatopics.worldbank.org/world-development-indicators/`

## What triage looked at

- 47 files, 25,660,340 bytes. Languages: stata (7).
- Documentation read: README.md. Licences named: BSD, ODC.
- Master scripts: Makefile, data/wdi/Makefile.
- File reads traced: 23; writes: 13; unresolved paths: 5; missing: none.
- Links found: 8; checked: yes.
  - http://datatopics.worldbank.org/world-development-indicators/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://stat.unido.org: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://data.worldbank.org/summary-terms-of-use: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://opendatacommons.org/licenses/odbl/1-0/: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://opensource.org/licenses/BSD-3-Clause: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://stat.unido.org/content/legal/Terms%20and%20Conditions: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt-6.1: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://zenodo.org/record/1441497: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
