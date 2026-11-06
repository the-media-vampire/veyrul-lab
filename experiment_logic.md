# Why consistency is the upstream question

The Pitivi documentation [art_01M6QDQ1SYGKQ8DRSECJ1VKZC8, revision 1] describes
a crossfade as overlapping two clips on the same layer. It says nothing about
generated clips, continuity, or frame-to-frame colour matching.

The peer brief (Iris) proposes comparing hard cut vs crossfade as the primary
experiment. That comparison is only interpretable if the two clips are
sufficiently consistent: if the table changes colour or the ring appears in
a different position, viewers may attribute the transition artefact to the
editing choice when the real cause is generation variance.

## Experiment order
1. Generate Frame A and Frame B from the prompts in prompts.md
2. Fill inspection_sheet.md BEFORE any editing
3. If CONSISTENT: run Iris's A/B comparison (cut vs crossfade)
4. If MARGINAL or INCONSISTENT: record what varied, report as a finding
   (this is an informative failure, not a production problem)

## The discriminating test
Consistency failure is itself a result. It tells us that prompt-identical
image generation does not reliably hold background variables fixed — which
matters for any multi-clip story told with generated assets.

## Variables held fixed in this experiment
- Prompt structure (only the subject changes)
- Lighting description
- Position description
- Aspect ratio

## Variables NOT held fixed (acceptable differences)
- Ring wetness appearance (no ground truth)
- Exact cup handle position