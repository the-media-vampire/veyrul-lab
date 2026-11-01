# Known research gaps -- 2026-11-01

Source: art_01M6AATGSEDBC6G46272K4Y7Q8 r1

## Gap 1: Mesh output format
None of the seven workflow JSON files name the mesh format (OBJ, GLB, PLY)
that Comfy3D nodes emit. A downstream converter cannot be specified.

## Gap 2: Weight licences
The source record notes no licence is cited or interpreted. Hunyuan3D,
TripoSG, TRELLIS and Stable3DGen each have their own terms. Commercial
use cannot be assessed without reading each model's licence file.

## Gap 3: VRAM per workflow
Only Era3D has a stated figure (>=16 GB). The seven documented workflows
have no quantified VRAM figure in the source record.

## Gap 4: IMAGE pre-processing contract
None of the files state whether the input image must be background-removed,
cropped to a fixed square, or normalised before the ShapeGen node. Tools
like rembg are common in 3D workflows but absent from the documented files.

## Gap 5: 64 remaining workflow files
The source record notes 64 other files in the packet were not read. Those
may include additional models or pipeline patterns that change the picture.