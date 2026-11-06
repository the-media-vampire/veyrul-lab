"""measure_onset_delta.py
Tempo Unit Drift: Onset Delta Measurement

Inputs (edit these two paths):
  REFERENCE_WAV  - audio rendered from FoxDot at 120 BPM (Condition A reference)
  TARGET_WAV     - audio rendered from Strudel (Condition A: setcpm 60, or Condition B: setcpm 30)

Output: onset_deltas.csv with columns: bar, ref_onset_s, tgt_onset_s, delta_ms

Requirements: librosa>=0.9, numpy, soundfile
  pip install librosa numpy soundfile

This script does not run a live-coding environment.
It analyses pre-rendered audio files only.
Note: results depend on audio quality and render consistency.
"""
import csv
import sys
try:
    import librosa
    import numpy as np
except ImportError:
    sys.exit("Missing dependency. Run: pip install librosa numpy soundfile")

REFERENCE_WAV = "foxdot_120bpm.wav"   # <-- set your path
TARGET_WAV    = "strudel_cpm60.wav"   # <-- set your path (cpm60 = Condition A)
OUTPUT_CSV    = "onset_deltas.csv"
BARS_TO_CHECK = 8                      # check bars 1-8


def load_onsets(path: str) -> np.ndarray:
    """Return onset times in seconds."""
    y, sr = librosa.load(path, mono=True)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units="frames")
    return librosa.frames_to_time(onset_frames, sr=sr)


def select_bar_onsets(onsets: np.ndarray, n_bars: int) -> list:
    """Take the first n_bars onsets (assumes kick-on-1 pattern)."""
    return list(onsets[:n_bars])


def main():
    print(f"Loading reference: {REFERENCE_WAV}")
    ref_onsets = load_onsets(REFERENCE_WAV)
    print(f"Loading target:    {TARGET_WAV}")
    tgt_onsets = load_onsets(TARGET_WAV)

    n = min(BARS_TO_CHECK, len(ref_onsets), len(tgt_onsets))
    if n < BARS_TO_CHECK:
        print(f"WARNING: Only {n} bars available (wanted {BARS_TO_CHECK}). Check audio length.")

    rows = []
    for i in range(n):
        delta_ms = (tgt_onsets[i] - ref_onsets[i]) * 1000.0
        rows.append({
            "bar":         i + 1,
            "ref_onset_s": round(float(ref_onsets[i]), 6),
            "tgt_onset_s": round(float(tgt_onsets[i]), 6),
            "delta_ms":    round(delta_ms, 2),
        })
        print(f"  Bar {i+1:2d}: ref={ref_onsets[i]:.4f}s  tgt={tgt_onsets[i]:.4f}s  delta={delta_ms:+.2f} ms")

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["bar","ref_onset_s","tgt_onset_s","delta_ms"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWritten: {OUTPUT_CSV}")
    max_drift = max(abs(r["delta_ms"]) for r in rows) if rows else 0
    print(f"Max |delta| across {n} bars: {max_drift:.2f} ms")
    if max_drift < 5:
        print("Result: drift < 5 ms — unit difference may be cosmetic at this tempo.")
    else:
        print("Result: drift >= 5 ms — unit difference is a first-class production concern.")


if __name__ == "__main__":
    main()