# Receipt: Billakanti and Shin, "At-Risk Transformation for U.S. Recession Prediction" (International Journal of Forecasting, conditionally accepted): first Linux run, main paper

**Status, 2026-11-27 00:29 UTC: 2 of 2 commands exited 0. 1 of 7 declared outputs reproduced (1 equal in every number within 1e-12 relative). 6 did not regenerate the committed file, 92 values in all; the committed materials did not reproduce those values here, reason unknown.**

This was done unasked, by someone with no connection to the authors or the journal. It says what the committed
materials did on this machine. It does not say anything about whether the paper is right.

## What was checked

- Package: the authors' repository [mcmcs/At-Risk-Public](https://github.com/mcmcs/At-Risk-Public), commit `4ec0c1de156a19cd0fa318dd4a885d253fbb27ed`.
- Paper: Rahul Billakanti and Minchul Shin, At-Risk Transformation for U.S. Recession Prediction, International Journal of Forecasting, conditionally accepted.
- 154 tracked files, each hashed in [`evidence/package-files.sha256`](evidence/package-files.sha256) (SHA-256 of that list `dd861cd1f21252e2…`).
- Protocol and comparison rule, committed before any package code ran: [`PROTOCOL.md`](PROTOCOL.md).
- Comparison: each declared output, after the run, against the committed file of the same path. Numbers are compared one by one with relative tolerance 1e-12; all other text must be identical.
- Main paper only: Tables 1-7 as CSV. LaTeX tables carry a run fingerprint comment and figures are PDFs, so they are not compared here. The appendix (Tables 8-22, Figure 4) is not run.
- The tested platform is macOS on Apple Silicon. This is an x86-64 Linux runner, so the run also says whether the results carry across platforms.

## Result

| Command | Exit | Time | Output | Outcome | Reproduced |
|---|---|---|---|---|---|
| `cd program_v04 && .venv/bin/python -m program_v04.main.run_main --input-mode public` | 0 | 2 h 11 min | `(none declared)` |  |  |
| `cp program_v04/output/main/tables/*.csv reference/output/main/tables/` | 0 | 0 s | `reference/output/main/tables/table01_single_binary_summary.csv` | every number equal to the committed file within the tolerance; bytes differ (24 of 30 numbers identical text) | yes |
|  |  |  | `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | did not regenerate the committed values: 9 of 38 numbers | no |
|  |  |  | `reference/output/main/tables/table03_aggregation_comparison.csv` | did not regenerate the committed values: 10 of 45 numbers | no |
|  |  |  | `reference/output/main/tables/table04_encompassing_tests.csv` | did not regenerate the committed values: 28 of 60 numbers | no |
|  |  |  | `reference/output/main/tables/table05_mse_decomposition_h3.csv` | did not regenerate the committed values: 3 of 6 numbers | no |
|  |  |  | `reference/output/main/tables/table06_feature_importance.csv` | did not regenerate the committed values: 10 of 31 numbers | no |
|  |  |  | `reference/output/main/tables/table07_sector_contribution.csv` | did not regenerate the committed values: 32 of 68 numbers | no |

### Values that did not regenerate

The committed materials did not reproduce these values on this machine, reason unknown. Line numbers are lines of the output file. The full list is in `results.json`.

| Output | Line | Committed | Regenerated |
|---|---|---|---|
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 5 | 0.0631581642921904 | 0.06315816363302572 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 5 | 0.08649560310915522 | 0.08649560304866484 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 5 | 0.10496414834183229 | 0.10496414825138352 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 6 | 0.5871605239516309 | 0.5872770966432267 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 6 | 0.05944214285714285 | 0.05948166666666666 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 6 | 0.38439869006941185 | 0.38170798961936225 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 6 | 0.07223238095238095 | 0.07227999999999998 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 6 | 0.4125728745235048 | 0.420071609295358 |
| `reference/output/main/tables/table02_zt_vs_benchmarks.csv` | 6 | 0.07068904761904762 | 0.07052190476190476 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 3 | 0.05941969651374924 | 0.05941969734871816 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 3 | 0.09008001668615043 | 0.09008001737310173 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 3 | 0.09236899101545284 | 0.09236899231622021 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 5 | 0.102508393630588 | 0.10250839389881886 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 5 | 0.1424631193014328 | 0.1424631188403671 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 5 | 0.11562152977728055 | 0.11560824860274177 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 5 | 0.131090971694137 | 0.13109157164376273 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 7 | 0.05245600306051973 | 0.05245600367618478 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 7 | 0.06723569914694515 | 0.06723569826783932 |
| `reference/output/main/tables/table03_aggregation_comparison.csv` | 7 | 0.0868573321462641 | 0.08685733220566189 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 2 | -0.01450481739915004 | -0.014504817399125297 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 3 | 0.7266024679877018 | 0.7266024524051495 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 3 | 5.610838947765513e-07 | 5.610842476185222e-07 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 3 | -0.023765325447434153 | -0.023765316605247035 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 3 | 0.7272657217461909 | 0.727265821774767 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 4 | 0.4196498497356429 | 0.4192437794322006 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 4 | 0.001426954846506276 | 0.0014411198203174989 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 4 | 0.39464881575121497 | 0.3957530110652952 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 4 | 0.027803608529637185 | 0.02839531774149061 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 7 | 0.6952752286171854 | 0.6952754547520087 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 7 | 4.816206439118614e-09 | 4.8160589581226445e-09 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 7 | -0.04518753323964164 | -0.04518771258571849 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 7 | 0.38390613194384604 | 0.38390423348136193 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 8 | 0.4072210876515942 | 0.4014762499156874 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 8 | 0.0010009571213895712 | 0.0012464139840490098 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 8 | 0.2594687147985696 | 0.2666038217180211 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 8 | 0.07402370406845016 | 0.06846280942920438 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 9 | 0.01213476827733316 | 0.012134768277320433 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 11 | 0.8789392597697834 | 0.8789392529548645 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 11 | 8.194166125793028e-06 | 8.194168848365124e-06 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 11 | -0.012222428677745274 | -0.012222426670567357 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 11 | 0.7847880671996724 | 0.7847881042417196 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 12 | 0.482676260871951 | 0.4668918507592393 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 12 | 0.008984275352646585 | 0.01120542512098158 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 12 | 0.3125895331808877 | 0.3300596067830239 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 12 | 0.02961341487177834 | 0.023125155181233408 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 13 | 1.2091922268587973e-08 | 1.2091922268601326e-08 |
| `reference/output/main/tables/table04_encompassing_tests.csv` | 13 | -0.010780505888862415 | -0.01078050588880591 |
| `reference/output/main/tables/table05_mse_decomposition_h3.csv` | 3 | 0.5233131659995177 | 0.5233131648083835 |
| `reference/output/main/tables/table05_mse_decomposition_h3.csv` | 3 | 0.014720795691419097 | 0.014720795088251217 |
| `reference/output/main/tables/table05_mse_decomposition_h3.csv` | 3 | 0.0631581642921904 | 0.06315816363302572 |
| `reference/output/main/tables/table06_feature_importance.csv` | 2 | 12.506191591707774 | 12.506191590982384 |
| `reference/output/main/tables/table06_feature_importance.csv` | 3 | 11.369226786104548 | 11.369226778866395 |
| `reference/output/main/tables/table06_feature_importance.csv` | 4 | 11.125158954703485 | 11.125158958170784 |
| `reference/output/main/tables/table06_feature_importance.csv` | 5 | 6.664173616548934 | 6.664173613724715 |
| `reference/output/main/tables/table06_feature_importance.csv` | 6 | 4.759328276937984 | 4.759328277358037 |
| `reference/output/main/tables/table06_feature_importance.csv` | 7 | 3.5463779851198924 | 3.546377984023275 |
| `reference/output/main/tables/table06_feature_importance.csv` | 8 | 3.24587371609007 | 3.2458737152832104 |
| `reference/output/main/tables/table06_feature_importance.csv` | 9 | 2.85170070759237 | 2.8517006980606094 |
| `reference/output/main/tables/table06_feature_importance.csv` | 10 | 2.4600843345148653 | 2.4600843326473036 |
| `reference/output/main/tables/table06_feature_importance.csv` | 11 | 2.4171128427429474 | 2.417112844322906 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 10 | 3.2845619329929345 | 3.2845618965724808 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 10 | 2.57158051264698 | 2.571580516418756 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 10 | 3.7438009181590948 | 3.7438009173017983 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 10 | 6.378338832335082 | 6.378338832968146 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 11 | 19.235000993180815 | 19.235001315791816 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 11 | 19.796533585932377 | 19.796533628358297 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 11 | 28.68424668356587 | 28.68424667665147 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 11 | 20.867015522012082 | 20.867015490346144 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 12 | 2.293762139771989 | 2.2937621595034354 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 12 | 12.389442785727809 | 12.38944277139408 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 12 | 12.44058889790761 | 12.440588905232886 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 12 | 13.514339254904941 | 13.514339258662314 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 13 | 0.5160612766743394 | 0.516061262588534 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 13 | 1.5558478712272414 | 1.55584787475782 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 13 | 2.6431086307001923 | 2.643108631297772 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 13 | 0.7848163918855356 | 0.7848163920560498 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 14 | 0.812188199394412 | 0.812187828709571 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 14 | 5.101239114154406 | 5.101239115034359 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 14 | 0.9541491052982316 | 0.9541491056060485 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 14 | 0.7808891528481469 | 0.7808891341652546 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 15 | 66.71933204612459 | 66.71933217878689 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 15 | 53.33930677102148 | 53.33930670792247 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 15 | 47.21600675490917 | 47.21600675794046 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 15 | 54.716662902196646 | 54.71666292931048 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 16 | 0.9649895963900985 | 0.9649896048185569 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 16 | 0.5788804231712771 | 0.5788804272530359 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 16 | 1.399351825578732 | 1.3993518232704438 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 16 | 1.0580367626389384 | 1.0580367830215434 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 17 | 6.174103815470825 | 6.174103753228721 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 17 | 4.667168936118434 | 4.6671689588611835 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 17 | 2.918747183881096 | 2.918747182699123 |
| `reference/output/main/tables/table07_sector_contribution.csv` | 17 | 1.8999011811786233 | 1.899901179470068 |

## Environment

| | |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| CPU | AMD EPYC 9V74 80-Core Processor |
| Cores | 4 |
| RAM | 15.6 GB |
| GPU | none |
| git | git version 2.56.1 |
| python3 | Python 3.12.10 |
| julia | julia version 1.13.4 |

Full environment listings: [`evidence/environment.json`](evidence/environment.json).

## Wall clock and cost

Commands ran for 2 h 12 min in all, one after another, from 2026-11-26T22:17:05Z to 2026-11-27T00:29:16Z.
At 0.0 USD an hour for this machine (GitHub-hosted ubuntu-24.04 runner, free for public repositories (a comparable 4 vCPU cloud machine is about 0.20 USD an hour)), that is about 0.00 USD.

## Deviations, in order

1. Run 2 runs only the README's main-paper command (Figures 1-3, Tables 1-7), because the full run passed this runner's time limit in run 1.
2. The package's own comparison script checks all 50 outputs and so cannot run on the main paper alone. Instead the seven regenerated main-table CSVs are copied over the committed reference CSVs, and receiptgen compares each with the committed file, number by number, at relative tolerance 1e-12. The package's own rule is absolute 5e-12; both are given in the notes.

## Failed, stopped or killed runs

None.

## Evidence

- [`results.json`](results.json): every number above, with each command's start, end and exit code.
- [`evidence/logs/`](evidence/logs/): stdout and stderr of every command.
- [`evidence/outputs/`](evidence/outputs/): every output this run wrote.
- Generated by `receiptgen/rerun.py` from the spec in `results.json`.
