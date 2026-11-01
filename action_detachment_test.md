# Action Detachment Test Brief

## Problem statement
Both Card A (c6002874) and Card B (4b632fd7) show a large blank gap
between the description text and "Reserve a place." My vision-model
inspection of each image confirmed this independently of Scout's report.
The action element reads as the weakest and most detached item in both
cards, regardless of which hierarchy variant is chosen.

## Hypothesis
The gap is an auto-layout default spacing artifact, not a deliberate
design decision. It will persist through FigCraft auto-layout conversion
unless explicitly overridden.

## Test inputs (fixed across all variants)
- Width: 320 px, internal margin: 24 px
- Background: warm off-white; text: near-black
- Copy identical to Iris's brief (rpl_01M6C6SARGXYEXPY2Y2GBB99PK, rev 1)
- Card A hierarchy only (title 32 px, details 14 px)

## Three spacing conditions to compare

### Condition 1 — Baseline (current state)
Apply Add auto layout with no spacing override.
Record: gap px between description bottom edge and action top edge.

### Condition 2 — Explicit gap collapse
Set auto-layout gap between description and action to 12 px.
Record: same measurement. Also: does action still feel discoverable
or does it merge with the description?

### Condition 3 — Action in a separate bottom-anchored sub-frame
Wrap title + details + description in one auto-layout frame.
Place action in a second frame pinned to the card bottom.
Record: visual separation, and whether action reads as a distinct CTA.

## Decision rule
Prefer the condition where:
1. Gap between description and action is <= 16 px (no detachment), AND
2. Action remains visually distinct from description (not merged), AND
3. Title still leads (per Iris's original rule).

If no condition satisfies all three, record which condition fails which
criterion and escalate to a type-weight change on the action element.

## What to log per condition
- Screenshot at baseline (before auto layout) and immediately after
  Add auto layout, no corrections.
- Measured gap in px (use FigCraft inspector).
- Any clipping, overflow or overlap.
- Manual repairs required and their description.

## Longer-title stress test (run after baseline passes)
Replace "After Hours" with "After Hours: Drawing Together After Dark".
Rerun all three conditions. Record whether gap changes (auto layout
may redistribute space when the title wraps).

## Scope
This brief targets spacing only. Hierarchy (A vs B) and punctuation
artifacts (trailing dot in Card B logistics wrap) are separate concerns
documented in rpl_01M6C8BXC17KXE6405J0W7455K, rev 1.