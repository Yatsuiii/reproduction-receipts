# Triage verdict: RUNNABLE WITH DEVIATIONS

- Package: `https://github.com/AlexandreAbraham/frontiers2013` at commit `97bf25836804195401ef213f963135957b431d70`
- Triaged: 2026-11-21T10:22:57Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.502 s of analysis
- Triage script: `triage.py` SHA-256 `42fe3acc44ecb384ba61c190862dd5f58ac33d0d2e15650289c1fc23359b63f6`; options: --check-links
- 0 blockers, 4 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Deviations a rerun would have to log

- **NO_DEPENDENCY_SPEC**: Python code imports distutils, lxml, matplotlib, nibabel, nilearn, numpy, pylab, scipy, sklearn but the package has no requirements file, environment file or lockfile. A rerun must choose versions and log them.
  Evidence: `scripts/adhd_clustering.py`, `scripts/adhd_ica.py`, `scripts/haxby_decoding.py`, `scripts/miyawaki_decoding.py`, `scripts/miyawaki_encoding.py`
- **REMOVED_API**: Code uses APIs that current releases no longer have: NumPy scalar aliases (np.int, np.float, ...) (removed in NumPy 1.24); nibabel get_data() (removed in nibabel 5.0); nibabel get_affine() / get_header() (deprecated, removed in later nibabel); sklearn.cross_validation (removed in scikit-learn 0.20); sklearn.externals.joblib / six (removed in scikit-learn 0.23); sklearn.datasets.base (removed in scikit-learn 0.24); distutils (removed from the standard library in Python 3.12). Nothing pins versions old enough, so a rerun must either reconstruct an old environment or edit the code, and log which.
  Evidence: `scripts/adhd_clustering.py:33`, `scripts/haxby_decoding.py:21`, `scripts/haxby_decoding.py:25`, `scripts/haxby_decoding.py:152`, `scripts/miyawaki_decoding.py:47`, `scripts/miyawaki_decoding.py:54`, `scripts/miyawaki_encoding.py:40`, `scripts/utils/datasets.py:1252`, `scripts/utils/searchlight.py:288`, `scripts/utils/searchlight.py:305`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (fetch_adhd, fetch_haxby, fetch_haxby_simple, fetch_miyawaki2008, urlopen). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `scripts/adhd_clustering.py:27`, `scripts/adhd_ica.py:11`, `scripts/haxby_decoding.py:40`, `scripts/haxby_decoding.py:41`, `scripts/miyawaki_decoding.py:9`, `scripts/miyawaki_encoding.py:14`, `scripts/utils/datasets.py:335`
- **NO_RUN_ORDER**: 6 scripts, no master script, and the README does not name an order. A rerun must choose one and log it.
  Evidence: `scripts/adhd_clustering.py`, `scripts/adhd_ica.py`, `scripts/haxby_decoding.py`, `scripts/miyawaki_decoding.py`, `scripts/miyawaki_encoding.py`, `scripts/visualization_101.py`

## Notes

- **PRECOMPUTED_OUTPUTS**: Files the code both writes and reads are already in the package: miyawaki/lr_coef.npy, miyawaki/lr_scores.npy, miyawaki/svc_coef.npy, miyawaki/svc_scores.npy, miyawaki/svcl2_scores.npy. A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and a matching output hash alone does not show recomputation.
  Evidence: `miyawaki/lr_coef.npy`, `miyawaki/lr_scores.npy`, `miyawaki/svc_coef.npy`, `miyawaki/svc_scores.npy`, `miyawaki/svcl2_scores.npy`
- **LINK_UNREACHABLE**: 13 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `http://nilearn.github.io`, `http://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/`, `http://www.pymvpa.org/files/pymvpa_exampledata.tar.bz2`, `http://data.pymvpa.org/datasets/haxby2001/`, `http://www.nitrc.org/frs/download.php/1071/NYU_TRT_session1a.tar.gz`, `http://www.nitrc.org/frs/download.php/1072/NYU_TRT_session1b.tar.gz`, `http://www.nitrc.org/frs/download.php/1073/NYU_TRT_session2a.tar.gz`, `http://www.nitrc.org/frs/download.php/1074/NYU_TRT_session2b.tar.gz`, `http://www.nitrc.org/frs/download.php/1075/NYU_TRT_session3a.tar.gz`, `http://www.nitrc.org/frs/download.php/1076/NYU_TRT_session3b.tar.gz`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 129 files, 97,449,167 bytes. Languages: python (11).
- Documentation read: README.md, submission/README.md, submission_review/README.md, submission_review_2/README.md. Licences named: none.
- Master scripts: none.
- File reads traced: 5; writes: 46; unresolved paths: 0; missing: none.
- Links found: 13; checked: yes.
  - http://connectir.projects.nitrc.org: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://data.pymvpa.org/datasets/haxby2001/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://nilearn.github.io: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.nitrc.org/frs/download.php/1071/NYU_TRT_session1a.tar.gz: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.nitrc.org/frs/download.php/1072/NYU_TRT_session1b.tar.gz: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.nitrc.org/frs/download.php/1073/NYU_TRT_session2a.tar.gz: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.nitrc.org/frs/download.php/1074/NYU_TRT_session2b.tar.gz: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.nitrc.org/frs/download.php/1075/NYU_TRT_session3a.tar.gz: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.nitrc.org/frs/download.php/1076/NYU_TRT_session3b.tar.gz: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - http://www.pymvpa.org/files/pymvpa_exampledata.tar.bz2: FAILED (URLError: <urlopen error [Errno -2] Name or service not known>)
  - https://team.inria.fr/parietal/files/2013/05/MSDL_rois.zip: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.nitrc.org/frs/download.php: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
