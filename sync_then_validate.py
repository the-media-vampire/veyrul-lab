"""sync_then_validate.py
Source sample only -- not run, not tested.
Shows the interface join between ffsubsync (subprocess) and pysubs2 (library).
Dependencies: ffsubsync, pysubs2, ffmpeg on PATH.
Provenance: art_01M6N3Y4A4RTHK7PKXE3ZWES7K r2, art_01M6M7RTZQAYHCT8C265GC68C9 r2
"""
import subprocess
import sys
import pathlib
import pysubs2  # type: ignore  # pip install pysubs2

MIN_CUE_MS = 1000   # caption-timing floor (from art_01M5P66MVH8XS2CQPFSHY6AWDT)
MAX_CUE_MS = 7000   # caption-timing ceiling


def sync_subtitles(
    video: str,
    unsynced_srt: str,
    output_srt: str,
    max_offset_seconds: int = 60,
) -> pathlib.Path:
    """Run ffsubsync and return the output path.
    Raises RuntimeError if the process exits non-zero.
    Silent-failure risk: if the true offset > max_offset_seconds the file
    is written but NOT synced; this function cannot detect that case.
    """
    cmd = [
        "ffs", video,
        "-i", unsynced_srt,
        "-o", output_srt,
        f"--max-offset-seconds={max_offset_seconds}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffsubsync failed (exit {result.returncode}):\n{result.stderr}"
        )
    return pathlib.Path(output_srt)


def validate_cue_durations(srt_path: pathlib.Path) -> list[dict]:
    """Load synced SRT with pysubs2 and flag cues outside timing bounds.
    Returns a list of violation dicts; empty list means no violations found.
    This is a documentation check, not a compliance determination.
    """
    subs = pysubs2.load(str(srt_path))
    violations = []
    for i, event in enumerate(subs.events):
        duration_ms = event.end - event.start
        if not (MIN_CUE_MS <= duration_ms <= MAX_CUE_MS):
            violations.append({
                "index": i,
                "start_ms": event.start,
                "end_ms": event.end,
                "duration_ms": duration_ms,
                "text": event.text[:60],
            })
    return violations


if __name__ == "__main__":
    video, raw_srt, out_srt = sys.argv[1], sys.argv[2], sys.argv[3]
    synced = sync_subtitles(video, raw_srt, out_srt)
    issues = validate_cue_durations(synced)
    if issues:
        print(f"{len(issues)} timing violation(s):")
        for v in issues:
            print(f"  cue {v['index']}: {v['duration_ms']} ms — {v['text']}")
    else:
        print("No timing violations found.")