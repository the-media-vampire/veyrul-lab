"""Blender 4.5 glTF constraint bake validation script.

Usage: paste into Blender Scripting workspace, run in a scene that contains
  - An Empty named 'FollowTarget' with a simple keyframed Z position
  - A Cube named 'ConstrainedProp' with a 'Child Of' constraint targeting FollowTarget
  - Timeline: frames 1–60

Baseline export (bake OFF) — run first, rename output:
  set BAKE_ANIMATIONS = False
Test export (bake ON) — run second:
  set BAKE_ANIMATIONS = True

Observable difference: open each .glb in Godot 4.6 and check
AnimationPlayer track count on ConstrainedProp (see checklist.md).
"""

import bpy
import os

# --- Configuration -----------------------------------------------------------
BLENDER_VERSION = bpy.app.version_string   # logged; must be 4.5.x
OUTPUT_DIR      = "/tmp/gltf_constraint_test"  # adjust to your OS
FRAME_START     = 1
FRAME_END       = 60
FPS             = 24
SAMPLING_RATE   = 1          # export every frame; reduces missed poses
BACE_ANIMATIONS = True       # <-- toggle False for baseline, True for test
# -----------------------------------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

tag = "bake_ON" if BACE_ANIMATIONS else "bake_OFF"
out_path = os.path.join(OUTPUT_DIR, f"constraint_test_{tag}.glb")

bpy.context.scene.frame_start = FRAME_START
bpy.context.scene.frame_end   = FRAME_END
bpy.context.scene.render.fps  = FPS

bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format='GLB',
    # Animation options
    export_animations=True,
    export_animation_mode='ACTIONS',   # or NLA_TRACKS if actions differ
    export_bake_animation=BACE_ANIMATIONS,  # 'Bake All Objects Animations'
    export_sampling_rate=SAMPLING_RATE,
    # Material options (Principled path; no bake needed for plain diffuse)
    export_materials='EXPORT',
    export_image_format='AUTO',
    # Keep transforms relative to scene root
    export_apply=False,
)

print(f"[constraint-test] Blender {BLENDER_VERSION}")
print(f"[constraint-test] bake={BACE_ANIMATIONS}  output={out_path}")
print("[constraint-test] Done. Open output in Godot 4.6 and run checklist.md")