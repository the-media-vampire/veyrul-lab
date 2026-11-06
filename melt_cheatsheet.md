# melt 7.42.0 — command cheat sheet

> Source: art_01M6QEKH1BBRA1D9SPWE13DRM0 r1 (reading of melt.1, help2man 1.38.4, header "October 2026").
> Nothing here was run or installed. Treat as a reading aid, not verified behaviour.

## Synopsis (from man page)
```
melt [producer [name=value ...]] [option ...]
```
Producers come first; each takes `name=value` pairs. Options follow and act on
the last cut, last two cuts, or current track. **Argument order is not stated
on the page — curator inference, not documented fact.**

---

## Cuts — act on the most recent item

| Option | What the page says | Unit stated? |
|---|---|---|
| `-split relative-frame` | Split the last cut into two cuts | frame (stated) |
| `-join clips` | Join multiple clips into one cut | count (implied) |
| `-remove` | Remove the most recent cut | — |
| `-repeat times` | Repeat the last cut | count (implied) |
| `-swap` | Swap the last two cuts | — |

---

## Mix and transitions

| Option | What the page says | Known gap |
|---|---|---|
| `-mix length` | Add a mix between the last two cuts | **Unit of `length` is not stated** |
| `-mixer transition` | Add a transition to the mix | — |
| `-transition` | Add a transition | Page prints two "Add a transition" lines (lines 66 & 144); difference not explained |

---

## Filters — four attachment points

| Option | Attaches to |
|---|---|
| `-attach` | Output |
| `-attach-cut` | A cut |
| `-attach-track` | A track |
| `-attach-clip` | A producer |
| `-filter` | Current track |

---

## Blank and tracks

| Option | What the page says |
|---|---|
| `-blank frames` | Add blank silence to a track (picture side not mentioned) |
| `-track` | Add a track |
| `-audio-track` / `-hide-video` | Audio-only track |
| `-video-track` / `-hide-audio` | Video-only track |
| `-null-track` / `-hide-track` | Hidden track |

---

## Other options

| Option | What the page says |
|---|---|
| `-consumer` | Set the output sink (only line about where output goes) |
| `-profile name` | Set processing settings |
| `-serialise [filename]` | Write commands to a text file |
| `-query` | List all registered services |
| `-chain` | Use producer as a chain |
| `-link` | Add a link to a chain |
| `-group` | Apply properties repeatedly |

---

## Documented silences — what the page does NOT say

These are gaps from the man page reading, not from testing.

| Gap | Why it matters for generated clips |
|---|---|
| No example command | Cannot verify intended argument order |
| No frame rate stated | Generated clips may differ from live-capture defaults |
| Unit of `-mix length` unknown | Cannot safely set a crossfade duration |
| What `-mix` does to audio is unspecified | Mix behaviour on AI-generated audio+video unknown |
| `-serialise` format undocumented | Cannot round-trip a generated composition without testing |
| No filter or transition list on the page | Must run `-query filters` or `-query transitions` to discover names |
| Nothing about generated/synthetic producers | All examples assume file-based producers |

---

## Licence and warranty (quoted from man page, lines 163-164)

> "This is free software; see the source for copying conditions.
> There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
> PARTICULAR PURPOSE."

The page names no licence; the source was not read (a gap).