# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pk/thimodeschouwer_replication-meaningflexibilitypuzzle` at commit `a65a0e7fa4274f15551ebdfb0350c0ed2878c253`
- Triaged: 2026-11-23T17:48:02Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.065 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 0 blockers, 6 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **UNDECLARED_DEPENDENCIES**: R code loads libpath, project, version, which code/renv.lock does not pin.
  Evidence: `code/renv.lock`
- **MISSING_INPUT_SOURCE_LISTED**: `data/raw/liss/background_202106.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (readme.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `code/functions/1_Clean_LISS.R:26`
- **MISSING_INPUT_SOURCE_LISTED**: `data/raw/issp/ISSP_2015.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (readme.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `code/appendix.R:56`, `code/main.R:52`
- **MISSING_INPUT_SOURCE_LISTED**: `data/raw/liss/L_HCE_5p.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (readme.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `code/appendix.R:57`, `code/main.R:53`
- **MISSING_INPUT_SOURCE_LISTED**: `data/raw/liss/work_2021.dta` is read by the code but is not in the package. The documentation does not name the file but lists external data sources (readme.md: 2 links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source accounts for would make this blocked.
  Evidence: `code/functions/1_Clean_LISS.R:30`
- **ABSOLUTE_PATH**: 2 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `code/appendix.R:13`, `code/main.R:14`

## Notes

- **SYSTEM_FILE_READS**: Code reads system files (/etc/redhat-release), usually to detect the operating system. Not package inputs; a rerun on another OS may take a different branch.
  Evidence: `code/renv/activate.R:850`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 53 files, 9,743,540 bytes. Languages: r (12).
- Documentation read: readme.md. Licences named: none.
- Master scripts: code/functions/0_Utilities.R, code/main.R.
- File reads traced: 21; writes: 76; unresolved paths: 0; missing: background_202106.dta, issp_2015.dta, l_hce_5p.dta, work_2021.dta.
- Links found: 5; checked: no.
