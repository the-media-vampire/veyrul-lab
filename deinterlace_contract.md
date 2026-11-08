# Deinterlace filter integration contract

Sources: art_01M6WBQHN1QPSVDASBNRJ79MJ0 r1 (estdif), art_01M6W7KM5GGM4S7CYABK1YGN7G r1 (w3fdif).  
Evidence status: both records are documentary reviews; no command was run in either.

## Shared interface surface

| Parameter | estdif | w3fdif | Notes |
|---|---|---|---|
| Field parity | `parity` (tff/bff/auto) | `parity` (tff/bff/auto) | Identical name and semantics; auto assumed tff when unknown |
| Deint scope | `deint` (all/interlaced) | `deint` (all/interlaced, not covered in w3fdif record) | estdif record documents this; w3fdif record notes the option exists but skips it |
| Input flags | Decoder-reported or setfield | Decoder-reported or setfield | Same fix path for wrong field order |
| Output container | Any FFmpeg-muxable format | Any FFmpeg-muxable format | No filter-level constraint |

## Divergent interface surface

| Concern | estdif | w3fdif |
|---|---|---|
| Algorithm | Spatial edge-slope tracing | Weston 3-field temporal + spatial |
| Output frame rate | Always 1× input | mode=field (default) = 2× input; mode=frame = 1× |
| Main quality knobs | rslope (1–15), redge (0–15), ecost/mcost/dcost (0–50 each), interp (2p/4p/6p) | filter=simple/complex |
| Temporal dependency | None (spatial only) | Yes — uses adjacent fields |
| Jagged-diagonal fix | Raise rslope | No direct equivalent |

## Decision table

```
If temporal fields are available AND frame-rate doubling is acceptable:
  → w3fdif, mode=field (default). Better on motion; uses neighbouring fields.
If temporal fields are unavailable OR source is damaged/discontinuous:
  → estdif. Spatial-only; no cross-field dependency.
If output must stay at input frame rate:
  → w3fdif mode=frame  OR  estdif (always 1×).
If diagonal edges are the main artefact:
  → estdif; tune rslope upward.
```

## Minimal selector script (shell, illustrative — not tested)

```sh
#!/bin/sh
# Usage: deint.sh <input> <filter: estdif|w3fdif> <output>
# Assumptions: FFmpeg on PATH; input is interlaced; field order auto-detected.
INPUT="$1"
FILTER="$2"
OUTPUT="$3"

case "$FILTER" in
  estdif)  VF="estdif=interp=4p:rslope=1" ;;
  w3fdif)  VF="w3fdif=filter=complex:mode=frame" ;;
  *)       echo "Unknown filter: $FILTER"; exit 1 ;;
esac

ffmpeg -i "$INPUT" -vf "$VF" "$OUTPUT"
```

## Combination filter chain

If a source has both damaged fields and a known bad field order:
```
ffmpeg -i in.mov -vf setfield=tff,estdif=interp=6p:deint=interlaced out.mp4
```
setfield corrects parity; estdif skips frames already marked progressive.  
This chain is assembled from documented options; no output was observed.

## Assumptions that must hold

1. FFmpeg build includes both filters (not guaranteed by all distribution packages).
2. `deint=interlaced` relies on correct interlacing flags in the stream; corrupted flags defeat this.
3. w3fdif temporal quality depends on fields being temporally adjacent — not true for stills-sourced or heavily edited timelines.
4. Mode equivalence of `parity` and `deint` between filters is inferred from reading both records side by side, not from a shared code base.

## Open evidence gaps

- Neither record was run; no visual output exists for either filter.
- w3fdif `deint` option is acknowledged but not documented in its record.
- Actual rslope thresholds for real diagonal content are uncharacterised.