# Replication package triage: 33 recent economics packages

Sample report, 21 November 2026, with rerun results added 26 November. Prepared by Raghav Sharma from public materials. Nothing in this report says whether any paper's results
are correct. A verdict says only whether the committed materials look able to run on a typical data desk, and why not.

## What this is

Before a reviewer spends a week on a replication package, a desk needs to know whether it can run at all. For each package below I
read its README and code, ran a triage script over every file, and checked each verdict by hand. No package code was executed.

Each package gets one of three verdicts:

- **runnable**: nothing found that stops an as-is run on a desk with the named software.
- **runnable-with-deviations**: it can probably run, after steps a receipt must log, such as downloading public data, choosing
  package versions, editing paths, or a long compute run.
- **blocked**: something the desk cannot supply is missing, usually confidential or commercial data.

The desk is assumed to hold Stata and MATLAB licences, as most economics data desks do.

## Summary

| Journal | Packages | Runnable as is | Runnable with logged changes | Blocked | Needs Stata or MATLAB | Triage verdict matched the hand check |
|---|---|---|---|---|---|---|
| JPE | 8 | 0 | 3 | 5 | 6 | 7 of 8 |
| REStud | 8 | 0 | 3 | 5 | 6 | 5 of 8 |
| Econometrics Journal | 6 | 2 | 4 | 0 | 4 | 4 of 6 |
| Econometrica | 4 | 0 | 1 | 3 | 3 | 4 of 4 |
| CJE | 2 | 0 | 1 | 1 | 2 | 2 of 2 |
| Economic Journal | 2 | 0 | 2 | 0 | 2 | 0 of 2 |
| Journal of Finance | 2 | 0 | 2 | 0 | 2 | 0 of 2 |
| JEEA | 1 | 1 | 0 | 0 | 1 | 1 of 1 |
| **All** | 33 | 3 | 16 | 14 | 26 | 23 of 33 |

- 14 of 33 packages (42%) are blocked. Seven of those need confidential administrative or firm data, four need commercial data
  (IHS Markit, CRSP, Data Axle, Refinitiv and others), and three do not hold their data in this public copy.
- Only 3 of 33 look runnable as committed. All three are small MATLAB packages with their data included.
- 26 of 33 need Stata or MATLAB. Of the 19 that are not blocked, only four can run on free software alone: gretl, R, Python or Julia.
- Among the 16 that can run with logged changes, the most common change is fetching data at run time or from an outside folder
  (Dropbox, Zenodo, BLS, FRED, a registration site), in 8 packages. The next is unpinned package versions. Two state full run
  times of 48 hours or more (48 and 160 hours).

## How good is the script on its own

On these 33 packages the triage script's verdict matched my hand check 23 times. Guessing "runnable with deviations" for every
package would have matched 16 times, and guessing "blocked" would have matched 14. Its stated main reason was right 17 times.

Its errors, which are the reason every verdict here was checked by hand:

- **2 packages called runnable that are blocked.** One holds no data at all and relies on Refinitiv, Compustat, EIU, Markit and
  MSCI. The other marks its business database as not provided. These are the costly kind of error, because each one sends a
  reviewer into a package that cannot finish.
- **8 packages called blocked that can run.** In most of these the script read files that the pipeline downloads or writes as
  missing inputs. It also failed to recognise gretl scripts, and in two cases it read a tab or line-ending character as a file name.
- **PDF and Word READMEs are not read.** Where the data statement sits only in a PDF, the script cannot see it.

The script is a first pass, not a referee. Its use is to point at the files a person should read first.

## Did the verdicts hold when the packages were run?

Six packages with a free-software route were later rerun from a clean checkout. Each rerun has its own receipt in this
repository. Four are from the table below, one (Cattaneo, Jansson and Nagasawa) is from the 25 November candidate list, and
one (Renner and Scheidegger, REStud) was triaged and rerun on 21 November.

| Package | Hand verdict | Script said | What the rerun found | Receipt |
|---|---|---|---|---|
| Assemblage VAR, Econometrics Journal | runnable-with-deviations (unpinned R packages) | runnable-with-deviations | Ran, exit 0, the package's own checks pass. 89 of 1,267 quoted numbers differ on Linux and 43 on Windows, mostly in the last digit | [receipt](../ectj-assemblage-var/RECEIPT.md) |
| Casoli and Lucchetti, Econometrics Journal | runnable-with-deviations (gretl add-ons fetched) | blocked (wrong) | All three Section 4 scripts ran; all 20 cells of the cointegration table match the working paper | [receipt](../ectj-casoli-lucchetti/run1/RECEIPT.md) |
| Conlon and Rao, JPE | runnable-with-deviations (processed data provided) | blocked (wrong) | Main estimation stops with current pyblp and with the numpy current at the commit date. The full run needs about 20 hours and has not finished on any machine here | [runs](../jpe-conlon-rao/) |
| Cattaneo, Jansson and Nagasawa, Econometrica | (candidate list) free software, inputs in repo | n/a | `Hhat.cpp` does not compile with current Rcpp as found. With one compile flag, all three files reproduce byte for byte | [receipt](../ecma-cattaneo-jansson-nagasawa/run2/RECEIPT.md) |
| Cattaneo, Ma, Masatlioglu and Suleymanov, JPE | (candidate list) one R script | n/a | Ran; the two null rates match the script's stated result; three power rates differ by 1 or 2 in 1,000 repetitions | [receipt](../jpe-cattaneo-ma-masatlioglu-suleymanov/runs/github-45671757826-linux/RECEIPT.md) |
| Renner and Scheidegger, REStud | runnable | blocked (wrong) | All 16 re-simulated cells of Tables 7 and 8 reproduce | [receipt](../restud-renner-scheidegger/RECEIPT.md) |

What this says, plainly. None of the six packages a hand verdict called runnable turned out to be blocked. The script on its
own called three of them blocked, which is why every verdict here is checked by hand. Two of the six (Conlon and Rao,
Cattaneo, Jansson and Nagasawa) hit a version break that neither the hand verdict nor the script named. A verdict says
where to look first. It does not replace a run.

## Per package

Each package is pinned to the commit it was read at. "Licence named" lists what the script found in the package text.

| # | Journal | Package (commit) | Verdict, hand-checked | Why | Paid software or data needed | Licence named | Triage said | Matched |
|---|---|---|---|---|---|---|---|---|
| 1 | CJE | [akhederlarian/pre-trends-TTBs](https://github.com/akhederlarian/pre-trends-TTBs/tree/e2077db1470536a50411c2acf253e5381e717f76) (`e2077db`) | blocked | World trade data from IHS Markit Global Trade Atlas is commercial and not included; US Census API extracts not posted | Stata, commercial data | none | blocked | yes |
| 2 | CJE | [bela-georgiev/CJE-replication-countryfood](https://github.com/bela-georgiev/CJE-replication-countryfood/tree/2b6e11b81503067210839f6b6a4493c5614d3af1) (`2b6e11b`) | runnable-with-deviations | Stata; all data included; run order and Stata version only in READ_ME.pdf | Stata | CC BY-NC | runnable-with-deviations | yes |
| 3 | Econometrica | [ekrose/rss_rep](https://github.com/ekrose/rss_rep/tree/fa5cc286e09c6e744e09d07e93b66590edfbcea3) (`fa5cc28`) | blocked | North Carolina school and court records are confidential; only simulated data are provided | Stata | BSD | blocked | yes |
| 4 | Econometrica | [rsaggio87/Replication_DKSS](https://github.com/rsaggio87/Replication_DKSS/tree/ddbe91801f7193c63aebb4fd74cc63b77b0041d4) (`ddbe918`) | blocked | INPS-INVIND worker data available only from the Bank of Italy | Stata, MATLAB | none | blocked | yes |
| 5 | Econometrica | [tholden/RobustRealRateRulesReplication](https://github.com/tholden/RobustRealRateRulesReplication/tree/41d8bf69e4b47dc71dd15aa2929db6eea131ef41) (`41d8bf6`) | runnable-with-deviations | MATLAB R2024a with toolboxes, Dynare 6.0 for one appendix; one file fetched at run time | MATLAB | CC BY-NC, CC0, BSD, GPL | runnable-with-deviations | yes |
| 6 | Econometrica | [zhexiaolin/Estimation-based-on-nearest-neighbor-matching](https://github.com/zhexiaolin/Estimation-based-on-nearest-neighbor-matching/tree/0d0d5539c4b74c667c23bb909d27eebdd495b2c8) (`0d0d553`) | blocked | Shadish application data are confidential; simulations claim about 336 hours and mention GPUs | none (Python, R) | MIT | blocked | yes |
| 7 | Econometrics Journal | [DavBrg/Structural-Forecast-Analysis-Final](https://github.com/DavBrg/Structural-Forecast-Analysis-Final/tree/3c18528c0bedd75867a4bb7a6418640345c3261d) (`3c18528`) | runnable-with-deviations | MATLAB; data included in one workbook; README is DOCX/PDF; three absolute paths | MATLAB | none | runnable-with-deviations | yes |
| 8 | Econometrics Journal | [InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication](https://github.com/InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication/tree/d46e6006dda79c13313daa02d405b76e53df0ae4) (`d46e600`) | runnable-with-deviations | gretl 2021c (free); data included; gretl add-on packages fetched from the gretl server | none (gretl) | CC BY | blocked | **no** |
| 9 | Econometrics Journal | [Paul-Haimerl/replication-fuse-time](https://github.com/Paul-Haimerl/replication-fuse-time/tree/d768f7539e679bda30f1663233147f3fd25cb8de) (`d768f75`) | runnable-with-deviations | R packages unpinned; MATLAB with CVX for the benchmark; about 48 hours | MATLAB | CC BY-NC, CC0, GPL | blocked | **no** |
| 10 | Econometrics Journal | [andreaviselli/comparing-predictive-ability-very-short-instability](https://github.com/andreaviselli/comparing-predictive-ability-very-short-instability/tree/09efc854d246d3b068c2e3f21e7ba8093561fede) (`09efc85`) | runnable | MATLAB R2023a; data included; public domain data | MATLAB | CC0, MIT | runnable | yes |
| 11 | Econometrics Journal | [andreaviselli/robust-fcast-eval-extreme-shocks](https://github.com/andreaviselli/robust-fcast-eval-extreme-shocks/tree/f8e38a2a1ecc99a9636fb674a59c601c54294a96) (`f8e38a2`) | runnable | MATLAB R2026a; data included; Econometrics Toolbox for one script | MATLAB | MIT | runnable | yes |
| 12 | Econometrics Journal | [timmy-o-toole/Assemblage_VAR](https://github.com/timmy-o-toole/Assemblage_VAR/tree/199c5f8c432c9571e601ce68ada49ab3d1819e55) (`199c5f8`) | runnable-with-deviations | R packages unpinned; processed data included and documented as sufficient; two commercial raw files excluded | none (R) | CC0, MIT | runnable-with-deviations | yes |
| 13 | Economic Journal | [johanneswieland/MPC2001](https://github.com/johanneswieland/MPC2001/tree/15a801cc5d4acae71a9956c52a016d5bb510f644) (`15a801c`) | runnable-with-deviations | Code downloads BLS, BEA and Philadelphia Fed data at run time; files it creates are not in the package by design | Stata | CC BY-NC, CC0, BSD, GPL | blocked | **no** |
| 14 | Economic Journal | [pzoch/demographic-transition-wealth-inequality](https://github.com/pzoch/demographic-transition-wealth-inequality/tree/bc01805b1e16ee906f200292c0f73d4b0b5568a8) (`bc01805`) | runnable-with-deviations | Figure route needs PSID and SCF extracts after registration; full rebuild needs restricted raw files and over 110 GB of bootstrap files | Stata, MATLAB | MIT | blocked | **no** |
| 15 | JEEA | [pmichaillat/pricing-fairness](https://github.com/pmichaillat/pricing-fairness/tree/a8d5d758eef3cffabe154e07b58e3cb150113a50) (`a8d5d75`) | runnable | MATLAB R2020a and Dynare 4.5.7, both named; figures only | MATLAB | MIT | runnable | yes |
| 16 | JPE | [apb-umn/managing-public-portfolios-replication](https://github.com/apb-umn/managing-public-portfolios-replication/tree/b9de92dd229ac162a5fafd4a46c8be17e23ef11e) (`b9de92d`) | blocked | CRSP returns are a subscription dataset and are not included; other data public, FRED fetched at run time | none (Python, Julia), CRSP subscription | none | blocked | yes |
| 17 | JPE | [chrisconlon/Liquor_Replication_JPE](https://github.com/chrisconlon/Liquor_Replication_JPE/tree/97567b1968f44980a47a7b72c1928a5e01255a67) (`97567b1`) | runnable-with-deviations | Entry point 2 starts from the provided processed data; NielsenIQ licence needed only for the raw cleaning stage; one large pickle must be rebuilt | none (Python, R), licensed data for stage 1 | MIT | blocked | **no** |
| 18 | JPE | [fediskhakov/EQB](https://github.com/fediskhakov/EQB/tree/33c68b4f7de035c1a86ee5450146905800a0a966) (`33c68b4`) | runnable-with-deviations | MATLAB; tabulated data included; one Python notebook with no requirements file | MATLAB | CC BY-NC, GPL | runnable-with-deviations | yes |
| 19 | JPE | [mbholm/Asset-Price-Redistribution](https://github.com/mbholm/Asset-Price-Redistribution/tree/6636b72eafad8506756f4fa7e76b50b542ab70ad) (`6636b72`) | blocked | Statistics Norway registers are confidential; Worldscope is private | Stata | none | blocked | yes |
| 20 | JPE | [mbholm/Transmission-of-Monetary-Policy-under-the-Microscope](https://github.com/mbholm/Transmission-of-Monetary-Policy-under-the-Microscope/tree/c7677d15754508208d41f83e547fa64018a841d5) (`c7677d1`) | blocked | Statistics Norway registers are confidential | Stata, MATLAB | none | blocked | yes |
| 21 | JPE | [pcmichaud/agghealth_replicate](https://github.com/pcmichaud/agghealth_replicate/tree/360fec651d2b451d5bc8b2b30f5b1ce7177f3f70) (`360fec6`) | blocked | The data_sources folder the README describes is not in this GitHub copy | MATLAB | none | blocked | yes |
| 22 | JPE | [ymohanty/rationing-commons](https://github.com/ymohanty/rationing-commons/tree/4d60ad2f8d12ced60106c70649d8984b8d97bce0) (`4d60ad2`) | blocked | No data in this repository; the farmer survey holds personal information and needs authorisation | Stata, MATLAB | GPL | blocked | yes |
| 23 | JPE (JPE Macro) | [rolf-campos/navigating-replication](https://github.com/rolf-campos/navigating-replication/tree/e5404a755fb7a30d82a311669bf5ee1451a0a616) (`e5404a7`) | runnable-with-deviations | Stata 17, MATLAB R2021b and Python; data included; Python packages unpinned | Stata, MATLAB | MIT | runnable-with-deviations | yes |
| 24 | Journal of Finance | [lefarmer89/pockets-of-predictability-reply](https://github.com/lefarmer89/pockets-of-predictability-reply/tree/22c6be1295b898a9ad9b963f1061cac6e6fcfb7c) (`22c6be1`) | runnable-with-deviations | Cached results (0.8 GB) and external data (7.8 GB) download from Dropbox; full rerun 10 to 20 hours on 8 cores | MATLAB | MIT | blocked | **no** |
| 25 | Journal of Finance | [pcmichaud/repl_msa_jf](https://github.com/pcmichaud/repl_msa_jf/tree/487849e1733d37c3aa6ff6ccf95432b0af701dea) (`487849e`) | runnable-with-deviations | Survey data included; Statistics Canada public files to download, one through institutional ODESI access; about 160 hours | Stata | CC BY-NC, CC0, GPL | blocked | **no** |
| 26 | REStud | [LindseyRRay/HiringAsExplorationReplPackage](https://github.com/LindseyRRay/HiringAsExplorationReplPackage/tree/d830a57846520bbaa1dd12a964abed4fc80e5b48) (`d830a57`) | blocked | Confidential firm personnel data under a data use agreement | Stata | MIT | blocked | yes |
| 27 | REStud | [floswald/LandUse-REStud](https://github.com/floswald/LandUse-REStud/tree/5b7f48c533dff10d5658e842820332c5c3228542) (`5b7f48c`) | blocked | Development copy without data; its README says it cannot replicate the results | Stata | CC BY, CC0 | blocked | yes |
| 28 | REStud | [gabrielgggg/DeadlyDebtCrises](https://github.com/gabrielgggg/DeadlyDebtCrises/tree/62d163e82276e1bc79d00adba0f075ca8b9766dc) (`62d163e`) | runnable-with-deviations | Cleaned data included (some from commercial sources, redistributed in cleaned form); Fortran, Stata and MATLAB; README is a PDF | Stata, MATLAB | none | blocked | **no** |
| 29 | REStud | [haanwinckel/HaanwinckelSoares2021](https://github.com/haanwinckel/HaanwinckelSoares2021/tree/297d90a561bf2d6001fefe9cd4f03a20496c2b33) (`297d90a`) | runnable-with-deviations | Cleaned data at the official Zenodo package; 1991 Census from IBGE on request for one appendix | Stata, MATLAB | CC BY | runnable-with-deviations | yes |
| 30 | REStud | [jblumenstock/migration_networks_replication](https://github.com/jblumenstock/migration_networks_replication/tree/2651b34cf01a2c9892117c90e1d8dae837b5201c) (`2651b34`) | blocked | Rwanda mobile phone records are private; only sample data are provided | none (Python, R) | CC BY-NC, GPL | blocked | yes |
| 31 | REStud | [jrblevin/epl-replication](https://github.com/jrblevin/epl-replication/tree/ab20cf057c991fbaf5759f46f0caeaba33b4d0a8) (`ab20cf0`) | blocked | The application needs Data Axle business data, which the README marks as not provided; Monte Carlo runs are possible | MATLAB, Stata | none | runnable-with-deviations | **no** |
| 32 | REStud | [kelloggrk/Public_EndOfOil](https://github.com/kelloggrk/Public_EndOfOil/tree/b491fbac63c7387de74e1f3f89a279e556574e16) (`b491fba`) | runnable-with-deviations | Julia with no Manifest; intermediate files from a public Dropbox folder | none (Julia) | none | runnable-with-deviations | yes |
| 33 | REStud | [mschwedeler/countryrisk](https://github.com/mschwedeler/countryrisk/tree/17caff81a4ee30e83cf3d70211871aff2c7fbffe) (`17caff8`) | blocked | No data in the repository; Refinitiv transcripts, Compustat (WRDS), EIU, Markit and MSCI are commercial | Stata, commercial data | none | runnable-with-deviations | **no** |

## Method

- **Selection.** Public GitHub repositories, created after mid-2021 and not forks, that are the authors' own replication package (or
  the authors' mirror of the journal archive) for a paper published, accepted or forthcoming in Econometrica, REStud, the Economic
  Journal, the Econometrics Journal, JEEA, JPE (including JPE Macro), the Journal of Finance or the Canadian Journal of Economics.
  The journal had to be named in the package text or the repository description. I excluded third-party re-replications, ports to
  another language, course work, theses, and papers that are only submitted. The search found 36. Two were dropped because no file named
  the journal, and the other 34 were pinned by commit before triage ran. One more was dropped after the run, because the journal it
  named was only a cited data source. The full selection is in `triage/SURVEY_2026-11-21.json` in the reproduction-receipts repository.
- **Triage.** One run per package of `triage/triage.py` (SHA-256 `c2ddd83b…3138ca`), with `--have stata,matlab`. It took
  under a second for most packages and 15 seconds for the largest. The total compute cost was nil beyond a laptop-class machine.
- **Hand check.** I read each README (and the PDF or Word README where that is the only full one) and the files the script named,
  then wrote my own verdict before comparing it with the script's. My verdict is a reading, not a run.

## Limits

- **These are GitHub copies, not the journals' archives.** The archives on openICPSR, Zenodo and Dataverse were not reachable from
  the machine this ran on. A journal's archived copy can differ from the authors' GitHub copy, most often by including data the
  GitHub copy leaves out. Three "blocked" verdicts (data not in this copy) may not hold for the archived package.
- **Links were not checked.** The machine's network refuses most outside hosts, so a link test there would report working links as
  dead. No verdict here rests on a dead link.
- **No package was run.** "Runnable" means nothing was found that stops a run. It does not mean the run reproduces the paper.
- **One reader.** Every hand verdict is one person's reading, and some are judgement calls. Examples are a package that runs only
  from its provided intermediate files, or one where part of the paper runs and the rest needs licensed data. The reason column
  says which.
- **33 packages, not 50.** The aim was 50. GitHub held 33 authors' packages for these journals that met the selection rule, and
  none for Economic Inquiry. The per-journal counts are small and do not describe each journal's whole archive.
