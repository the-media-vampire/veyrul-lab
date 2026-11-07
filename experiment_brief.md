# Experiment Brief: CITATION.cff Validation Contrast

## Intention
Test whether cffconvert's validation error message is informative enough to
guide a first-time user to the specific broken field, using the README's own
validation instructions (art_01M6Q7SK1QKYS9DQMRV9MMB0GJ r1, lines 67-84).

## Contrasting alternatives
| | File A (valid) | File B (invalid) |
|---|---|---|
| cff-version | 1.2.0 ✓ | absent ✗ |
| message | present | present |
| title | present | present |
| authors | present | present |

## Discriminating test
Run both through cffconvert on the command line:

```bash
pip install --user cffconvert
cffconvert --validate -i file_a_valid.cff
cffconvert --validate -i file_b_missing_cff_version.cff
```

## What would change our mind
- If File B passes: the validator does not enforce cff-version as required.
  That would contradict the schema's stated required fields.
- If File A fails: the minimal field set listed here is not sufficient;
  another required field was missed.
- If the error message for File B names a field other than cff-version:
  the validator's error path may be indirect and less guiding than hoped.

## Technical observations to record separately from taste
- Exact error class and message string from cffconvert Traceback (File B)
- Whether 'validation error' lines are searchable as README promises
- Exit codes (0 vs. non-zero) for scripted CI use

## Source
All field choices derived from art_01M6Q7SK1QKYS9DQMRV9MMB0GJ revision 1
(README lines 14-36 and 67-84). Not executed; documented-not-tested.