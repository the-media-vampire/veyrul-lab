# MacKellar 1893 Spacing Rules — CSS Reference Template

Source: **art_01M6Q2PGM0RAKG2T790AEWR19C rev 1**  
MacKellar's *American Printer* (1893), Gutenberg eBook #56817, lines 4574–4699.

## Baseline comparison
1. Open `demo.html` in a browser.
2. Disable `mackellar-spacing.css` in DevTools.
3. The visual delta is the effect of these rules on your font and viewport.

No rendering was run at publication time. The delta is the test.

## Rule table
| Rule | CSS encoding | Inference? |
|------|-------------|------------|
| Thick space between words (line ~4579) | `word-spacing:0.083em` | Yes — glyph space varies |
| Justify text (~4590) | `text-align:justify` | Direct |
| Comma → thick space (4601) | EN SPACE in JS | Yes |
| Semicolon/colon → hair+en (4602) | HAIR+EN in JS | Yes |
| Full stop → em (4603) | EM SPACE in JS | Yes |
| Paragraph indent 1em (4671) | `text-indent:1em` | Direct |
| Wide measure: 2–3em (4673) | `2.5em @90ch` | Yes — threshold inferred |
| Final line not open page (4691) | `orphans:2` | Yes — CSS orphans differ |
| First line not foot page (4692) | `widows:2` | Yes |
| Head-lines: small caps, under body size | `small-caps; 0.95em` | Yes |
| Notes: two sizes below body (4636–4638) | `0.75em` | Yes |

## Limits
- Metal-type size steps ≠ CSS em fractions. All size translations are proportional approximations.
- CSS `orphans`/`widows` differ from MacKellar's page-makeup rule; paged-media support is browser-dependent.
- Punctuation JS may misfire on abbreviations and numbers.