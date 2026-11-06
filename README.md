# FxNorm-Automix Setup Discriminator

Experiment brief for evaluating FxNorm-Automix inference under two conditions.
Source: art_01M6JV03D8SRF5T8MH86SJWF0N revision 2 (Veyrul).

## Why this experiment?

The Veyrul record identifies three unresolved blockers before inference can run:
1. Stem layout (count, order, format) is not stated in the README.
2. Impulse responses (IRs) are withheld for copyright; users must supply their own.
3. Weight and training-data terms are not stated in the files read.

Blockers 1 and 3 must be resolved before running anything.
This brief targets **blocker 2** once 1 and 3 are cleared: does IR quality matter?

## Discriminating question

> Does supplying high-quality, length-matched IRs (2-4 s RT60 for augmentation;
> <1.5 s pre-reverb for real dry stems, as stated in the README) produce a
> perceptibly different mix from using the model with minimal/no reverberation
> augmentation?

This is the most informative small test because the paper used 130 IRs for
augmentation, but users must source their own. If IR choice has negligible
perceptual effect on inference output, the withheld-IR blocker is practically
moot. If it matters, IR sourcing becomes a first-class preparation step.

## Two conditions

| Condition | Description |
|-----------|-------------|
| A (IR-matched) | User-sourced IRs meeting README specs: RT60 2-4 s for augmentation, <1.5 s pre-reverb for real dry stems |
| B (IR-minimal) | Inference run without reverberation augmentation (or with a single flat/anechoic response) |

All other variables held fixed: same stems, same model checkpoint, same
normalization pipeline.

## Pre-run checklist

- [ ] Confirm weight licence terms before any use (not stated in files read)
- [ ] Confirm training data terms (MUSDB18 licence; private sets not available)
- [ ] Probe stem layout (see `probe_stem_layout.py`)
- [ ] Confirm model checkpoint name matches one of: ours_S_La, ours_S_Lb,
      ours_S_pretrained, wun_S_Lb (small-set only; large-set weights release status unknown)
- [ ] Source IRs: at minimum 1 short (<1.5 s) and 1 long (2-4 s RT60) free-licence IR
- [ ] Pin environment: torch 1.9.0, librosa >=0.8.1, setuptools 59.5.0
  (note: older torch may conflict with current CUDA drivers)

## What would change our mind?

- If A and B outputs are **indistinguishable** in a blind flip test: IR sourcing
  is a low-priority blocker; focus shifts to weight terms and stem layout.
- If A and B outputs **differ audibly** (panning, reverb tail, spectral balance):
  IR sourcing is a critical preparation step and the 130-IR augmentation
  strategy in the paper has a real practical counterpart.

## Limitations to record

- The paper's highest scores are for large-set models; released weights are
  small-set only. Any result here applies only to the released checkpoints.
- The listening test in the paper used 14 engineers on short
  chorus-to-verse excerpts, not full songs. The paper itself notes full-length
  coherent mixes need further analysis.
- Objective metrics (loudness, dynamics, panning) matched better than spectral
  values in the paper's own analysis. EQ and reverb deviation is expected.