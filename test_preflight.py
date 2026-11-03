"""Synthetic self-test for preflight.py.

Uses stdlib only; no audio files on disk required.
Expected outcomes are deterministic given the synthesis parameters.
"""

import io
import math
import struct
import wave

from preflight import preflight_wav


def _sine_wav(amplitude: float, apply_clip: bool = False,
              freq: int = 440, sr: int = 44100, duration: float = 1.0) -> bytes:
    n = int(sr * duration)
    samples = []
    for i in range(n):
        val = amplitude * math.sin(2 * math.pi * freq * i / sr)
        if apply_clip:
            val = max(-1.0, min(1.0, val * 3.0))
        samples.append(int(val * 32767))
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(struct.pack(f"<{n}h", *samples))
    return buf.getvalue()


def test_clean_passes():
    data = _sine_wav(0.5)
    r = preflight_wav("clean.wav", data)
    assert r["pass"] is True, r["errors"]
    assert r["peak_norm"] < 1.0
    print("PASS test_clean_passes")


def test_clipping_caught():
    data = _sine_wav(0.5, apply_clip=True)
    r = preflight_wav("clipped.wav", data)
    assert r["pass"] is False
    assert any("E3001" in e for e in r["errors"]), r["errors"]
    print("PASS test_clipping_caught")


def test_same_file_caught():
    data = _sine_wav(0.5)
    r = preflight_wav("same.wav", data, other_data=data)
    assert r["pass"] is False
    assert any("E4005" in e for e in r["errors"]), r["errors"]
    print("PASS test_same_file_caught")


def test_different_files_pass():
    a = _sine_wav(0.5)
    b = _sine_wav(0.3)
    r = preflight_wav("ref.wav", b, other_data=a)
    assert r["pass"] is True, r["errors"]
    print("PASS test_different_files_pass")


if __name__ == "__main__":
    test_clean_passes()
    test_clipping_caught()
    test_same_file_caught()
    test_different_files_pass()
    print("All tests passed.")