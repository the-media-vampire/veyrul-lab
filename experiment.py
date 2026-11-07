"""Bark cue-vs-plain experiment script.
Source: art_01M6V77FQTNKYX3ANHPCAT5V9N r1 (not run by Scout; untested)."""
import os, json
os.environ["SUNO_USE_SMALL_MODELS"] = "True"  # set before bark import

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

PRESET = "v2/en_speaker_1"
CONDITIONS = {
    "A_plain": "The lighthouse was empty. Or so everyone said.",
    "B_cued":  "The lighthouse was empty... [sighs] Or so everyone said.",
}
RUNS = 3
LOG = []

preload_models()

for cond, text in CONDITIONS.items():
    for run in range(1, RUNS + 1):
        fname = f"{cond}_run{run}.wav"
        audio = generate_audio(text, history_prompt=PRESET)
        write_wav(fname, SAMPLE_RATE, audio)
        LOG.append({"condition": cond, "run": run, "file": fname,
                    "text": text, "preset": PRESET})
        print(f"Wrote {fname}")

with open("run_log.json", "w") as f:
    json.dump(LOG, f, indent=2)
print("Log written to run_log.json")
# After running: fill in observations in observations.md