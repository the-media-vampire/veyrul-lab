# Doves Press Integration Linter

Operationalises two claims from **art_01M6Q5QTJRQ9WJC3YF38BTTBYE rev 1**
(Cobden-Sanderson, _The Ideal Book_, Doves Press 1900, file lines 199–227).

## Rules encoded

| Rule ID | Tract source | What to check |
|---------|-------------|----------------|
| R1 | lines 221–224 | Every `<img>` or `.illustration` has a visible border/frame **and** a margin ≥ body-font-size on all sides |
| R2 | lines 221, 227 | No illustration's rendered width exceeds 70% of the text column (prevents "over brilliancy") |
| R3 | lines 199, 202 | Every verse block (`<pre>` or `.verse`) is displayed as a block, not inline; line-height ≥ 1.4 so the stanza shape reads at a glance |

## Files

- `baseline.html` — fails all three rules (floating unframed image, inline verse span)
- `corrected.html` — passes all three rules
- `doves-integration.css` — the shared stylesheet that enforces R1–R3
- `lint-checklist.txt` — a manual diff table: open both pages in a browser and tick each row

## Limits

- CSS cannot enforce R2 without JavaScript; the stylesheet uses `max-width: 70%`, which is a best-effort proxy.
- "Same texture as the type" (line 221) is a visual/craft judgment the stylesheet cannot mechanically test.
- Rules are curator analysis derived from art_01M6Q5QTJRQ9WJC3YF38BTTBYE rev 1; they are not a quotation of Cobden-Sanderson.
- Source published, not executed. Browser rendering is the execution step.

## Next improvement

Add a JavaScript axe-style checker that reads computed styles and reports R1–R3 pass/fail to the console,
producing a machine-readable delta without manual visual inspection.