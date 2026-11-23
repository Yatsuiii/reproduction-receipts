"""Exploratory follow-up, written AFTER the first run's results were seen (not part of the pre-registered protocol).

Two questions the first run raised:
1. Segment 1 could not be placed for nine subjects. Is that because the recording started after segment 1 began?
   Place the LAST 20 s of every segment's audio too, which is inside the recording even if its start is not.
2. Five subjects gave no usable audio match. What does their audio channel contain?

usage: python diag_tails.py <clone_dir> <data_dir> <out_dir>
"""
import os
import re
import sys

import mne
import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import resample_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_onsets import FS, band, env, place  # noqa: E402

TAIL_S = 20.0


def main():
    clone, data, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    story = pd.read_csv(os.path.join(data, "sourcedata/AliceChapterOne-EEG.csv")).set_index("Order")
    tails = {}
    for k in range(1, 13):
        sr, x = wavfile.read(os.path.join(data, f"stimuli/DownTheRabbitHoleFinal_SoundFile{k}.wav"))
        x = x.astype(float)
        x = x.mean(axis=1) if x.ndim > 1 else x
        g = np.gcd(FS, sr)
        xb = band(resample_poly(x, FS // g, sr // g))
        n = int(TAIL_S * FS)
        tails[k] = (xb[-n:], env(xb)[-n:], (len(xb) - n) / FS)  # offset of the tail inside the segment, s

    rows, chans = [], []
    for sub in sorted(d for d in os.listdir(clone) if re.fullmatch(r"sub-\d+", d)):
        vhdr = os.path.join(data, sub, "eeg", f"{sub}_task-alicelistening_eeg.vhdr")
        raw = mne.io.read_raw_brainvision(vhdr, preload=False, verbose="error")
        ch = [c for c in raw.ch_names if c in ("AUD", "Aux5")][0]
        aud = raw.get_data(picks=[ch])[0]
        ab = band(aud)
        chans.append({"subject": sub, "channel": ch, "raw_std": float(np.std(aud)), "raw_ptp": float(np.ptp(aud)),
                      "band_std": float(np.std(ab)), "n_unique_values": int(len(np.unique(aud[: 50 * FS])))})
        evf = os.path.join(clone, sub, "eeg", f"{sub}_task-alicelistening_events.tsv")
        if not os.path.exists(evf):
            continue
        ev = pd.read_csv(evf, sep="\t")
        ev["implied"] = ev["onset"] - story.loc[ev["word_index"], "onset"].values
        ae = env(ab)
        for k in range(1, 13):
            wb, we, off = tails[k]
            best, r_env, second, fine, r_fine = place(ab, ae, wb, we)
            seg_start_from_tail = fine / FS - off
            g = ev[ev["segment"] == k]
            imp = g["implied"].median() if len(g) else np.nan
            rows.append({"subject": sub, "segment": k, "has_events": len(g) > 0, "implied_start_s": imp,
                         "start_from_tail_s": round(seg_start_from_tail, 4), "r_env_tail": round(r_env, 4),
                         "second_peak_ratio_tail": round(second / r_env if r_env > 0 else np.inf, 4),
                         "residual_tail_ms": round((imp - seg_start_from_tail) * 1000, 3) if len(g) else np.nan})
    pd.DataFrame(rows).to_csv(os.path.join(out, "tails.csv"), index=False)
    pd.DataFrame(chans).to_csv(os.path.join(out, "audio_channel.csv"), index=False)


if __name__ == "__main__":
    main()
