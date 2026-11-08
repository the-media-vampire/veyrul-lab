# yaepblur planes-axis experiment brief

**Source:** art_01M6WM9RZW0W148WYFBN0D3MA8, revision 1  
**Status:** Informative brief only. No commands executed, no outputs inspected.

## The gap this addresses

Iris's brief (rpl_01M6WPM0NPN71JF02HQ2BX767M) varies sigma while holding radius=3 and planes=default (luma only). The source documents a 'colour noise remains' failure mode caused by the default planes setting. If chroma noise is a meaningful contributor to the 'distracting texture' problem, neither of Iris's filtered arms will touch it — and all three files will look identical in the chroma channel. That is a confound: you cannot tell whether sigma tuning is insufficient *or* whether the wrong plane was filtered.

This brief isolates planes as a single new variable.

## Design constraints

- Same clip as Iris's brief (5-second, permission-cleared YUV portrait, blink + small head turn, visible cheek texture)
- Sigma locked at 128 (Iris's 'restrained' value) throughout — do not change it
- Radius locked at 3 throughout
- FFV1 lossless output for all arms
- No sharpening, grain or grade changes

## Arms

```sh
# Already in Iris's brief — reuse, do not re-encode
ffmpeg -i portrait.mov -t 5 -an -c:v ffv1 control.mkv
ffmpeg -i portrait.mov -t 5 -an -vf "yaepblur=r=3:s=128" -c:v ffv1 luma_only.mkv

# Scout addition: luma + chroma (planes bitmask 7 = all three planes in YUV)
ffmpeg -i portrait.mov -t 5 -an -vf "yaepblur=r=3:s=128:p=7" -c:v ffv1 all_planes.mkv
```

Planes bitmask values (from documented option; not independently verified against a build):  
- `p=1` — first plane only (default, luma)  
- `p=7` — all three planes (Y + Cb + Cr)

Record: FFmpeg version, input pixel format, any errors or warnings.

## Discriminating questions

| Observation | Probable implication |
|---|---|
| luma_only and all_planes look identical | Chroma noise is not the distracting element; sigma tuning is the right lever |
| all_planes noticeably reduces colour blotchiness | Chroma was a meaningful contributor; Iris's sigma arms would have missed it |
| all_planes introduces colour smearing at edges | planes=7 is too aggressive; use p=3 (Y+Cb) or p=5 (Y+Cr) as intermediate steps |
| Either filtered arm trails during the head turn | Radius=3 may already be too large for motion; reduce before raising sigma |

## Technical log template

Fill in after running — before watching with labels visible.

```
FFmpeg version:
Input pixel format:
Errors/warnings:

[control]       cheek texture:        eyelash edge:        colour cast:
[luma_only]     cheek texture:        eyelash edge:        colour cast:
[all_planes]    cheek texture:        eyelash edge:        colour cast:
```

## Taste log (separate section, fill in after technical)

```
Which file did you want to keep watching?
Where did your eye land first in each?
Did the face feel calmer — or less particular?
```

## Coordination note

If Iris's sigma arms (s=128 vs s=200) are run first and the result is 'colour noise unchanged across both', run all_planes.mkv before changing sigma again. That sequence keeps variables separated and prevents chasing the wrong knob.