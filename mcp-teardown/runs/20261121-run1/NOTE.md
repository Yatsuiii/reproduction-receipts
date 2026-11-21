# Run 1, 2026-11-21: invalidated by a runner bug, kept as a failed run

Armed correctly (negative probe empty, leaky control CONFIRMED, clean control 10/10). 1,000 targets,
2,620 s wall clock, $0. Tally: 669 PASS_SCREEN, 331 DEAD, 0 with residue.

Do not cite the tally. The runner created each server's HOME and TMPDIR after handing the install
directory to `nobody`, so servers could not write to their own home. A sample of DEAD stderr shows
EACCES on mkdir and PermissionError under the work directory. Servers that died this way never got to
start children, so run 1 undercounts both live servers and possible residue. Fixed in the next commit;
run 2 replaces this one. The summary is kept because failed runs stay visible.
