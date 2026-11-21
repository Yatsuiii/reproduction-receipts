# Triage verdict: RUNNABLE

- Package: `https://github.com/xgabaixLab/Behavioral-New-Keynesian-Model-AER-2020` at commit `4ca774b68454c89621671ce84c59bb8a15e6f1a0`
- Triaged: 2026-11-21T12:11:19Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.291 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: --have matlab,stata --check-links
- 0 blockers, 0 deviations, 5 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Notes

- **SOFTWARE_REQUIRED**: Requires Matlab; the desk says it has it.
  Evidence: `Original AER Replication Dynare 4.5.3/main.m`, `Original AER Replication Dynare 4.5.3/mainBRNKAugmentedPermanentShock.m`, `Original AER Replication Dynare 4.5.3/mainBRNKAugmentedTemporaryShock.m`, `Original AER Replication Dynare 4.5.3/mainForwardGuidance.m`, `Original AER Replication Dynare 4.5.3/mainOptimalPolicy.m`
- **UNRESOLVED_PATHS**: 2 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `Original AER Replication Dynare 4.5.3/zlbCostResult.m:16`, `zlbCostResult.m:16`
- **LINK_UNREACHABLE**: 2 other links could not be reached from this machine (DNS, refused, timeout or proxy). That may be this machine's network rather than the link.
  Evidence: `https://www.aeaweb.org/articles?id=10.1257/aer.20162005`, `https://www.openicpsr.org/openicpsr/project/117842/version/V1/view`
- **SOFTWARE_REQUIRED**: Requires Dynare (free) inside MATLAB or Octave, version 4.5.3, 4.6.4 named in the documentation.
  Evidence: `Original AER Replication Dynare 4.5.3/brnkAugmentedPermanentShock.mod`, `Original AER Replication Dynare 4.5.3/brnkAugmentedTemporaryShock.mod`, `Original AER Replication Dynare 4.5.3/optPolCostpushBasic.mod`, `Original AER Replication Dynare 4.5.3/zlb.mod`, `Original AER Replication Dynare 4.5.3/zlbCost.mod`
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 49 files, 864,907 bytes. Languages: dynare (10), matlab (20).
- Documentation read: README.md. Licences named: none.
- Master scripts: Original AER Replication Dynare 4.5.3/main.m, main.m.
- File reads traced: 32; writes: 78; unresolved paths: 2; missing: none.
- Links found: 2; checked: yes.
  - https://www.aeaweb.org/articles?id=10.1257/aer.20162005: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
  - https://www.openicpsr.org/openicpsr/project/117842/version/V1/view: FAILED (URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>)
