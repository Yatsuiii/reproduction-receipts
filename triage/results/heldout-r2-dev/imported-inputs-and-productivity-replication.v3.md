# Triage verdict: BLOCKED

- Package: `https://github.com/korenmiklos/imported-inputs-and-productivity-replication` at commit `a24e5f08085af959275e36c3b5ba65836dd6e2bc`
- Triaged: 2026-11-21T12:11:23Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.378 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 2 blockers, 3 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_RESTRICTED**: `../doc/foreignpresence_tfp_gain.dta` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("confidential"), so it is most likely one of those.
  Evidence: `code/table9.do:36`
- **MISSING_INPUT_UNDOCUMENTED**: `../data/impmanuf.dta` is read by the code and named in the documentation (README.md), but it is not in the package and no source for it is given.
  Evidence: `code/decomposition.do:63`, `code/import_margins.do:20`, `code/import_margins.do:77`, `code/numbers-in-text.do:15`, `code/numbers-in-text.do:72`

## Deviations a rerun would have to log

- **PYTHON2_SYNTAX**: 2 Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 interpreter (end of life since 2020) or a port, and either is a logged deviation.
  Evidence: `code/filename_parser.py:23`, `code/write_results_to_excel.py:156`
- **NO_DEPENDENCY_SPEC**: Python code imports StringIO but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `code/filename_parser.py`, `code/write_results_to_excel.py`
- **STATA_NETWORK_INSTALL**: Do-files install graphexportpdf from the network at run time, with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.
  Evidence: `code/all_graphs.do:9`

## Notes

- **SOFTWARE_REQUIRED**: Requires Stata (version 10, 12, 9 named in code); the desk says it has it.
  Evidence: `code/all_graphs.do`, `code/collapse-and-draw-graph.do`, `code/counterfactual.do`, `code/csvmerge.ado`, `code/decomposition.do`
- **UNRESOLVED_PATHS**: 20 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/all_graphs.do:73`, `code/all_graphs.do:74`, `code/collapse-and-draw-graph.do:19`, `code/collapse-and-draw-graph.do:21`, `code/csvmerge.ado:8`, `code/csvmerge.ado:14`, `code/estimate_specification.do:28`, `code/estimate_specification.do:31`, `code/estimate_specification.do:48`, `code/import_margins.do:25`
- **LINK_UNREACHABLE**: 1 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `http://www.mtakti.hu/english/`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 9502 files, 87,733,828 bytes. Languages: python (2), stata (32).
- Documentation read: README.md. Licences named: none.
- Master scripts: code/Makefile.
- File reads traced: 58; writes: 27; unresolved paths: 20; missing: foreignpresence_tfp_gain.dta, impmanuf.dta.
- Links found: 1; checked: yes.
  - http://www.mtakti.hu/english/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
