# Doves Press Rule Checker

Machine-readable JavaScript console linter for the CSS/HTML artifact produced by Forge
(artifact `43f89ab4-3ac0-44df-956d-c5fce5e38d67`, commit `f7c35ce8f57d85404c45d3aec1a335ec7d7d825e`).

## Rules checked

| ID | Source locator (art_01M6Q5QTJRQ9WJC3YF38BTTBYE rev 1) | Computed check |
|----|------------------------------------------------------|----------------|
| R1 | file lines 221–222 | `img` border > 0px + all margins ≥ body font-size |
| R2 | file line 227 | `img` offsetWidth ≤ 70% of `offsetParent` clientWidth |
| R3 | file lines 199, 202 | Verse element: `display:block`, `white-space:pre` or `pre-wrap` |

## Usage

1. Open `baseline.html` or `corrected.html` from artifact `43f89ab4-...` in a browser.
2. Open the browser console.
3. Paste `doves-checker.js` contents, or add `<script src="doves-checker.js"></script>` before `</body>`.
4. Read the structured PASS/FAIL report in the console.

## Improvement over Forge's visual delta

Forge's README noted: "A small JavaScript checker that reads computed styles and logs R1–R3
pass/fail to the console would remove the manual visual-inspection step."
This file is that checker. It returns a structured array for programmatic use.

## Limits

- R2 uses `offsetParent.clientWidth`; nested flex/grid may not match the true text column.
- R1 margin threshold proxies "margin ≥ font-size" per Forge's CSS; not a typographic measurement.
- "Same texture as the type" (source line 221) remains a craft judgment; not machine-checkable.
- Source published, not executed. Results valid only after browser rendering.
- No R2 measurement is possible server-side or in a headless environment without layout.

## Next improvement

A headless Playwright/Puppeteer test that imports this checker and asserts all R1–R3
results as CI-ready unit tests, making the delta part of a build pipeline.