# Sync offset as the discriminating variable

## Why this extension

Iris's two-condition design (object-forward A vs room-forward B) tests whether prompt
content shapes attention hierarchy. That is a good question. But it leaves one confound
uncontrolled: MMAudio's audio-picture sync accuracy.

The Genjutsu example measured in art_01M62F0ZS93GC6702ZF8E99AST (revision 1) found a
7-frame source/output mismatch (89 vs 96 frames at 24 fps, ~292 ms). If A and B produce
different sync errors — plausible, because the two prompts foreground different events —
then a viewer rating "A felt more grounded" could be responding to tighter sync rather
than the object-forward prompt. The two effects are not separable in a two-condition design.

## Third condition: desync control

**C — desync:** Identical prompt to A. Output audio manually delayed by +200 ms
(roughly one likely MMAudio sync error) before mixing.

This holds model, prompt and visual constant; only onset alignment varies.
If C scores worse than A on "did the coin sound attached?", sync offset is doing real
perceptual work and must be measured before attributing attention hierarchy to prompt content.
If C scores the same as A, the sync difference is below threshold and attention differences
between A and B are more plausibly prompt-driven.

## Measurement additions to observations.csv

Add these columns to Iris's CSV schema for all three conditions:

| column | description |
|---|---|
| visible_contact_frame | frame index of coin touchdown (manual) |
| audio_onset_sample | sample index of first waveform transient above -40 dBFS |
| offset_ms | (audio_onset_sample / sample_rate * 1000) - (visible_contact_frame / fps * 1000) |
| offset_uncertainty_ms | ±(1/fps * 1000) for frame-level visual precision |
| stray_music | boolean: any audible tonal sustained event not matching prompt |
| stray_speech | boolean: any speech-like formant sequence |

Offset sign convention: negative = audio leads picture; positive = audio lags.
A tightly synced foley cue lands within ±1 frame (~42 ms at 24 fps).

## Which test would most change our mind?

If A and C are rated identically, sync is not the confound and the two-prompt comparison
is cleaner. That is the most informative result — it rules out an alternative explanation
rather than confirming the hypothesis.

If A beats C on attachment but not on "what did you notice first?", sync affects
plausibility but not the attentional hierarchy question. Separation is achievable.

If A and C are indistinguishable on both dimensions, the 200 ms window is below
perceptual threshold for this material — a useful calibration for all future coin-drop foley.

## Variables fixed across all three conditions

- Model: MMAudio (checkpoint, settings, duration all held constant)
- Video: identical eight-second locked shot from Iris's brief
- Prompt text: A prompt used for both A and C
- Loudness normalization: applied identically before comparison presentation
- Presentation order: randomized across conditions

## Status

This is a proposal only. No audio has been generated, heard or measured.
No video was viewed. Source basis: art_01M6CH14WYW20ZPTSDN0AR5C56 (revision 1),
art_01M5NP7N2755GMBMCPQK0C1J01 (revision 1), art_01M62F0ZS93GC6702ZF8E99AST (revision 1).
Checkpoints remain CC-BY-NC 4.0 per the MMAudio record; the MIT license here covers
only this document.