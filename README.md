# negate + colorchannelmixer adapter

Sources: `art_01M6VRHPQXCYKH293R9K1F7KF2` r1 (negate), `art_01M6VJS0YQE8PBGBG1H50KN8MF` r1 (colorchannelmixer)

## What this is

A source-derived shell adapter and integration contract for chaining FFmpeg
`negate` with `colorchannelmixer`. No command was run to produce this.

## Critical assumption

`colorchannelmixer` outputs RGB. `negate=components=y` requires YUV.
Chaining them without a `format=` conversion node between them will fail
or silently no-op for the `y` component. `negate_mix.sh` inserts
`format=yuv420p` before luma-only negate and returns to `format=rgb24` after.

## Modes

| Mode | Filter chain | Use |
|------|-------------|-----|
| `negate_then_sepia` | negate → colorchannelmixer | Sepia of inverted image |
| `sepia_then_negate` | colorchannelmixer → negate | Inverted sepia (predictable) |
| `luma_negate` | format → negate=y → format | Luma-only inversion, format-safe |
| `rgb_negate_only` | negate | Control / baseline |

## Verification steps needed

1. Run `rgb_negate_only` on a test clip; confirm white→black.
2. Run `sepia_then_negate`; confirm sepia warm tones become cool inverted.
3. Run `luma_negate`; confirm hues preserved, brightness inverted.
4. Run `negate_then_sepia`; compare with step 2 to confirm order changes output.

## Evidence status

All filter chains: assembled from source-documented option names. Not run.
See `integration_contract.md` for full evidence table.

## License

MIT