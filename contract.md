# Spine-panel lettering contract

Maps Cockerell (Bookbinding, and the Care of Books, Gutenberg 26672,
chapter XV, lines 3818–3924) to a CSS/SVG layout interface.
Every rule is the author's claim, restated; none is tested here.
Source: art_01M6QDBQN448XJGKMPFN7C85ES r1.

## Interface table

| Rule ID | Cockerell claim (line) | Interface parameter | Pass condition | Assumption flagged |
|---|---|---|---|---|
| R1 | Lettering fills the panel without strain (3888–3889) | `--spine-fill-ratio` | 0.75 ≤ ratio ≤ 0.95 | 'strain' is unquantified; 0.95 is a proposed ceiling |
| R2 | Four letter sizes serve every book (3839–3840) | `--spine-size-steps` | exactly 4 discrete values | Cockerell's claim; no measurement given |
| R3 | Mixing type sizes in one title: avoid when possible (3903–3904) | `--spine-mixed-sizes` | boolean false preferred | 'when possible' allows override with justification |
| R4 | Mixing letter designs: on no account whatever (3904–3905) | `--spine-font-families` | count === 1 | Absolute in source; treated as hard constraint |
| R5 | Single-word title on narrow back (<= 5/8 in) is illegible at small size (3892–3894) | `--spine-word-count`, `--spine-width-in` | if word_count===1 and width<=0.625, flag WARN | 5/8 in = 15.875 mm; digital DPI conversion needed |
| R6 | Running word lengthwise: use only when necessary (3897–3899) | `--spine-orientation` | 'horizontal' preferred; 'vertical' allowed with WARN | Raised bands context omitted in digital use |
| R7 | Thin volume in a set: compromise its lettering, not the set's (3909–3912) | `--spine-is-thin-in-set` | boolean; if true, allow R2 exception (smaller step) | 'generally better' — not absolute |
| R8 | Very thin book: lettering on side, not back (3914–3916) | `--spine-width-in` | if width < threshold, emit ERROR with side-label advice | Threshold not stated; proposed 0.25 in (6.35 mm) |
| R9 | Special decorated binding: some licence / mystery acceptable (3918–3921) | `--spine-special-binding` | boolean; if true, R3 and R6 downgrade to WARN | 'not perhaps out of place' — hedged; must be declared |
| R10 | Most books: clear lettering of utmost importance (3922–3923) | default state | R4 always hard; R1, R3 hard unless R9 set | Named as the default, not the exception |

## Known gaps (documented in source record)

- Figures 90–95 and 115 are absent from the plain-text file; letter-design
  examples Cockerell references are not recoverable from this source.
- 'Strain' (R1), 'very thin' (R8), and 'very large number of copies' (pallet
  advantage) are unquantified. All numeric thresholds above are proposals.
- The pallet vs. handle-letter distinction has no digital analog; omitted.