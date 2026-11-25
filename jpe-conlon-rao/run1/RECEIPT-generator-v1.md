# Receipt: Conlon and Rao, "The Cost of Curbing Externalities with Market Power: Alcohol Regulations and Tax Alternatives" (Journal of Political Economy, forthcoming)

**Status, 2026-11-25 16:39 UTC: 2 of 9 commands exited 0. 7 of 25 declared outputs reproduced (7 byte-identical). 2 did not regenerate the committed file; the committed materials did not reproduce those values here, reason unknown. 9 were not written by the run, so they are not counted. 4 (figures or other files declared hash-only) were rewritten and hashed, not compared. 1 were not produced.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on this machine. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' repository [chrisconlon/Liquor_Replication_JPE](https://github.com/chrisconlon/Liquor_Replication_JPE), README Entry Point 2 (no NielsenIQ access), commit `97567b1968f44980a47a7b72c1928a5e01255a67`.
- Paper: Christopher T. Conlon and Nirupama S. Rao, The Cost of Curbing Externalities with Market Power: Alcohol Regulations and Tax Alternatives, Journal of Political Economy, forthcoming.
- 257 tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256) (SHA-256 of that list `0e2eed899de23b9b…`).
- Protocol and comparison rule, committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md).
- Comparison: each declared output, after the run, against the committed file of the same path. Numbers are compared one by one with relative tolerance 1e-12; all other text must be identical.
- Entry Point 2 of the README: demand estimation from the provided `estimation_data/`, then the counterfactuals and their tables. Stage 1 (cleaning from NielsenIQ) needs licensed data and is not run.
- The README's Stage 3 asks for `slow_paper.pickle` from a Dataverse DOI marked TBD. That file is not in the repository, so here it is produced by the README's own Stage 2 command (`estimate_demand_MAIN.py`) and used by every later step.
- Not run: the nested logit, demographics-only and fast RCNL specifications (they feed no main-text table compared here), the rho grid, and the five appendix notebooks. Figures 7 and 8 are hashed only. The paper's PDF was not compared.

## Result

| Command | Exit | Time | Output | Outcome | Reproduced |
|---|---|---|---|---|---|
| `cd counterfactual_code && ../venv/bin/python 1_descriptive_tables.py` | 1 | 9 s | `tables_and_figures/table1_summary_tab_cat.tex` | identical to the committed file; written by a command that did not exit 0 | no |
|  |  |  | `tables_and_figures/table2_summary_tab_manuf.tex` | text differs from the committed file; written by a command that did not exit 0 | no |
|  |  |  | `app_figures/summary_tab_cat_all.tex` | identical to the committed file; written by a command that did not exit 0 | no |
|  |  |  | `app_figures/summary_tab_manuf_all.tex` | text differs from the committed file; written by a command that did not exit 0 | no |
|  |  |  | `app_figures/size_cat_table.tex` | not written by this run, so not compared | no |
| `cd counterfactual_code && ../venv/bin/python 12_panel_regressions.py` | 0 | 5 s | `tables_and_figures/ph_panelreg.tex` | identical to the committed file | yes |
|  |  |  | `tables_and_figures/ph_retailreg.tex` | identical to the committed file | yes |
| `cd estimation_code && ../venv/bin/python estimate_demand_MAIN.py ../estimation_outputs/slow_paper.pickle` | 1 | 4 s | `estimation_outputs/slow_paper.pickle` | not produced | no |
| `cd estimation_code && ../venv/bin/python post_estimation.py ../estimation_outputs/slow_paper.pickle` | 1 | 1 s | `estimation_outputs/slow_paper_mc.parquet` | not written by this run, so not compared | no |
| `cd counterfactual_code && ../venv/bin/python 4_parameter_tables.py` | 1 | 2 s | `tables_and_figures/table3_parameter_results.tex` | not written by this run, so not compared | no |
|  |  |  | `tables_and_figures/table4_diversion_results.tex` | not written by this run, so not compared | no |
| `cd counterfactual_code && ../venv/bin/python 3a_compute_counterfactual.py --all` | 1 | 2 s | `(none declared)` |  |  |
| `cd counterfactual_code && ../venv/bin/python 3b_collate_cf.py` | 1 | 0 s | `results/all_both_taxes.parquet` | not written by this run, so not compared | no |
|  |  |  | `results/all_endog.parquet` | not written by this run, so not compared | no |
|  |  |  | `results/all_main.parquet` | not written by this run, so not compared | no |
|  |  |  | `results/all_mc1.parquet` | not written by this run, so not compared | no |
| `cd counterfactual_code && ../venv/bin/python 3c_compute_counterfactual_both_tax.py` | 1 | 1 s | `(none declared)` |  |  |
| `cd counterfactual_code && ../venv/bin/python 6_counterfactual_plots.py` | 0 | 22 s | `tables_and_figures/table6_distributional_effects_main.tex` | identical to the committed file | yes |
|  |  |  | `tables_and_figures/table7_welfare_volume_main.tex` | identical to the committed file | yes |
|  |  |  | `tables_and_figures/table8_welfare_ethanol_main.tex` | identical to the committed file | yes |
|  |  |  | `tables_and_figures/table8_welfare_ethanol_short.tex` | identical to the committed file | yes |
|  |  |  | `tables_and_figures/alt_table6_distributional_effects_mc1_v2.tex` | identical to the committed file | yes |
|  |  |  | `tables_and_figures/figure7_prices_triple.pdf` | not written by this run, so not compared | no |
|  |  |  | `tables_and_figures/figure7a_prices_main.pdf` | rewritten; hashed only, not compared (declared hash-only in the spec) | no |
|  |  |  | `tables_and_figures/figure7b_prices_main.pdf` | rewritten; hashed only, not compared (declared hash-only in the spec) | no |
|  |  |  | `tables_and_figures/figure7c_prices_main.pdf` | rewritten; hashed only, not compared (declared hash-only in the spec) | no |
|  |  |  | `tables_and_figures/figure8_welfare_main.pdf` | rewritten; hashed only, not compared (declared hash-only in the spec) | no |

Not written by this run: `app_figures/size_cat_table.tex`, `estimation_outputs/slow_paper_mc.parquet`, `tables_and_figures/table3_parameter_results.tex`, `tables_and_figures/table4_diversion_results.tex`, `results/all_both_taxes.parquet`, `results/all_endog.parquet`, `results/all_main.parquet`, `results/all_mc1.parquet`, `tables_and_figures/figure7_prices_triple.pdf`. A committed file that the run leaves untouched may be read back rather than recomputed, so it counts for nothing here.

## Environment

| | |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| CPU | Intel(R) Xeon(R) Processor @ 2.10GHz |
| Cores | 4 |
| RAM | 15.7 GB |
| GPU | none |
| git | git version 2.43.0 |
| python3 | Python 3.13.18 |
| R | R version 4.3.3 (2024-02-29) -- "Angel Food Cake" |

Full environment listings: [`evidence/environment.json`](evidence/environment.json).

## Wall clock and cost

Commands ran for 1 min 30 s in all, one after another, from 2026-11-25T16:37:42Z to 2026-11-25T16:39:21Z.
At 0.2 USD an hour for this machine (typical on-demand price for a 4 vCPU, 16 GB cloud machine), that is about 0.01 USD.

## Deviations, in order

1. `cd counterfactual_code && ../venv/bin/python 6_counterfactual_plots.py` changed tracked files that are not declared outputs: `tables_and_figures/alt_figure7_prices_mc1_v2.pdf`, `tables_and_figures/alt_figure7_prices_period_1.pdf`, `tables_and_figures/alt_figure8_welfare_mc1_v2.pdf`, `tables_and_figures/alt_figure8_welfare_period_1.pdf`.
2. At least one output was written by a command that did not exit 0. It is listed but not counted as reproduced.

## Failed, stopped or killed runs

1. `cd counterfactual_code && ../venv/bin/python 1_descriptive_tables.py`: exit 1 after 9 s. [Log](evidence/logs/1_descriptive_tables.log).
2. `cd estimation_code && ../venv/bin/python estimate_demand_MAIN.py ../estimation_outputs/slow_paper.pickle`: exit 1 after 4 s. [Log](evidence/logs/estimate_demand_MAIN.log).
3. `cd estimation_code && ../venv/bin/python post_estimation.py ../estimation_outputs/slow_paper.pickle`: exit 1 after 1 s. [Log](evidence/logs/post_estimation.log).
4. `cd counterfactual_code && ../venv/bin/python 4_parameter_tables.py`: exit 1 after 2 s. [Log](evidence/logs/4_parameter_tables.log).
5. `cd counterfactual_code && ../venv/bin/python 3a_compute_counterfactual.py --all`: exit 1 after 2 s. [Log](evidence/logs/3a_compute_counterfactual.log).
6. `cd counterfactual_code && ../venv/bin/python 3b_collate_cf.py`: exit 1 after 0 s. [Log](evidence/logs/3b_collate_cf.log).
7. `cd counterfactual_code && ../venv/bin/python 3c_compute_counterfactual_both_tax.py`: exit 1 after 1 s. [Log](evidence/logs/3c_compute_counterfactual_both_tax.log).

## Evidence

- [`results.json`](results.json): every number above, with each command's start, end and exit code.
- [`evidence/logs/`](evidence/logs/): stdout and stderr of every command.
- [`evidence/outputs/`](evidence/outputs/): every output this run wrote.
- Generated by `receiptgen/rerun.py` from the spec in `results.json`.
