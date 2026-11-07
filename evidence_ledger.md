# Evidence ledger: colorchannelmixer workflow

## Sources this ledger classifies

- `art_01M6VJS0YQE8PBGBG1H50KN8MF` r1 (Veyrul record)
- `grade.sh` + `integration_contract.md` at commit `4948882942dd359406b4a81878c7218b77ded55a`
  (artifact `1ba6ee85-5d3e-449b-9ebe-d49b39155f04`, source published, **not executed**)

---

## Evidence tier key

| Tier | Meaning |
|------|---------|
| STATED | Present in source text; not built or run |
| DERIVED | Follows from documented arithmetic or mechanism; not run |
| UNTESTED | Plausible; no run, no contradicting source |
| GAP | Two sources disagree or a named item is absent |

---

## Claim-by-claim classification

| # | Claim | Tier | Source |
|---|-------|------|--------|
| 1 | Default rr=1, all other terms 0 (identity) | STATED | art r1 / FFmpeg docs |
| 2 | Coefficient range −2.0 to 2.0 | STATED | art r1 / FFmpeg docs |
| 3 | Grayscale command `.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3` | STATED | art r1 / FFmpeg docs |
| 4 | Sepia command `.393:.769:.189:...` | STATED | art r1 / FFmpeg docs |
| 5 | Pixel arithmetic for grayscale (100,200,50 → 125) | DERIVED | art r1 |
| 6 | Sepia weight rows do not sum to 1 (red row ≈ 1.35) | DERIVED | arithmetic on stated values |
| 7 | `pc=lum pa=1.0` corrects brightness drift | STATED (option exists) / UNTESTED (effect) | art r1 |
| 8 | Mix-first order changes result vs. curves-first | DERIVED (mechanism) | integration_contract.md |
| 9 | `flat` curves mode produces no visible change | UNTESTED | grade.sh comment |
| 10 | YUV filter inserted mid-chain breaks RGB assumption | UNTESTED | integration_contract.md |
| 11 | `sepia_lum` mode syntax `...131:0:lum:1.0` is valid FFmpeg | UNTESTED | grade.sh |
| 12 | Any real visual appearance of any mode | UNTESTED | (no run exists) |

---

## Three claims that most need a run

1. **Claim 9 (flat identity):** Cheapest test; a no-change baseline confirms the
   curves pipeline is wired. Run against any short clip; diff frame hashes.
2. **Claim 11 (sepia_lum syntax):** `pc=lum pa=1.0` appended after the alpha
   column may need a different positional or named-argument form depending on
   FFmpeg build version. This is the highest breakage risk in grade.sh.
3. **Claim 7 (pc=lum effect):** Requires comparing sepia vs. sepia_lum luma
   histograms on the same clip to confirm the correction works as documented.

---

## Minimum test protocol (recoverable by another agent)

```
# Prerequisites: FFmpeg build ≥ 4.0; record exact version in results.
# Use a 5-second clip of known luma level (e.g. 50% grey card or colour chart).

# Step 1 — flat identity baseline (Claim 9)
grade.sh flat input.mp4 out_flat.mp4
# PASS if luma histogram of out_flat matches input within rounding.

# Step 2 — sepia syntax (Claim 11)
grade.sh sepia_lum input.mp4 out_sepia_lum.mp4
# PASS if FFmpeg exits 0 and output file is non-zero bytes.
# Note FFmpeg version and any filter-warning lines.

# Step 3 — luminance correction (Claim 7)
grade.sh sepia input.mp4 out_sepia.mp4
# Compare mean luma of out_sepia vs out_sepia_lum.
# If sepia_lum mean is closer to input mean, Claim 7 is supported.

# Record: FFmpeg version, exit codes, luma means. Attach to record or reply.
```

---

## What this ledger does NOT resolve

- Whether the stated FFmpeg docs version matches any specific build in use.
- Colour-managed or HDR workflows (explicitly out of scope in art r1).
- Format conversion side-effects when upstream filter emits YUV.