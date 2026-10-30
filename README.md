# Seedance 2.5 multi-cast prompt validator

Static pre-submission checker. Derived from `art_01M669GA8H3XAFN94DM0MG7QC5 r1`.

## Rules checked

| # | Rule | Source section |
|---|---|---|
| 1 | Cast-binding line present (`NAME = @ImageN`) | cast-binding line |
| 2 | Character lock: each name once in action lines per shot | character lock |
| 3 | Unbound ALL-CAPS alias detection | PRINCE/CHARMING bug |
| 4 | Named-object capitalisation (DOOR, STAIRCASE) | wide masters |

## Not checked (not statically verifiable)

Continuity lock, movement rule, dialogue completeness, render output.

## Usage

```bash
python seedance_prompt_check.py
```

```python
from seedance_prompt_check import check_prompt
result = check_prompt("scene", prompt_text, {"ALICE","BOB"})
print(result["issues"])
```

## Design note

Dialogue-attribution lines (`ALICE: "text"`) are stripped before the
character-lock count. Naive counting flags them as duplicates (false
positive caught in first run; corrected in second).

## Limits

Regex-based; extend `STRUCTURAL` for unusual ALL-CAPS vocabulary.
Does not parse nested shot formats. Text check only; no render evidence.