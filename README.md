# Threshold: dark refuge / exposed threshold

Status: UNRUN experiment brief. No PhotoCraft installation, command execution, rendering, image inspection or viewer testing is represented by this package.

## Source boundary
PhotoCraft documentation summary: art_01M6AHP9GYVSKJVJ4N2FTDK9HJ revision 1, commit 422ca7beda90 (v0.18.0). It documents image.adjustments.invert, PNG read/write, MCP command discovery and render_preview. These are documentary capabilities, not verified behavior here. Brief responds to dsc_01M6B8XAKTMGKNRQ0SJ32NSATJ revision 1.

## Visual intention
First notice a narrow doorway; next feel hesitation about crossing it. My taste hypothesis is that a bright doorway in a dark field suggests refuge, whereas its global inversion suggests exposure. Inversion may instead leave the emotional reading unchanged: that is an informative result.

## Fixture specification (create locally; not supplied as rendered media)
Create a flattened, opaque, 1200 x 800, 8-bit grayscale-equivalent RGB PNG. Coordinates use a top-left origin, with half-open rectangles.
- Fill background RGB(24,24,24).
- Fill a doorway rectangle x=[760,880), y=[180,620), RGB(232,232,232).
- Fill a small foreground person-marker rectangle x=[590,610), y=[510,620), RGB(120,120,120).
No lettering, shadows, texture, gradients or other objects. Empty left space is deliberate; do not crop it away. Save fixture.png. This abstract marker is not intended as a realistic person.

## Bounded run
Use disposable copies, no production documents. Preserve fixture.png untouched as A. Obtain B by applying only image.adjustments.invert to a duplicate in PhotoCraft and exporting an opaque PNG. No selective inversion, resizing or automatic enhancement.

Optional MCP route documented in the source: photocraft-cli mcp --automation-read-root /work/project --automation-write-root /work/project . Use a dedicated directory containing only these test files. Discover tool and command argument schemas before issuing requests; this brief supplies no guessed JSON payloads. command_list is the documented discovery tool. Use the available document-opening/export operations only after verifying their schemas. Stop if inversion cannot be identified rather than substituting an undocumented operation.

For a reversibility control, invert B once more and export C. Record command responses and actual filenames. Do not interpret a successful tool response as proof of a correct image.

## Technical checks (not results)
Inspect A, B and C at equal size. Confirm dimensions, opacity, clipping and unchanged geometry. Compare decoded RGB pixels, not compressed file bytes. An exact 8-bit complement would be B=255-A and C=A, but this is a test expectation, not a claim about PhotoCraft's color pipeline. Record profile/rounding differences before judging a mismatch. Inspect actual exported files; a preview alone does not verify export parity.

## Perceptual review
Show A/B separately, at the same display size, for two seconds each; counterbalance order across six reviewers. Hide filenames and the intended emotional labels. Ask: 'What did you notice first?' then 'What does this place feel like?' Capture verbatim answers before offering any interpretation. This is a small qualitative check, not proof of a population effect.

Gate 1: at least four of six identify the doorway first in each version. If not, the hierarchy needs revision before making an emotional claim. Gate 2: inspect whether unprompted descriptions distinguish refuge from exposure. No difference is a valid finding. Do not brighten the person-marker mid-test. Any altered geometry is a new experiment.

## Preference, not finding
I favor A's restrained bright opening, but would reject it if viewers primarily notice the marker or read the opening as a distracting graphic rather than a threshold.