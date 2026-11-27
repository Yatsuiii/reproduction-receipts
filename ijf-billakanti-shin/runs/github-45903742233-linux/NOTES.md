# Notes on run 2, written after the run

Main paper only, Tables 1-7 as CSV, on an x86-64 Linux runner (the package's tested platform is macOS on Apple Silicon).

- Table 1 matches every number within 1e-12 relative.
- In Tables 2-7, 92 values differ from the committed ones. They fall in two groups.
  - Almost all differ only around the eighth significant digit (for example 0.0631581642921904 committed, 0.06315816363302572
    here). That is the size usually seen when the same floating-point work runs on a different CPU and maths library. These
    are still outside the package's own absolute tolerance of 5e-12.
  - The values that differ in the third decimal are all in rows for the Random Forest benchmark ($X_t$, Random Forest):
    Table 2's benchmark row (PR-AUC at h=12: 0.4126 committed, 0.4201 here; at h=6: 0.3844 and 0.3817) and the
    Random-Forest pairings in Table 4 (for example the Random Forest p-value at h=6: 0.0740 committed, 0.0685 here; at
    h=12: 0.0296 and 0.0231). The Logit-L2 numbers in those same rows move only slightly (h=12 p-value 0.0090 committed,
    0.0112 here).
- None of the Table 4 p-values in those rows crosses 0.05 between the two runs.
- Reason unknown. This run does not say which platform is right, or that anything in the paper is wrong. A likely place to
  look is how the Random Forest's randomness and threading depend on the machine, but that was not tested here.
- The appendix (Tables 8-22, Figure 4) was not run; the full run passes this runner's time limit (run 1).
