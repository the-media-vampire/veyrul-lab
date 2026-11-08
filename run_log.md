# Run log — fill in before watching any output

## Environment

- FFmpeg version: (copy from ffmpeg-version.txt)
- Input file: (sha256 of input.mp4)
- Input dimensions/fps/pix_fmt: (copy from input-probe.txt)
- Date/time of run: (record at time of execution)

## Per-arm results

For each arm, record exit code and stderr summary before playback.

### control
- Exit code:
- Stderr (errors only):
- Output file size (bytes):

### short (s=5)
- Exit code:
- Stderr (errors only):
- Output file size (bytes):

### long (s=17)
- Exit code:
- Stderr (errors only):
- Output file size (bytes):

### scout_0b (0b=0.12)
- Exit code:
- Stderr (errors only):
- Output file size (bytes):

## Verification

All four arms must exit 0 and produce non-zero output before proceeding to inspection.
If any arm fails, record the diagnostic from diagnostics.md and stop.