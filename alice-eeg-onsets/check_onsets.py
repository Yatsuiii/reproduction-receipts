"""Check NEMAR nm000180 word onsets against the story audio recorded in each EEG file. See PROTOCOL.md.

usage: python check_onsets.py <clone_dir> <data_dir> <out_dir>
  clone_dir: git clone of nm000180 (events.tsv, channels.tsv live in git)
  data_dir:  annexed files fetched by fetch.py (same relative paths)
"""
import json
import os
import re
import sys

import mne
import numpy as np
import pandas as pd
from scipy.io import loadmat, wavfile
from scipy.signal import butter, fftconvolve, resample_poly, sosfiltfilt

FS = 500
TEMPLATE_S = 30.0  # first 30 s of each segment, so a segment cut off by the end of a recording can still be placed
FINE_MS = 50
SOS_BAND = butter(4, [70, 200], btype="band", fs=FS, output="sos")
SOS_ENV = butter(4, 20, btype="low", fs=FS, output="sos")


def band(x):
    return sosfiltfilt(SOS_BAND, x - np.mean(x))


def env(xb):
    return np.sqrt(np.maximum(sosfiltfilt(SOS_ENV, xb ** 2), 0))


def ncc(sig, tmpl):
    """Normalised cross-correlation of tmpl at every valid lag of sig (Pearson r per lag)."""
    L = len(tmpl)
    t = (tmpl - tmpl.mean()) / (tmpl.std() * L)
    num = fftconvolve(sig, t[::-1], mode="valid")
    c1 = np.concatenate([[0], np.cumsum(sig)])
    c2 = np.concatenate([[0], np.cumsum(sig ** 2)])
    m = (c1[L:] - c1[:-L]) / L
    v = (c2[L:] - c2[:-L]) / L - m ** 2
    return num / np.sqrt(np.maximum(v, 1e-30))


def place(aud_b, aud_e, wav_b, wav_e):
    r = ncc(aud_e, wav_e)
    best = int(np.argmax(r))
    masked = r.copy()
    masked[max(0, best - 2 * FS): best + 2 * FS + 1] = -np.inf
    second = float(np.max(masked)) if np.isfinite(masked).any() else float("nan")
    w = FINE_MS * FS // 1000
    lo, hi = max(0, best - w), min(len(aud_b) - len(wav_b), best + w)
    rf = ncc(aud_b[lo: hi + len(wav_b)], wav_b)
    fine = lo + int(np.argmax(np.abs(rf)))
    return best, float(r[best]), second, fine, float(rf[fine - lo])


def verdict(res_ms, r_env, ratio):
    if not np.isfinite(res_ms) or r_env < 0.2 or ratio >= 0.8:
        return "undetermined"
    a = abs(res_ms)
    return "consistent" if a <= 10 else "small offset" if a <= 50 else "mismatch"


def main():
    clone, data, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)

    story = pd.read_csv(os.path.join(data, "sourcedata/AliceChapterOne-EEG.csv"))
    print("CSV columns:", list(story.columns))
    print(story.head(3).to_string())
    oc = "onset" if "onset" in story.columns else [c for c in story.columns if "onset" in c.lower()][0]
    print("in-segment onset column used:", oc)
    story = story.set_index("Order")

    wavs = {}
    for k in range(1, 13):
        sr, x = wavfile.read(os.path.join(data, f"stimuli/DownTheRabbitHoleFinal_SoundFile{k}.wav"))
        x = x.astype(float)
        if x.ndim > 1:
            x = x.mean(axis=1)
        g = np.gcd(FS, sr)
        xb = band(resample_poly(x, FS // g, sr // g))
        n = int(TEMPLATE_S * FS)
        wavs[k] = (xb[:n], env(xb)[:n], len(x) / sr)
        print(f"segment {k}: {sr} Hz, {len(x) / sr:.3f} s", flush=True)

    rows, rebuild = [], []
    subs = sorted(d for d in os.listdir(clone) if re.fullmatch(r"sub-\d+", d))
    for sub in subs:
        evf = os.path.join(clone, sub, "eeg", f"{sub}_task-alicelistening_events.tsv")
        if not os.path.exists(evf):
            print(f"{sub}: no events.tsv in the release, skipped", flush=True)
            continue
        ev = pd.read_csv(evf, sep="\t")

        # check 1: rebuild onsets from proc .mat
        sxx = "S%02d" % int(sub.split("-")[1])
        matf = os.path.join(data, "sourcedata/proc", f"{sxx}.mat")
        if os.path.exists(matf):
            p = loadmat(matf, squeeze_me=True, struct_as_record=True, simplify_cells=True)["proc"]
            trl = np.asarray(p["trl"], dtype=float)
            cols = ["start", "stop", "offset"] + list(p["varnames"])
            t = pd.DataFrame(trl, columns=cols[: trl.shape[1]])
            t = pd.DataFrame({"word_index": t["Order"].astype(int), "rebuilt": (t["start"] - t["offset"]) / FS})
            m = ev.merge(t, on="word_index", how="outer", indicator=True)
            both = m["_merge"] == "both"
            d = (m.loc[both, "onset"] - m.loc[both, "rebuilt"]).abs()
            rebuild.append({"subject": sub, "n_events": len(ev), "n_trl": len(t), "n_matched": int(both.sum()),
                            "max_abs_diff_ms": float(d.max() * 1000) if len(d) else float("nan")})
        else:
            rebuild.append({"subject": sub, "n_events": len(ev), "n_trl": 0, "n_matched": 0,
                            "max_abs_diff_ms": float("nan")})

        # checks 2-4
        vhdr = os.path.join(data, sub, "eeg", f"{sub}_task-alicelistening_eeg.vhdr")
        raw = mne.io.read_raw_brainvision(vhdr, preload=False, verbose="error")
        assert raw.info["sfreq"] == FS, raw.info["sfreq"]
        ch = [c for c in raw.ch_names if c in ("AUD", "Aux5")]
        assert len(ch) == 1, raw.ch_names[-4:]
        aud = raw.get_data(picks=ch)[0]
        aud_b = band(aud)
        aud_e = env(aud_b)
        rec_s = len(aud) / FS

        ev["csv_onset"] = story.loc[ev["word_index"], oc].values
        ev["implied"] = ev["onset"] - ev["csv_onset"]
        for k, g in ev.groupby("segment"):
            wb, we, wav_s = wavs[int(k)]
            imp = g["implied"].median()
            best, r_env, second, fine, r_fine = place(aud_b, aud_e, wb, we)
            res = (imp - fine / FS) * 1000
            ratio = second / r_env if r_env > 0 else float("inf")
            rows.append({"subject": sub, "channel": ch[0], "segment": int(k), "n_words": len(g),
                         "implied_start_s": round(imp, 4),
                         "implied_spread_ms": round((g["implied"].max() - g["implied"].min()) * 1000, 3),
                         "measured_env_s": best / FS, "measured_fine_s": fine / FS,
                         "r_env": round(r_env, 4), "second_peak_ratio": round(ratio, 4), "r_fine": round(r_fine, 4),
                         "residual_ms": round(res, 3), "verdict": verdict(res, r_env, ratio),
                         "recording_s": rec_s, "segment_audio_s": round(wav_s, 3)})
            print(f"{sub} seg {int(k):2d}: implied {imp:8.3f}s measured {fine / FS:8.3f}s "
                  f"residual {res:8.1f} ms r_env {r_env:.3f} ratio {ratio:.2f} -> {rows[-1]['verdict']}", flush=True)

    seg = pd.DataFrame(rows)
    determined = seg["verdict"] != "undetermined"
    const = float(seg.loc[determined, "residual_ms"].median()) if determined.any() else float("nan")
    seg["residual_minus_constant_ms"] = (seg["residual_ms"] - const).round(3)
    seg["verdict_after_constant"] = [verdict(r, e, q) for r, e, q in
                                     zip(seg["residual_minus_constant_ms"], seg["r_env"], seg["second_peak_ratio"])]
    seg.to_csv(os.path.join(out, "per_segment.csv"), index=False)
    pd.DataFrame(rebuild).to_csv(os.path.join(out, "rebuild.csv"), index=False)

    summary = {
        "subjects_checked": int(seg["subject"].nunique()),
        "segments_checked": int(len(seg)),
        "verdicts": seg["verdict"].value_counts().to_dict(),
        "constant_residual_ms_median": const,
        "verdicts_after_constant": seg["verdict_after_constant"].value_counts().to_dict(),
        "residual_minus_constant_ms_abs_max": float(seg.loc[determined, "residual_minus_constant_ms"].abs().max()),
        "implied_spread_ms_max": float(seg["implied_spread_ms"].max()),
        "rebuild_max_abs_diff_ms": float(pd.DataFrame(rebuild)["max_abs_diff_ms"].max()),
        "versions": {"mne": mne.__version__, "numpy": np.__version__, "pandas": pd.__version__,
                     "python": sys.version.split()[0]},
    }
    with open(os.path.join(out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
