# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `pkgs/kelloggrk__Public_EndOfOil` at commit `b491fbac63c7387de74e1f3f89a279e556574e16`
- Triaged: 2026-11-21T18:16:57Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.071 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata
- 0 blockers, 3 deviations, 1 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Julia code without a Manifest.toml: package versions are not pinned.
  Evidence: `code/analysis/CustomEndOfOilModel.jl`, `code/analysis/EOOmodel.jl`, `code/analysis/EOOmodel_AKS.jl`, `code/analysis/PlotFunctions.jl`, `code/analysis/altcaseout.jl`
- **LFS_POINTERS**: 51 files are Git LFS pointers, not data. The data must be fetched with git lfs, which may need the host's quota or credentials.
  Evidence: `output/figures/AKSplot_agg.pdf`, `output/figures/AKSplot_region1.pdf`, `output/figures/AKSplot_region2.pdf`, `output/figures/AKSplot_region3.pdf`, `output/figures/AKSplot_region4.pdf`, `output/figures/ThyFigA.png`, `output/figures/ThyFigB.png`, `output/figures/comboplot_R.pdf`, `output/figures/comboplot_c0high.pdf`, `output/figures/comboplot_costR.pdf`
- **ABSOLUTE_PATH**: 3 code lines use absolute paths from the authors' machines. A rerun must edit them, and each edit is a logged deviation.
  Evidence: `EndOfOil_bash_file.sh:25`, `EndOfOil_bash_file.sh:26`, `code/analysis/intfilepath.jl:1`

## Notes

- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 351 files, 548,959 bytes. Languages: julia (18), shell (3).
- Documentation read: README.md. Licences named: none.
- Master scripts: none.
- File reads traced: 68; writes: 16; unresolved paths: 0; missing: none.
- Links found: 4; checked: no.
