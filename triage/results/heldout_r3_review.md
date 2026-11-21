# Held-out review, round 3: triage v3 on six new journal packages

I pinned six author-published packages in [`HELDOUT_R3.json`](../HELDOUT_R3.json) before triage ran on any of them. None of them was
in the round 2 set. One journal label in that file was wrong at pinning and is corrected there, with a note. Each was triaged once with `triage.py` SHA-256
`c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`, options `--have stata,matlab --check-links`. Each verdict was then
compared with a hand reading of the package's README, the PDF where the README is a PDF, and the files the findings name. The hand
label is a reading, not a run: none of these packages was executed. Raw verdicts are in [`heldout-r3/`](heldout-r3/). The run was on
2026-11-21 from the same cloud container as round 2 (HTTPS through a proxy only).

## Result

| Package | Journal | Hand label | Triage | Verdict agrees | Main reason right |
|---|---|---|---|---|---|
| Caselli, Koren, Lisicky, Tenreyro, diversification through trade | QJE | runnable with deviations: Julia 0.6.4, no Manifest, WDI download | blocked | **no** | no |
| de Silva, income-contingent student loans | QJE | blocked: four private Australian datasets (ALife, ATO, Census via DataLab, HILDA) | blocked | yes | **no** |
| Arcidiacono, Aucejo, Maurel, Ransom, college attrition | JPE | runnable with deviations, **uncertain**: NLSY97 and SIPP downloads; NPSAS confidential, used only for auxiliary coefficients; over two weeks of compute | blocked | **no** | no |
| Fagereng, Holm, Natvik, MPC heterogeneity | AEJ: Macro | blocked: confidential Statistics Norway registers | blocked | yes | **no** |
| Card, Rothstein, Yi, location | AEJ: Applied | blocked: confidential LEHD inside the Census Bureau only; SAS | blocked | yes | yes |
| Koren, Tenreyro, volatility and development | QJE | runnable with deviations: data in Git LFS, Stata version only in README | runnable with deviations | yes | yes |

- Verdict agrees: **4 of 6**. Verdict and main reason both right: **2 of 6**.
- Cheap baselines on the same six: always-blocked **3/6**, always-runnable 0/6, readme-and-code 0/6.
- Triage beats the best cheap baseline by one package. Its stated reason was right in two of six, which is worse than the three of six in
  round 2. I would not call this an improvement in reasons. What improved is the claims it no longer makes (next section).
- The Dropout-JPE label is uncertain. If it is really blocked, the counts become 5/6 for the verdict and 4/6 for always-blocked.

## Round 2 failures, checked on this new set

- **Proxy refusals reported as dead links:** fixed. No `DEAD_DATA_LINK` was raised on any of the six. Card, Rothstein and Yi's Census URL,
  refused by this container's proxy, is reported as `DATA_LINK_UNREACHABLE`, with a note that this is evidence about this machine's
  network, not about the link.
- **Generated outputs read as missing inputs:** still happens. The cause is different this time (failures 1 and 3 below).
- **Software missed:** none missed on this set. SAS was caught (Card, Rothstein, Yi).

## New failures, left as found

These were not fixed in this pull request, by the rule written in `HELDOUT_R3.json` before the run.

1. **Julia `jldopen(path, "w")` treated as a read (Caselli et al.).** `jldopen` is in the read table regardless of mode, so
   `results.jld2`, which the code writes, was reported as a missing input. This is the only blocker, and it makes the verdict wrong.
2. **Unreadable README reported as silence (de Silva; Fagereng, Holm, Natvik).** Both READMEs are a PDF or LyX file. Triage said so in a
   `README_NOT_TEXT` note. Its blockers then said the documentation "does not say where it comes from", when in fact it does: the data
   are private. The verdict is right, but the stated reason claims something triage could not read.
3. **Earlier pipeline outputs labelled restricted (Arcidiacono et al.).** Twenty files under `../../output/` that later estimation
   stages read were called restricted because the README mentions confidential data somewhere. The README-wide restricted fallback
   is too broad.
4. **`LONG_COMPUTE` of 27 hours on Caselli et al. not traced to a sentence.** The finding gives no evidence line, so I could not check it.
   A finding must name its source.

## What would change the verdict next time

Round 4 starts the same way: one injection per failure above, written before the fix and frozen, then the fix, then a new held-out
set. These six packages are now development cases. The two numbers to beat are 4/6 for the verdict against an always-blocked 3/6,
and 2/6 for the reason.
