# Survey review: triage v3 on 33 recent journal packages

I pinned 36 author-published packages in [`SURVEY_2026-11-21.json`](../SURVEY_2026-11-21.json) before triage ran on any of them.
None was in the round 2 or round 3 sets. Two were dropped at pinning because no file or description named the journal, and one after
the run because its journal label was wrong (see `corrections` in that file). Each was triaged once with `triage.py` SHA-256
`c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca` and `--have stata,matlab`. That is the same script as round 3,
unchanged. Raw verdicts are in [`survey-2026-11/`](survey-2026-11/).

`--check-links` was not used. The container this ran in refuses most outside hosts through its proxy, so link results there describe
the machine, not the links. For the same reason the journals' own archives (openICPSR, Zenodo, Dataverse) could not be fetched, so
every package is the authors' GitHub copy.

Each verdict was compared with a hand reading of the README, the PDF or DOCX README where that is the only full one, and the files
the findings name. The hand label is a reading, not a run. None of these packages was executed.

## Result

- Verdict agrees: **23 of 33**. Verdict and main reason both right: **17 of 33**.
- Cheap baselines on the same 33: always-runnable-with-deviations **16/33**, always-blocked **14/33**, always-runnable 3/33.
- This is the first held-out set on which triage clearly beats the best cheap guess, by 7 packages. The set is larger than rounds 2
  and 3 (6 each) and drawn differently: these are mostly newer packages, more of them in MATLAB, from journals with data editors.
  The baseline gap may come from the mix of packages as much as from the script.
- **False runnable: 2** (`jrblevin/epl-replication`, `mschwedeler/countryrisk`). For a desk this is the costly error.
- **False blocked: 8.**

| Package | Hand label | Triage | Verdict agrees | Main reason right | What triage got wrong |
|---|---|---|---|---|---|
| akhederlarian/pre-trends-TTBs | blocked | blocked | yes | **no** | Reported 'no code': the do-files are inside zip files in the repository, which triage does not open |
| bela-georgiev/CJE-replication-countryfood | runnable-with-deviations | runnable-with-deviations | yes | **no** | Says Stata packages are installed from the network; they are bundled in the package |
| ekrose/rss_rep | blocked | blocked | yes | yes | - |
| rsaggio87/Replication_DKSS | blocked | blocked | yes | **no** | Cited test files of a bundled MATLAB library as missing; did not name the restricted data |
| tholden/RobustRealRateRulesReplication | runnable-with-deviations | runnable-with-deviations | yes | yes | - |
| zhexiaolin/Estimation-based-on-nearest-neighbor-matching | blocked | blocked | yes | yes | Also listed simulation outputs as missing inputs |
| DavBrg/Structural-Forecast-Analysis-Final | runnable-with-deviations | runnable-with-deviations | yes | yes | Said there is no run order; Main_RunAll.m exists and the PDF README names it |
| InsIDE-Lab-DiECO/permanent-transitory-decomposition-replication | runnable-with-deviations | blocked | **no** | **no** | Did not recognise gretl scripts (.inp) and reported 'no code' |
| Paul-Haimerl/replication-fuse-time | runnable-with-deviations | blocked | **no** | **no** | Read intermediate outputs, which the package regenerates, as missing inputs |
| andreaviselli/comparing-predictive-ability-very-short-instability | runnable | runnable | yes | yes | - |
| andreaviselli/robust-fcast-eval-extreme-shocks | runnable | runnable | yes | yes | Did not mention the Econometrics Toolbox |
| timmy-o-toole/Assemblage_VAR | runnable-with-deviations | runnable-with-deviations | yes | yes | Reported a claimed run time of 422,640 hours with no source sentence |
| johanneswieland/MPC2001 | runnable-with-deviations | blocked | **no** | **no** | Read files the pipeline downloads or creates as missing inputs |
| pzoch/demographic-transition-wealth-inequality | runnable-with-deviations | blocked | **no** | **no** | Read model output files as missing inputs, and read a line-ending string as a file name |
| pmichaillat/pricing-fairness | runnable | runnable | yes | yes | - |
| apb-umn/managing-public-portfolios-replication | blocked | blocked | yes | yes | - |
| chrisconlon/Liquor_Replication_JPE | runnable-with-deviations | blocked | **no** | **no** | Blocked on NielsenIQ-derived files that entry point 2 does not need |
| fediskhakov/EQB | runnable-with-deviations | runnable-with-deviations | yes | yes | - |
| mbholm/Asset-Price-Redistribution | blocked | blocked | yes | **no** | Said the README gives no source; the README is a PDF triage cannot read, and it names the sources |
| mbholm/Transmission-of-Monetary-Policy-under-the-Microscope | blocked | blocked | yes | **no** | Same PDF README problem |
| pcmichaud/agghealth_replicate | blocked | blocked | yes | yes | The journal's archive copy may include it; not checked |
| ymohanty/rationing-commons | blocked | blocked | yes | yes | - |
| rolf-campos/navigating-replication | runnable-with-deviations | runnable-with-deviations | yes | yes | - |
| lefarmer89/pockets-of-predictability-reply | runnable-with-deviations | blocked | **no** | **no** | Read cached results as missing inputs and did not link them to the Dropbox archive |
| pcmichaud/repl_msa_jf | runnable-with-deviations | blocked | **no** | **no** | Read model estimates the code writes as missing inputs |
| LindseyRRay/HiringAsExplorationReplPackage | blocked | blocked | yes | yes | - |
| floswald/LandUse-REStud | blocked | blocked | yes | yes | - |
| gabrielgggg/DeadlyDebtCrises | runnable-with-deviations | blocked | **no** | **no** | Read a tab character as a missing file name |
| haanwinckel/HaanwinckelSoares2021 | runnable-with-deviations | runnable-with-deviations | yes | **no** | Did not flag the Zenodo download; cited only the Stata version and paths |
| jblumenstock/migration_networks_replication | blocked | blocked | yes | yes | - |
| jrblevin/epl-replication | blocked | runnable-with-deviations | **no** | **no** | Missed the README's 'Provided: False' row and called the package runnable |
| kelloggrk/Public_EndOfOil | runnable-with-deviations | runnable-with-deviations | yes | yes | Did not flag the Dropbox download |
| mschwedeler/countryrisk | blocked | runnable-with-deviations | **no** | **no** | Called it runnable and said every traced input is present; the data folder holds code only |

## Failures, left as found

These were not fixed in this pull request, by the rule written in `SURVEY_2026-11-21.json` before the run.

1. **Pipeline outputs and downloads read as missing inputs** (Haimerl et al., Michaud and St-Amour, Farmer et al., Orchard et al.,
   Makarski et al.). This is still the largest cause of false "blocked" verdicts, as in rounds 2 and 3.
2. **Control characters read as file names.** A `\t` (Arellano et al.) and a `\r\n` (Makarski et al.) were reported as missing input
   files. One of them is the only blocker on a package that can run.
3. **gretl not recognised.** `.inp` scripts are not a known language, so Casoli and Lucchetti got `NO_CODE`.
4. **Code inside zip files not opened.** Khederlarian and Steinbach keep their do-files in `do-files.zip`. The verdict happened to be
   right, for a different reason.
5. **README data tables not read.** Dearing and Blevins' README table marks Data Axle as `Provided: False`. Triage missed it and
   called the package runnable.
6. **"Every traced input is present" when no data file exists.** Hassan et al. hold only code. Their inputs are reached through a
   `config.yaml` that triage does not resolve: all 94 reads it found were unresolved paths. It reported nothing missing and called the package runnable. This is the worst error in
   the set.
7. **PDF READMEs still unread** (both Statistics Norway packages). This is round 3 failure 2, unchanged.
8. **Bundled Stata packages reported as network installs** (Georgiev and Li bundle `ado/plus`).
9. **LONG_COMPUTE of 422,640 hours with no source sentence** (Barrette et al.). This is round 3 failure 4, unchanged.

## What would change the verdict next time

Round 4 starts as before. Write one injection per failure above, freeze it, then make the fix. These 33 are now development cases, so
a new held-out set is needed after the fix. The numbers to beat are 23/33 for the verdict, against a best cheap guess of 16/33, and
17/33 for the reason.
