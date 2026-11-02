# Shot-Design Parameter Validation Contract

Source: art_01M6E0C4BCPN6F8PBCHMAM3X4Q r1 (reported, not tested).
All prompt mappings are the source records' inference; no model was tested.

## Two downstream interfaces

| Interface | Key fields |
|-----------|------------|
| AI video prompt (e.g. Veo) | lens_word, dof_intent, fstop, move |
| USD camera turnover | focalLength, apertures, focusDistance, fStop |

## Assumptions at each boundary

**Prompt interface** (sources: art_01M5NP7E r1, art_01M5NHNG r1, art_01M5NNTZ r1)
1. One lens type + one effect per clause; contradictory stacking flagged.
2. One move per shot with type and direction from the Veo vocabulary.
3. Wide-angle + extreme shallow DOF is a flagged blend (ZEISS mechanics).

**USD turnover** (sources: art_01M5NPJC r1, art_01M5MTTJ r1, art_01M5MCHV r1)
1. focalLength and both apertures required for pinhole solve.
2. Estimates must be labelled; nominal lens numbers are starting points only.
3. Distortion and entrance-pupil data absent from base UsdGeomCamera.
4. ARRI sources: use Lens Effective Focal Length, not plain Focal Length.

## License
MIT. Upstream document rights (ZEISS paper, ARRI white paper, Veo guide,
LibreTexts CC BY-ND 4.0) are not determined here; see source records.