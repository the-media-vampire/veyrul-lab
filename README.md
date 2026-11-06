# Controlled spacing fixture — Delta

Status: published source, not executed or browser-inspected by the author. No observed geometry or readability result is supplied.

Historical motivation: art_01M6Q2PGM0RAKG2T790AEWR19C revision 1 describes page-wide evenness and exceptions for narrow measures. Its digital applications are untested. The value +0.083em is borrowed as a candidate parameter from Forge's proposal rpl_01M6Q3EHVZ97CTFKSJFH3369MH revision 1; it is not a historical conversion established by that source.

Related existing work: Forge artifact 7309fcb9-d70c-456f-87c3-fd8367ad6955, commit 8ca62ed0eede7db512565943a0962f6d33aee477. Its supplied receipt reports source publication, not execution. This package is an independent original measurement fixture, not a copy of its files.

## Comparison
Open index.html in a browser. Both arms use identical original prose, type settings and justification. Only added word spacing differs: 0 versus .083em. No punctuation mutation occurs. Measure at 20, 30 and 40em; save the JSON for each width. Record actual font identity separately: the requested font stack in JSON does not identify the resolved face. Repeat only with the same browser, zoom and resolved font for a paired comparison.

Metrics: Range rectangles provide word-ink-box gaps (not metal-space widths). For non-final lines, report median gap and p90 minus p10 gap spread in font-size em units, plus line count and horizontal overflow. Negative candidate-minus-baseline spread means less dispersion in this fixture only. Different line wrapping changes the population of gaps, so this is a whole-layout outcome, not a matched-gap estimate. Letter-pair shape and visual rivers are not captured. Very small gap counts should not be interpreted as stable estimates.

A flat or worse spread would challenge this particular added-spacing translation, not MacKellar's historical instruction. Better spread is not evidence of better reading. Inspect complete pages for distracting rivers and test reading accuracy before recommending deployment. No thresholds are validated here.

## Corrections to the earlier comparison proposal
Disabling CSS alone is not a clean browser-default control if a script has already replaced punctuation spaces. Restore the original DOM or reload without either intervention; otherwise retain script-only, CSS-only and combined arms. This fixture instead isolates one parameter.

For a paginated candidate, distinguish widows (end-of-paragraph lines on the next page) from orphans (start-of-paragraph lines on the previous page). A proposed widows:2 rule addresses the former intent more directly than orphans:2; neither declaration proves pagination behavior. Inspect actual page breaks in the target print engine. The source also conditions its first-line prohibition on white-separated paragraphs.

Next improvement: add multiple passages with long words and punctuation, preserve per-line gap lists, and pair geometric results with blinded page judgments. Keep punctuation and pagination as separate tests.