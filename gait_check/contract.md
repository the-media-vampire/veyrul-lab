# Quadruped Walk-Order Integration Contract

## Purpose
Check a labelled frame sequence from an AI-generated video against the walk foot-contact order reported from eBook 37743 (Muybridge lecture).

## Source
- Record: art_01M6Q6TWNDRV36VHATTZYMPYYE revision 2
- Origin: plain-text eBook 37743, https://www.gutenberg.org/cache/epub/37743/pg37743.txt
- Licence note (source-reported, not interpreted): "no one owns a United States copyright in these works" (line 696). Jurisdiction check required outside the US per lines 7–9.

## Walk order (source-reported, horse; "probably common to all quadrupeds")
  LH → LF → RH → RF  (left-hind, left-fore, right-hind, right-fore)

## Interface

### Input (per stride)
```json
{
  "stride_id": "string",
  "contacts": [
    { "frame": int, "foot": "LH|LF|RH|RF" }
  ]
}
```
- One entry per *new* foot contact (foot-down event), in frame order.
- Ambiguous frames must be labelled `"foot": "?"` — do not omit them.

### Output
```json
{
  "stride_id": "string",
  "expected_cycle": ["LH","LF","RH","RF"],
  "observed_cycle": ["LH","LF","RH","RF"],
  "match": true,
  "flags": []
}
```
Flags: `"ambiguous_frame"`, `"wrong_order"`, `"missing_contact"`, `"extra_contact"`.

## Explicit assumptions (test before trusting results)
1. The order applies only to the walk; trot/amble/gallop have different sequences per the same source.
2. Labelling requires a run of frames showing at least one full stride — a single still cannot satisfy this.
3. The source gives order, not timing; foot dwell-time variation across species is noted but not quantified.
4. The checklist is agnostic to video quality, rendering artefacts or limb count; those are upstream concerns.
5. Species other than horse: source says "probably" common — treat deviations as evidence questions, not proof of error.

## Failure mode to watch
An AI video may hold a limb in contact across many frames; labellers must record the *onset* frame only, not every frame the foot is down. Without this discipline the cycle appears repeated and the check will over-match.