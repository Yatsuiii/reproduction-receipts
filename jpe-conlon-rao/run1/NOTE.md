# Run 1, kept as found

`RECEIPT-generator-v1.md` was written by the first version of `receiptgen/rerun.py`. **Its headline overcounts.** It calls
Tables 6 to 8 reproduced, but the steps that write the intermediate files those tables read (`3a`, `3b`, `3c`) had failed,
so `6_counterfactual_plots.py` formatted them from the committed `results/*.parquet`. That shows the committed intermediates
produce the committed tables, nothing more. The generator was fixed after this run (a failure injection first, see
`receiptgen/FROZEN_CHANGES.md`), and run 2 is reported with the fixed version.

What run 1 does show, from its logs:

1. `pip install -r requirements.txt` resolved pyblp 1.3.0 (released 14 Oct 2026; the package is from 19 Mar 2026 and asks
   for "0.13+").
2. `estimate_demand_MAIN.py` stopped after 4 seconds: pyblp 1.3.0 rejects the second-choice micro dataset ("In market '24',
   the products with eliminated product ID '999' span multiple nesting groups without covering all of them"). That check
   is not in pyblp 1.1.0, 1.1.2 or 1.2.0. Every later step that needs `slow_paper.pickle` failed for want of it.
3. `1_descriptive_tables.py` wrote Table 1 (identical to the committed file) and then stopped: it saves to a `checks/`
   folder that is not in the repository (git does not keep empty folders).
4. `12_panel_regressions.py` regenerated Appendix Tables A9 and A10 byte for byte from the public data in `raw_data/`.
