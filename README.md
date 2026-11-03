# Matchering Pre-flight Checker

A stdlib-only Python 3 module that checks WAV files against the conditions
documented in the **Matchering log-code table**
(source: `art_01M6H98YNPQYY532P86JDMSQ5F` revision 1, Veyrul)
before any mastering run begins.

## What it checks

| Check | Mapped log code | What it catches |
|---|---|---|
| Bit depth not 16 or 24 | W2203 proxy | Likely lossy or unusual format |
| Peak sample at full scale | E3001 | Clipping in the target file |
| Target == reference (byte identity) | E4005 | Same file passed as both inputs |
| Duration < 1 s | W4002 | Unexpectedly short file |
| Duration > 1 h | W4003 | Unexpectedly long file |

**Not checked here:** limiter detection (E3002), channel-count limits (E4004),
and the LUFS/true-peak delivery comparison — those require a separate meter
and the linked delivery records (`art_01M6F4359J1K2K4VP3R35TQX7Q`,
`art_01M5MSDHZRM272BANY4V98B48X`).

## Usage

```python
from preflight import preflight_wav

with open("target.wav", "rb") as f: target = f.read()
with open("ref_A.wav",   "rb") as f: ref_a  = f.read()

print(preflight_wav("target.wav", target, other_data=ref_a))
print(preflight_wav("ref_A.wav",  ref_a,  other_data=target))
```

## Running the self-test

```
python test_preflight.py
```

All four test cases use synthesised data; no audio files on disk required.

## Scope

This script does **not** run, wrap or require Matchering. It prepares inputs
so that avoidable Matchering errors are caught before the run. Limiter
detection (code 3002) requires signal-analysis beyond peak inspection and
is out of scope here — flag it as a human step.

## License

MIT — see LICENSE.