# Blender→Godot glTF constraint bake validation kit

## What this is
A minimal script + checklist to test the sourced claim in
**art_01M6QSV2D946VDMJJM3A83T42E rev 1**:

> The Blender 4.5 glTF exporter's `Bake All Objects Animations` option
> emits evaluated motion for constrained objects.

## What it is NOT
- Not an executed result. No Blender/Godot runtime was available here.
- Not a universal conversion pipeline.
- Not a material baking tool.

## Baseline vs. test
| Run | `export_bake_animation` | Expected Godot outcome |
|---|---|---|
| Baseline | `False` | No animation tracks on constrained prop |
| Test | `True` | Sampled position/rotation tracks present |

The observable delta is AnimationPlayer track count in Godot's Scene dock.

## Limits
- Script assumes Principled BSDF only — no procedural material bake.
- `Child Of` with offset is not tested; only simple follow-parent motion.
- `export_animation_mode='ACTIONS'` requires the constrained object to have
  an action or use NLA; switch to `'NLA_TRACKS'` if tracks are absent.
- Godot 4.6 Android/web editors cannot import .blend directly (sourced fact);
  use the GLB files instead.

## Next improvement
Add a second mesh with an unsupported procedural node and confirm it requires
a texture bake step — testing the other half of the research's material claim.