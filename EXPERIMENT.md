# One clear window

Status: original, unexecuted experiment brief. No PixiJS install, scene rendering, media inspection or viewer study has been performed for this package.

## Documentary basis
art_01M6FHCR2SS2T36K66NRDP3A56 revision 1 reports that PixiJS filters affect a display object and its children, and names BlurFilter as Gaussian blur. This supports a filter-scope experiment, not a claim that blur improves attention. The supplied source is a documentation summary, not runtime validation.

## Visual intention
First notice one illuminated window; next feel the quiet of a mostly sleeping building. My taste preference is selective softness rather than an all-over cinematic wash. The window must remain the subject, not the effect.

## Fixed composition
Use a 960 x 540 logical-pixel canvas, fixed camera, dark slate background. Center a flat facade at x=240,y=90,width=480,height=360. Arrange twelve 40 x 52 windows in four columns and three rows; centers x=300,420,540,660 and y=168,270,372. Eleven windows are muted blue-grey; the window at (540,270) is warm amber. No type, particles, glow, texture grain or motion. Leave the amber window identical in geometry and color in every condition.

Use a scene parent containing a context group (facade and eleven dim windows) and a separate focal-window object. This hierarchy is an implementation proposal, not tested API code.

## Conditions
C: no filter, baseline.
A: apply one BlurFilter to the context group only; keep the focal window unfiltered.
B: apply an identically configured BlurFilter to the scene parent; include the focal window.

Choose a moderate blur setting once during implementation and record its exact constructor options. Do not tune the setting separately for A and B. Keep all positions, colors, canvas dimensions, renderer, resolution and capture framing fixed. Allow sufficient filter bounds/padding and inspect facade edges for clipping. Record actual PixiJS version and renderer. Do not infer equivalent results across WebGL and WebGPU without testing both.

## Capture and technical checks
Capture C, A and B as separate stills, not a labeled side-by-side. Inspect all three actual outputs before making visual claims. Log: successful rendering; correct filter target; unchanged object geometry/colors before filtering; whether A leaves the focal window sharp; clipping or seams. If checks fail, fix or mark the condition invalid. Do not count a successful build as visual inspection.

## Small exploratory review
Show each condition separately for two seconds, using balanced order across six reviewers if available. Ask, without naming the window: (1) What did you notice first? (2) What mood did it suggest? Then show all conditions for a free comparison and ask whether softness felt deliberate or merely out of focus. Log individual answers and presentation order. Repeated composition creates carryover; this is a formative review, not a causal or population-level study.

## Decision rule
Prefer A only if at least four of six reviewers name the amber window first and A receives fewer 'out of focus' judgments than B. Treat this as a preselected design gate, not statistical proof. If C performs as well and conveys quiet, prefer C: remove the effect. If B better communicates the intended quiet without losing the focal window, reconsider the selective-blur preference. Report technical observations separately from reviewer responses and artistic judgment.

## Deliverables
Three inspected captures; renderer/version/filter-options log; raw review notes; a short decision with unresolved limitations. Until these exist, the outcome is unknown.