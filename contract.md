# Integration Contract: Midjourney Editor ↔ Local Batch-Mask Prep

**Status:** Proposal — not tested against live accounts.  
**Source:** art_01M6GKXQMMZWA3SYV9SQKETJE2 rev 1 (documented, not run).

---

## 1. What each side provides

| Side | Mechanism | Interface point |
|------|-----------|----------------|
| **Local mask prep** (e.g. rembg, SAM) | Pixel-level subject/background segmentation; outputs PNG with transparent regions | PNG file on disk; transparency = "regenerate this" |
| **MJ Editor (V8.X)** | Erase brush / Smart Select → Submit Edit; regenerates only transparent areas; flattens layers on submit | Browser upload or URL paste; results in Create/Organize pages |

## 2. Interface contract

```
INPUT  → RGBA PNG, ≤ browser upload limit (size/format limits NOT stated by MJ docs)
           transparent pixels = erase zone
           opaque pixels      = preserve zone
PROMPT → text description of what fills the transparent zone
OUTPUT ← 4 result variants in MJ results panel
         visibility: Create+Organize (V8.X, no Stealth) or Editor-only (V7)
```

**Key contract rule from MJ docs:** only pixels with visible transparency (gray checker) are regenerated; opaque areas are unchanged. This is the load-bearing assumption of the whole pipeline.

## 3. Provenance & license assumptions

- External images require agreement to MJ's extra rules: age compliance, applicable law, Community Guidelines, content responsibility. User must hold necessary rights to uploaded images.
- MJ deepfake/person-manipulation prohibition applies regardless of local prep.
- Local segmentation tools (rembg: MIT; SAM: Apache 2.0) are separately licensed; outputs inherit user's rights to source image.
- MJ output license: governed by MJ Terms of Service (not reproduced here).

## 4. Adapter steps (proposed, not run)

```
1. Segment locally:
   rembg -i input.jpg -o masked.png   # removes background → transparent
   # OR invert: keep background, erase subject zone

2. Validate before upload:
   - Confirm PNG has alpha channel
   - Confirm transparent region is intentional (preview overlay)
   - Remove Omni Reference / --ow if image originated from MJ gallery with those params

3. Upload to MJ Edit tab (external image path)
   - Accept extra-rules prompt
   - Paste or upload masked.png

4. Enter prompt describing fill content
   - If using Smart Select instead: apply mask with Erase Selection or
     Erase Background BEFORE submitting (green highlight = not yet applied)

5. Submit Edit → 4 variants generated
   - V8.X: appears on Create/Organize unless Stealth
   - V7 or earlier: Editor-only until upscaled
```

## 5. Failure modes & gaps

| Failure | Cause | Mitigation |
|---------|-------|------------|
| Smart Select mask not applied | Green highlight still visible | Click Erase Selection or Erase Background first |
| Omni Ref error on MJ gallery image | --ow / Omni Ref still attached | Strip those params before submit |
| Moderation block | Prompt or content flagged | No credit cost; revise prompt |
| Unknown size/format limit | MJ docs do not state limits | Test with small image first |
| Layer content lost | Layers flatten on submit | Export layer PNG before submit if needed |
| Retexture availability | Built-in V8.X; separate feature for V7 | Set version before workflow start |

## 6. What this contract cannot guarantee

- How closely preserved areas actually match original (not stated by MJ docs)
- Maximum accepted image dimensions or file size
- Credit cost of edits
- Failure repair beyond the mask/layer warnings above

## 7. Missing evidence (see research queue)

- Accepted file formats and size limits for external upload
- Whether transparent-PNG upload preserves alpha correctly in MJ browser UI
- Plan-tier requirements for Edit tab access