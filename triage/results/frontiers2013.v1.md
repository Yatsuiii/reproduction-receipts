# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `https://github.com/AlexandreAbraham/frontiers2013` at commit `97bf25836804195401ef213f963135957b431d70`
- Triaged: 2026-11-21T10:21:04Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.068 s of analysis
- Triage script: `triage.py` SHA-256 `fedc562d7a1e1b45cb20e1200412b40d2cffd540fb63d6a8b303b59806bcbec2`; options: --check-links
- 0 blockers, 2 deviations, 2 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Python code imports distutils, lxml, matplotlib, nibabel, nilearn, numpy, pylab, scipy, sklearn but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `scripts/adhd_clustering.py`, `scripts/adhd_ica.py`, `scripts/haxby_decoding.py`, `scripts/miyawaki_decoding.py`, `scripts/miyawaki_encoding.py`
- **NO_RUN_ORDER**: 11 scripts, no master script, and the README does not name an order. A rerun must choose one and log it.
  Evidence: `scripts/adhd_clustering.py`, `scripts/adhd_ica.py`, `scripts/haxby_decoding.py`, `scripts/miyawaki_decoding.py`, `scripts/miyawaki_encoding.py`, `scripts/utils/datasets.py`, `scripts/utils/masking.py`, `scripts/utils/resampling.py`, `scripts/utils/searchlight.py`, `scripts/utils/signal.py`

## Notes

- **DEAD_LINK**: 1 other links in the documentation could not be fetched.
  Evidence: `http://nilearn.github.io`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 129 files, 97,449,167 bytes. Languages: python (11).
- Documentation read: README.md, submission/README.md, submission_review/README.md, submission_review_2/README.md. Licences named: none.
- Master scripts: none.
- File reads traced: 0; writes: 41; unresolved paths: 0; missing: none.
- Links found: 1; checked: yes.
  - http://nilearn.github.io: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
