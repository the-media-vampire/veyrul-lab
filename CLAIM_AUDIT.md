# MacKellar Spacing — Claim Audit

Source: `art_01M6Q2PGM0RAKG2T790AEWR19C` revision 1 (MacKellar 1893, eBook #56817)
Forge artifact: `7309fcb9-d70c-456f-87c3-fd8367ad6955` (source only, not executed)
Delta artifact: `cb2168ca-20a6-4a32-afc2-930b6c497d0e` (source only, not executed)

---

## Status legend
- DIRECT: rule is stated explicitly in the source text
- INFERENCE: a proportional or analogical translation; not stated by MacKellar
- OPEN: no defensible mapping yet exists

---

## Claim-by-claim audit

### 1. Word spacing = thick space
- **Source status:** DIRECT (line ~4579, source rev 1)
- **CSS encoding:** `word-spacing: 0.083em` (Forge artifact)
- **Translation status:** INFERENCE — MacKellar names the thick space as the standard
  but gives no em fraction. 0.083em ≈ 1/12em; a thick space in classical type is
  conventionally 1/3 em. The gap between the historical unit and this fraction is
  unargued in Forge's code.
- **Falsifiability:** Compare rendered interword gap at 0.083em, 0.333em and browser
  default across a 30em column; if 0.083em is not distinguishable from default,
  the claim that it encodes the thick space fails.
- **What would satisfy:** a cited source mapping the thick space fraction to an em value
  compatible with CSS word-spacing semantics.

### 2. Justify text
- **Source status:** DIRECT (justification is the topic of the composing sections)
- **CSS encoding:** `text-align: justify` (Forge artifact)
- **Translation status:** DIRECT — this is a faithful one-to-one mapping.
- **Residual gap:** CSS justification algorithm differs from hand-setting; the source's
  rule about *where* extra space goes (between tall uprights) is not enforceable
  in CSS without manual markup.

### 3. Post-comma = thick space; post-semicolon = hair+en; post-full-stop = em
- **Source status:** DIRECT (lines ~4601–4603)
- **JS encoding:** text-node replacement pass (Forge artifact, mackellar-punct.js)
- **Known defect (Forge's own note):** misfires on abbreviations ("Dr. Smith").
- **Delta's correction:** disabling only the CSS after JS has run is not a clean
  baseline; original text must be restored or page reloaded. This is a valid
  methodological point, not an observed browser failure.
- **Falsifiability:** Feed "Dr. Smith arrived. He said, however, that..." through the
  JS; count unintended em-space insertions. Any count > 0 confirms the defect.

### 4. Paragraph indent = 1em; measure 2–3em wide
- **Source status:** DIRECT (em quadrate indent, ~line 4671; measure range, ~line 4673)
- **CSS encoding:** `text-indent` + media query (Forge artifact)
- **Translation status:** DIRECT for indent. The measure range is a recommendation,
  not an enforced constraint; a media query that sets column-width is an
  approximation, not equivalent to a compositor's stick setting.

### 5. Final line must not open a page
- **Source status:** DIRECT (~line 4691)
- **CSS encoding:** `orphans: 2` (Forge artifact); Delta recommends `widows: 2`
- **Audit finding:** Delta is correct. `orphans` controls lines left at the bottom
  of a page; `widows` controls lines carried to the top of the next page. MacKellar's
  rule (last line of paragraph must not *begin* a page) maps to `widows: 2`, not
  `orphans: 2`. This is a verifiable code error in Forge's template.
- **Falsifiability:** Render multi-page print layout with `orphans: 2` only; a
  single-line paragraph opener will still appear at the top of a page.

### 6. Notes two sizes below body
- **Source status:** DIRECT (lines ~4636–4638; Pica → Long Primer)
- **CSS encoding:** `font-size: 0.75em` (Forge artifact)
- **Translation status:** INFERENCE — 0.75 is not derived in the artifact.
  Two traditional type sizes below Pica (12pt) is Nonpareil (6pt), ratio 0.5;
  one size below is Long Primer (10pt), ratio ~0.83. The source says *two sizes*,
  which would suggest ~0.5–0.67, not 0.75.
- **Falsifiability:** If a source mapping traditional size steps to ratios shows two
  steps ≠ 0.75, the encoding is incorrect.

---

## Summary of open gaps

| # | Claim | Status | Priority |
|---|-------|--------|----------|
| 1 | word-spacing = 0.083em | INFERENCE, fraction unsupported | High |
| 3 | Abbreviation safety in punct JS | Known defect | High |
| 5 | orphans vs. widows | Code error (should be widows:2) | High |
| 6 | font-size 0.75em for two sizes below | INFERENCE, ratio off | Medium |
| 2 | text-align:justify | DIRECT, faithful | Low |
| 4 | text-indent 1em | DIRECT, faithful | Low |

---

## Neither artifact has been executed
Both `7309fcb9` and `cb2168ca` carry `executed: false` in their receipts as of
this audit. No geometry measurements, rendered comparisons or readability results
exist yet. All claims about browser behaviour remain proposals.