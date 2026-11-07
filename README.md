# Bark Cue-vs-Plain Experiment Brief

**Question:** Do Bark's documented sound cues ([sighs], [clears throat]) change
the output prosody relative to identical plain text — or does the model ignore
them unpredictably?

**Source:** art_01M6V77FQTNKYX3ANHPCAT5V9N r1

## Intention
Isolate one variable (cue presence) while holding everything else fixed:
- Same speaker preset (`v2/en_speaker_1`)
- Same seed text
- Same small-model flag
- Same machine / VRAM budget

## Contrasting Alternative
| Condition | Text |
|-----------|------|
| A — plain | "The lighthouse was empty. Or so everyone said." |
| B — cued  | "The lighthouse was empty... [sighs] Or so everyone said." |

Run each condition **three times** (different random seeds) to separate
systematic cue effects from run-to-run variance.

## What to Log (technical observations)
- Did a sigh-like sound appear in condition B but not A?
- Was the pause before "Or" longer in B?
- Were any words dropped or changed? (README warns of unexpected deviations)
- Wall-clock generation time per clip (CPU vs GPU signal)

## Taste judgments (keep separate)
- Which clip felt more natural for a narration context?
- Would you use the cued or plain version in a final cut?

## Discriminating Test
If cues have no systematic effect across the three B runs, the most
informative next step is NOT to tweak the script — it is to try a
different cue ([laughs], [gasps]) or a different preset, to find the
condition where cue behaviour is most consistent.

## Failure modes to record
- Cue rendered as spoken words ("sighs") — note it, do not discard the clip
- Out-of-memory: set SUNO_USE_SMALL_MODELS=True (source-documented)
- Import error after `pip install bark`: reinstall from Suno repo (source-documented)