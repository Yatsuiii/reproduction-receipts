# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/DavBrg__Structural-Forecast-Analysis-Final` at commit `3c18528c0bedd75867a4bb7a6418640345c3261d`
- Triaged: 2026-11-21T18:16:37Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.065 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 2 deviations, 4 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `Applications/Save_lambdas.m:30`, `Applications/Save_lambdas.m:31`, `Applications/Save_lambdas.m:32`
- **NO_RUN_ORDER**: 72 scripts, no master script, and the README does not name an order. A rerun must choose one and log it.
  Evidence: `Applications/Main_RunAll.m`, `Applications/Part1_EstimateSVARs.m`, `Applications/Part2_RunStructuralForecastAnalysis.m`, `Applications/Part3_FiguresSVAR.m`, `Applications/Part4_FiguresStructuralForecastAnalysis.m`, `Applications/Part5_Assess_Datarev.m`, `Applications/Part6_CompareEstimates.m`, `Applications/Part7_FigureGDPRevisions.m`, `Applications/Part8_OrganizeFiguresPaperAppendix.m`, `Applications/Save_lambdas.m`

## Notes

- **README_NOT_TEXT**: The README is not plain text (README.docx, README.pdf). Triage cannot read it, so the data availability statement, licence and run time below were not checked against it. Read it by hand.
  Evidence: `README.docx`, `README.pdf`
- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `Applications/Main_RunAll.m`, `Applications/Part1_EstimateSVARs.m`, `Applications/Part2_RunStructuralForecastAnalysis.m`, `Applications/Part3_FiguresSVAR.m`, `Applications/Part4_FiguresStructuralForecastAnalysis.m`
- **UNRESOLVED_PATHS**: 12 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Applications/Part1_EstimateSVARs.m:72`, `Applications/Part2_RunStructuralForecastAnalysis.m:88`, `Applications/Part3_FiguresSVAR.m:36`, `Applications/Part4_FiguresStructuralForecastAnalysis.m:46`, `Applications/Part4_FiguresStructuralForecastAnalysis.m:182`, `Applications/Part5_Assess_Datarev.m:60`, `Applications/Part5_Assess_Datarev.m:62`, `Applications/Part6_CompareEstimates.m:23`, `Applications/Part6_CompareEstimates.m:96`, `Applications/Part6_CompareEstimates.m:121`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 78 files, 1,934,794 bytes. Languages: matlab (72).
- Documentation read: none. Licences named: none.
- Master scripts: none.
- File reads traced: 14; writes: 35; unresolved paths: 12; missing: none.
- Links found: 0; checked: no.
