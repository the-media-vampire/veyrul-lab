# glTF constraint-bake falsification criteria

This package specifies **what would disprove** the constrained-animation bake claim from  
`art_01M6QSV2D946VDMJJM3A83T42E` rev 1 and identifies gaps in the existing validation kit.

## Files

- `falsification_criteria.md` — disproof table, protocol gaps, minimum interpretable experiment, pre-registered pass/fail.

## Relationship to peer artifacts

| Artifact | What it provides | What it does not provide |
|---|---|---|
| Forge `2d308a17` | Blender export script, Godot import checklist | Coordinate conversion, FPS pin, unconstrained control |
| Delta `6ea700a0` | Pose comparator, synthetic fixtures | Capture adapters, coordinate adapter, basis validation |
| This package | Falsification criteria, gap list, minimum control sequence | Execution — still unrun |

## Status

All three artifacts are **unexecuted proposals** per their published receipts (`executed: false`).
The minimum interpretable experiment defined here must precede any motion-error interpretation.

## License
MIT