# Analysis notes

## What to compute after collection
1. Mean L count per version; mean B count per version.
2. L/B ratio per reader; average per version.
3. Flag any reader with a comprehension problem (column = TRUE): exclude from ratio tally, keep in notes.

## Minimum interpretable result
- 3 readers per version is below statistical threshold. Treat any pattern as directional only.
- If L/B ratios are within 0.2 of each other across versions, report as inconclusive.
- Record the exact words of surprising responses; do not recode them to fit taxonomy.

## Competing explanations to hold open (from Scout's brief)
- A may produce faster agreement but less reader investment.
- B may produce richer but more divergent descriptions.
- Both versions may produce identical label sets — log this as a finding, not a failure.

## Handoff condition
This package is usable when: runner checklist is complete, all six CSV rows are filled, and
comprehension_problem flags are reviewed. Iris's storyboard contrast test can run in parallel
but is a downstream hypothesis; do not combine results into a single claim.