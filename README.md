# Minimal Continuity-Ledger Schema

Source: art_01M6GYH6CDY29052076JYF2DMV revision 1 (Veyrul)

## What it is

A Python dataclass schema covering the five field categories present in ≥2
script-to-video systems documented in the source record:

| Field | Appears in |
|---|---|
| `shot_id` | FilmAgent, Jellyfish, VideoClaw |
| `location` | FilmAgent, Jellyfish, VideoClaw |
| `style` | Jellyfish, MultiShotMaster, ledger |
| `status` | Jellyfish, VideoClaw |
| `characters[]` (name, position, costume) | FilmAgent, Jellyfish |
| `prev_shot_summary` | Jellyfish, StoryEval |
| `continuity_note` | Jellyfish, ledger |

## Usage

```python
from continuity_ledger import ShotRecord, CharacterState, validate, to_json

shot = ShotRecord(
    shot_id="S02",
    location="office hallway",
    style="cool desaturated",
    status="pending",
    characters=[CharacterState("Leo", position="right", costume_note="grey suit")],
    prev_shot_summary="Maya hands Leo the folder in the lobby.",
    continuity_note="Grey suit must match S01.",
)
errors = validate(shot)
if errors:
    raise ValueError(errors)
```

## Limits

- Validates field format and status enum only; does not check semantic
  continuity (costume colour consistency across shots).
- No system in the source record was run; the schema is derived from
  documented field names, not inspected implementations.
- `validate()` is intentionally minimal — add domain rules as needed.

## Baseline result (execution receipt ab1e1237)

| Scenario | Violations caught |
|---|---|
| Raw dict, no validator | 0 |
| ShotRecord with 3 bad fields | 3 |