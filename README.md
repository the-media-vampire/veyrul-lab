# Twelve-Block Compliance Log

Companion to Theo's TwelveBlockPrompt adapter (artifact 8077bea7).
That adapter validates authoring gaps. This package records *observed outcomes*:
which clauses the model honoured, which it did not, and which cannot be judged from stills.

## Files
- `compliance_log_schema.json` — JSON Schema for one clip's inspection log
- `compliance_log_example.json` — filled example from art_01M67CGQR5M8AXXN18VH6Z4ETM r1 (18s clip)
- `summarise.py` — prints verdict counts and mismatch list from a log file

## Verdict vocabulary
| Verdict | Meaning |
|---|---|
| match | Stills confirm the clause |
| mismatch | Stills contradict the clause |
| unverifiable | Cannot judge from stills (motion/audio/full orbit) |
| open_call | Lane disagreement; conservative label applied |

## Key assumption (inherited from source record)
Model compliance with written continuity sentences is **untested by any validator**.
Mismatches here are observed outcomes, not authoring errors.
Authoring errors are what the companion adapter catches.

## Source
art_01M67CGQR5M8AXXN18VH6Z4ETM r1 (Veyrul, 2026-10-30). Stills inspected;
playback and audio not done. 23 stills, 2 lanes.