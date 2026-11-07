# Render-Texture Flip: Two-Condition Experiment Brief

**Source:** art_01M6Q6PZWS3BYDS2A1RZQB7E0H revision 1  
**Documented limit:** render textures come out flipped (README lines 59–65)

## Intention

Test whether two common flip-compensation strategies produce identical pixel output
or differ in edge/seam behaviour when the render texture contains a 1-pixel border
of a distinct colour (a stress case for sampling boundaries).

## Controlled variable
Only the draw call changes. Window size, render-texture size, drawn content,
and clear colour are fixed across both conditions.

## Condition A — negative-height rect (DrawTexturePro)
Flip by passing `srcRect.height = -(float)rt.texture.height`.
Expected: clean inversion, no seam, no border bleed.

## Condition B — UV-flipped quad (DrawTextureRec)
Flip by passing a Rectangle with positive height from the bottom row:
`{ 0, (float)rt.texture.height, (float)rt.texture.width, -(float)rt.texture.height }`
Same mathematical intent, different API path.

## Discriminating test
Capture a screenshot of each condition (`TakeScreenshot`) and diff pixel rows
at y=0 and y=height-1. If the strategies are equivalent, both diffs are zero.
Any non-zero diff tells us which API path samples the boundary differently —
that is the informative failure worth reporting.

## What would change our mind
- Zero diff on border rows → strategies are equivalent; the choice is style only.
- Non-zero diff → one path bleeds the adjacent texel; that determines which
  strategy the CONVENTIONS example layout should recommend.

## Fixed variables (do not change between conditions)
- Window: 320×240
- RenderTexture2D: 320×240
- Content: solid fill + 1px border drawn with DrawRectangleLines
- ClearBackground colour: RAYWHITE
- raylib version: whichever commit the README and FAQ were read at
  (4bfb72d8ff46b74ec8e5c745364406c4f153929f)