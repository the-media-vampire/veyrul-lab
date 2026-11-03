"""Matchering pre-flight checker.

Checks WAV files against conditions that Matchering log codes flag,
before any mastering run. Produces a structured dict per file.
Does NOT install or invoke Matchering.

Source for log-code meanings: art_01M6H98YNPQYY532P86JDMSQ5F revision 1.
License: MIT
"""

import io
import math
import struct
import wave


def preflight_wav(name: str, data: bytes, other_data: bytes | None = None) -> dict:
    """Run pre-flight checks on a WAV file supplied as bytes.

    Parameters
    ----------
    name       : display name used in the output dict
    data       : bytes of the WAV file to check
    other_data : bytes of the *other* file in the pair (target vs reference)
                 used for the same-file identity check (code 4005)

    Returns
    -------
    dict with keys: file, channels, sample_rate_hz, bit_depth, duration_s,
                    peak_norm, warnings, errors, pass
    """
    results = {"file": name, "warnings": [], "errors": []}

    buf = io.BytesIO(data)
    with wave.open(buf, "rb") as wf:
        channels   = wf.getnchannels()
        sampwidth  = wf.getsampwidth()
        framerate  = wf.getframerate()
        n_frames   = wf.getnframes()
        raw        = wf.readframes(n_frames)

    results["channels"]       = channels
    results["sample_rate_hz"] = framerate
    results["bit_depth"]      = sampwidth * 8
    results["duration_s"]     = round(n_frames / framerate, 3)

    # W2203 proxy: flag unexpedted bit depth (not 16 or 24)
    if sampwidth not in (2, 3):
        results["warnings"].append(
            "W2203: unexpected bit depth; verify lossless source"
        )

    # E3001: clipping (any sample at full scale for 16-bit PCM)
    if sampwidth == 2:
        fmt = f"<{n_frames * channels}h"
        samples  = struct.unpack(fmt, raw)
        peak     = max(abs(s) for s in samples)
        peak_norm = peak / 32767.0
        results["peak_norm"] = round(peak_norm, 6)
        if peak >= 32767:
            results["errors"].append(
                "E3001: clipping detected; send version without clipping"
            )
    else:
        results["peak_norm"] = "not_measured"

    # E4005: target and reference are the same file (byte identity)
    if other_data is not None and data == other_data:
        results["errors"].append(
            "E4005: target and reference are the same file"
        )

    # W4002/W4003: length edge flags
    dur = n_frames / framerate
    if dur < 1.0:
        results["warnings"].append("W4002: file shorter than 1 s; check intended length")
    if dur > 3600:
        results["warnings"].append("W4003: file longer than 1 h; check intended length")

    results["pass"] = len(results["errors"]) == 0
    return results