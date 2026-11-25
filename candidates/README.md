# Candidates for an unasked receipt, target journals, 25 Nov 2026

Step three of the build order: recent papers in the target journals (REStud, Econometrica, JPE, Journal of Finance,
Economic Journal, JEEA, CJE, Economic Inquiry, Econometrics Journal) whose authors published a replication package, ranked
by the chance of a clean, boring, complete rerun on this kind of machine: Linux, free software only, a network that reaches
GitHub and PyPI but not CRAN, Zenodo, Dataverse, openICPSR or Dropbox.

How it was made:

- **Sources.** The 33 packages of the [21 Nov triage survey](https://github.com/Yatsuiii/reproduction-receipts/pull/12),
  with their hand verdicts; a new GitHub search on 25 Nov (each target journal's name with "replication", Python, R or
  Julia, pushed since 1 Jan 2025: 500 repositories, 143 after dropping course work, and of those only the authors' own
  packages kept); and the Journal of Econometrics package already rerun in draft PR 16.
- **Rule.** [`score.py`](score.py): four gates (target journal, authors' own package, no proprietary software for the tier
  to be rerun, every input reachable) and then points for inputs in the repository, committed numeric outputs to compare,
  stated run time, pinned versions, stated seeds, recency, and whether the tier recomputes main estimates. Facts per
  package, with the file each came from, are in [`candidates.json`](candidates.json).
- **Honest note on order.** The rule was written the same afternoon as the facts, after I had read the two top packages.
  It is a record of why they were picked, not a blind test of the ranking.

## Ranked (passed every gate)

| Points | Journal | Package | Tier to rerun | Status |
|---|---|---|---|---|
| 10 | Econometrics Journal | [timmy-o-toole/Assemblage_VAR](https://github.com/timmy-o-toole/Assemblage_VAR/tree/199c5f8c432c9571e601ce68ada49ab3d1819e55) | `Rscript run_all.R` fast mode | rerun started 25 Nov ([ectj-assemblage-var](../ectj-assemblage-var/)) |
| 9 | JPE | [chrisconlon/Liquor_Replication_JPE](https://github.com/chrisconlon/Liquor_Replication_JPE/tree/97567b1968f44980a47a7b72c1928a5e01255a67) | Entry Point 2: RCNL estimation, post-estimation, Tables 3-4, counterfactuals, Tables 6-8 | rerun started 25 Nov ([jpe-conlon-rao](../jpe-conlon-rao/)) |
| 7 | Econometrics Journal | [InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication](https://github.com/InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication/tree/d46e6006dda79c13313daa02d405b76e53df0ae4) | empirical analysis (gretl) |  |
| 7 | Econometrica | [mdcattaneo/replication-CJN_2020_ECMA](https://github.com/mdcattaneo/replication-CJN_2020_ECMA/tree/b03241c) | simulation tables (R with Rcpp) |  |
| 3 | JPE | [mdcattaneo/replication-CMMS_2020_JPE](https://github.com/mdcattaneo/replication-CMMS_2020_JPE/tree/d307dcd) | one R script |  |

## Gated out

29 of the 33 survey packages fail a gate, almost all on proprietary software (Stata or MATLAB, 26 of 33) or data that a
desk cannot get (confidential registers, commercial databases). That is the main finding of this list: in these journals, a
free-software rerun with every input in the repository is rare. Five of 38 packages pass every gate.

| Journal | Package | Gate failed | Why |
|---|---|---|---|
| CJE | akhederlarian/pre-trends-TTBs | free_software, inputs_available | World trade data from IHS Markit Global Trade Atlas is commercial and not included; US Census API extracts not posted |
| CJE | bela-georgiev/CJE-replication-countryfood | free_software | Stata; all data included; run order and Stata version only in READ_ME.pdf |
| Econometrica | ekrose/rss_rep | free_software, inputs_available | North Carolina school and court records are confidential; only simulated data are provided |
| Econometrica | rsaggio87/Replication_DKSS | free_software, inputs_available | INPS-INVIND worker data available only from the Bank of Italy |
| Econometrica | tholden/RobustRealRateRulesReplication | free_software | MATLAB R2024a with toolboxes, Dynare 6.0 for one appendix; one file fetched at run time |
| Econometrica | zhexiaolin/Estimation-based-on-nearest-neighbor-matching | inputs_available | Shadish application data are confidential; simulations claim about 336 hours and mention GPUs |
| Econometrics Journal | DavBrg/Structural-Forecast-Analysis-Final | free_software | MATLAB; data included in one workbook; README is DOCX/PDF; three absolute paths |
| Econometrics Journal | Paul-Haimerl/replication-fuse-time | free_software | R packages unpinned; MATLAB with CVX for the benchmark; about 48 hours |
| Econometrics Journal | andreaviselli/comparing-predictive-ability-very-short-instability | free_software | MATLAB R2023a; data included; public domain data |
| Econometrics Journal | andreaviselli/robust-fcast-eval-extreme-shocks | free_software | MATLAB R2026a; data included; Econometrics Toolbox for one script |
| Economic Journal | johanneswieland/MPC2001 | free_software | Code downloads BLS, BEA and Philadelphia Fed data at run time; files it creates are not in the package by design |
| Economic Journal | pzoch/demographic-transition-wealth-inequality | free_software | Figure route needs PSID and SCF extracts after registration; full rebuild needs restricted raw files and over 110 GB of bootstrap files |
| JEEA | pmichaillat/pricing-fairness | free_software | MATLAB R2020a and Dynare 4.5.7, both named; figures only |
| JPE | apb-umn/managing-public-portfolios-replication | inputs_available | CRSP returns are a subscription dataset and are not included; other data public, FRED fetched at run time |
| JPE | fediskhakov/EQB | free_software | MATLAB; tabulated data included; one Python notebook with no requirements file |
| JPE | mbholm/Asset-Price-Redistribution | free_software, inputs_available | Statistics Norway registers are confidential; Worldscope is private |
| JPE | mbholm/Transmission-of-Monetary-Policy-under-the-Microscope | free_software, inputs_available | Statistics Norway registers are confidential |
| JPE | pcmichaud/agghealth_replicate | free_software, inputs_available | The data_sources folder the README describes is not in this GitHub copy |
| JPE | ymohanty/rationing-commons | free_software, inputs_available | No data in this repository; the farmer survey holds personal information and needs authorisation |
| JPE | rolf-campos/navigating-replication | free_software | Stata 17, MATLAB R2021b and Python; data included; Python packages unpinned |
| Journal of Finance | lefarmer89/pockets-of-predictability-reply | free_software | Cached results (0.8 GB) and external data (7.8 GB) download from Dropbox; full rerun 10 to 20 hours on 8 cores |
| Journal of Finance | pcmichaud/repl_msa_jf | free_software | Survey data included; Statistics Canada public files to download, one through institutional ODESI access; about 160 hours |
| REStud | LindseyRRay/HiringAsExplorationReplPackage | free_software, inputs_available | Confidential firm personnel data under a data use agreement |
| REStud | floswald/LandUse-REStud | free_software, inputs_available | Development copy without data; its README says it cannot replicate the results |
| REStud | gabrielgggg/DeadlyDebtCrises | free_software | Cleaned data included (some from commercial sources, redistributed in cleaned form); Fortran, Stata and MATLAB; README is a PDF |
| REStud | haanwinckel/HaanwinckelSoares2021 | free_software | Cleaned data at the official Zenodo package; 1991 Census from IBGE on request for one appendix |
| REStud | jblumenstock/migration_networks_replication | inputs_available | Rwanda mobile phone records are private; only sample data are provided |
| REStud | jrblevin/epl-replication | free_software, inputs_available | The application needs Data Axle business data, which the README marks as not provided; Monte Carlo runs are possible |
| REStud | kelloggrk/Public_EndOfOil | inputs_available | intermediate files from a Dropbox folder; this machine's network refuses dropbox.com; Julia downloads also refused |
| REStud | mschwedeler/countryrisk | free_software, inputs_available | No data in the repository; Refinitiv transcripts, Compustat (WRDS), EIU, Markit and MSCI are commercial |
| Journal of Econometrics | ATbounds/ATbounds-replication | target_journal | not a target journal; already rerun (draft PR 16) |
| none named | gabrielgggg/Partial-Default-Replication | target_journal | README names no journal (Kim and Mihalache); strong package otherwise: replay in 1 min, --solve recompute in ~10 h |
| none named | v-asu/multiplexing-and-diffusion-replication-package | target_journal | README names no journal; renv.lock, data included, 15 committed tables |
| none named | ratbekd/myrepo | target_journal | README names no journal |
| Journal of Finance | chenandrewy/mostly-true | inputs_available | data downloaded from Google Drive and Dropbox at run time; Dropbox refused by this machine's network |
| Journal of Finance | bkelly-lab/ReplicationCrisis | free_software, inputs_available | SAS code on WRDS data |

## Limits

- GitHub copies only. A journal's archived package on openICPSR, Zenodo or Dataverse may include data the GitHub copy
  leaves out; this machine cannot reach those archives.
- A machine with Stata and MATLAB would open most of the gated list. The gate is about this machine, not about the packages.
- "Inputs reachable" is about this machine's network on 25 Nov. Dropbox, CRAN and Julia downloads were refused here; a
  GitHub-hosted runner reaches CRAN, which is why the Econometrics Journal rerun runs there.
