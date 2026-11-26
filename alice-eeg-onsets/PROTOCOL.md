# Protocol: do the word onsets in NEMAR nm000180 sit where the story audio is?

Written and committed before any EEG file was downloaded or any check was run.

## Why this check

NEMAR re-released the Brennan & Hale (2019) Alice in Wonderland EEG as a BIDS dataset,
[nemarDatasets/nm000180](https://github.com/nemarDatasets/nm000180). Its README says the 12 segment triggers are
not in the re-hosted `.vmrk` files, so every word onset in `*_events.tsv` was rebuilt from the original per-subject
preprocessing files (`sourcedata/proc/SXX.mat`, `onset = (start_sample - offset) / 500`). Nothing in the release
checks those rebuilt onsets against the recording itself.

Each recording has a channel (`AUD`, or `Aux5` for sub-001) that holds a digitised copy of what the listener heard.
So the onsets can be checked against the EEG file directly: if the story audio for segment *k* starts at time *T* in
the recording, every word of segment *k* should sit at *T* plus its position inside the segment's audio file.

## What is pinned

- Dataset: `https://github.com/nemarDatasets/nm000180`, commit `e37db55b334496f1602489963f94f354012ba580`
  (main, 21 Oct 2026). Every annexed file is fetched from the dataset's public S3 remote
  (`https://nemar.s3.us-east-2.amazonaws.com/nm000180/objects/<key>`) and its SHA-256 is checked against the
  git-annex key before use. A file whose hash does not match is not used.
- Software: Python 3.12 on a GitHub-hosted `ubuntu-24.04` runner, `mne==1.10.2`, `scipy==1.16.3`,
  `numpy==2.3.5`, `pandas==2.3.3`. Nothing else is installed.

## Checks

1. **Rebuild.** Recompute each subject's onsets from `sourcedata/proc/SXX.mat` with the formula in the README and
   compare with `events.tsv`, word by word. This only checks the conversion script did what it says.
2. **Implied segment start.** For each subject and segment, `events.tsv onset - CSV onset` for every word in that
   segment, where the CSV onset is the word's time inside its segment's audio file
   (`sourcedata/AliceChapterOne-EEG.csv`). Report the median and the spread (max minus min). If the CSV onset turns
   out not to be segment-relative, this shows up as a large spread and is reported, not patched.
3. **Measured segment start.** Both the first 30 s of the segment's `.wav` (resampled to 500 Hz; 30 s so that a
   segment cut off by the end of a recording can still be placed) and the recorded audio channel are
   band-passed 70 to 200 Hz, and their amplitude envelopes (low-passed at 20 Hz) are cross-correlated over the whole
   recording. The best lag is the measured start, refined to one sample by cross-correlating the band-passed signals
   themselves within ±50 ms. Peak correlation and the ratio of the best peak to the best peak more than 2 s away are
   reported.
4. **Residual** = implied start minus measured start, in ms.

## Decision rule, fixed now

- Audio not found: envelope peak correlation below 0.2, or second peak at least 0.8 of the best. Reported as
  "undetermined", never as a pass or a fail.
- |residual| ≤ 10 ms (5 samples): consistent.
- 10 < |residual| ≤ 50 ms: small offset.
- |residual| > 50 ms: mismatch.

One known complication, stated before looking: the original onsets were computed from the segment triggers, and a
sound card can play audio a fixed few ms to tens of ms after its trigger. A residual that is **the same for every
subject and segment** is most likely that hardware latency, already present in the 2019 analysis, and is not a
conversion error. A residual that **varies between subjects or segments** is the thing this check is looking for.
The receipt will report both the constant part (median over all segments) and the variation around it.

## What this does not check

It does not rerun any analysis from the paper, and it does not check the linguistic predictors. It says nothing
about whether the paper is right.
