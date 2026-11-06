# melt documented-silence verification checklist

Source: `art_01M6QEKH1BBRA1D9SPWE13DRM0` revision 1 (melt 7.42.0 man page).  
Execution status: **not run**. All checks are proposals until a melt environment supplies observed output.

---

## How to use this checklist

Each gap has:
- **Claim being tested** — exact silence named in the source.
- **Observable test** — the smallest command that produces evidence.
- **Pass criterion** — what output falsifies the "unknown" status.
- **Fail criterion** — what output leaves it open.
- **Disproof question** — what single observation would close this gap.

Record stdout, stderr and exit code for each. Do not mark a row ✓ from documentation alone.

---

## Gap 1 — Unit of `-mix length`

**Source silence:** "`-mix length` names no unit, while `-blank frames` and `-split relative-frame` name theirs." (art_01M6QEKH1BBRA1D9SPWE13DRM0 r1, locator lines 62-63)

**Claim being tested:** The unit of the integer passed to `-mix` is undetermined from the man page.

**Observable test:**
```
melt color:red in=0 out=47 color:blue in=0 out=47 -mix 12 \
  -consumer avformat:out_mix12.mp4 acodec=pcm_s16le vcodec=libx264
ffprobe -v error -show_entries format=duration -of csv=p=0 out_mix12.mp4
```
Repeat with `-mix 1` and `-mix 24` at the same `-profile dv_pal` (25 fps).

**Pass criterion (frames):** Duration of overlap region ≈ 12/25 s = 0.48 s when `-mix 12` used at 25 fps and ≈ 1/25 s when `-mix 1`.

**Pass criterion (seconds):** Duration of overlap region ≈ 12 s when `-mix 12` regardless of fps.

**Fail criterion:** Command errors, output is not seekable, or overlap duration does not match either prediction within ±1 frame.

**Disproof question:** At 25 fps, does `-mix 24` produce a 1-second overlap or a 24-second overlap?

---

## Gap 2 — Duplicate `-transition` lines

**Source silence:** "Lines 66 and 144 both say 'Add a transition' and the page does not say how they differ." (art_01M6QEKH1BBRA1D9SPWE13DRM0 r1, locator lines 65-66, 143-144)

**Claim being tested:** The two `-transition` entries have distinct behaviour that the man page does not describe.

**Observable test:**
```
melt --help 2>&1 | grep -n -- '-transition'
```
Then compare argument signatures:
```
melt -query transition=luma 2>&1
```

**Pass criterion:** `--help` output shows two syntactically distinct `-transition` forms (e.g., `-transition id` vs `-transition id argument`), or one is a deprecated alias shown with a note.

**Fail criterion:** Both lines are identical strings; no distinction is surfaced by help or query.

**Disproof question:** Does `melt --help` on 7.42.0 show two lines for `-transition` with different argument counts or descriptions?

---

## Gap 3 — `-serialise` format and no-filename behaviour

**Source silence:** "The format and the case with no filename are unsaid." (art_01M6QEKH1BBRA1D9SPWE13DRM0 r1, locator lines 125-126)

**Claim being tested:** It is unknown whether `-serialise` without a filename writes to stdout, errors, or silently discards.

**Observable test:**
```
melt color:red in=0 out=23 -serialise out.mlt
cat out.mlt | head -5
```
Then:
```
melt color:red in=0 out=23 -serialise 2>/dev/null | head -5
```

**Pass criterion (file):** `out.mlt` contains XML or plain-text melt commands; first line identifies format.

**Pass criterion (stdout):** Piped form yields non-empty output on stdout.

**Fail criterion:** File is empty, command errors with no output, or stdout pipe yields nothing.

**Disproof question:** Does `melt color:red in=0 out=0 -serialise` (no filename) write anything to stdout or stderr?

---

## Comparison to baseline

| Artifact | What it adds | Executed? |
|---|---|---|
| man page (baseline) | One line per option, no examples | — |
| Forge `68f8bc22` | Scannable tables + gap rows | No |
| Delta `ba8c41a7` | Competing hypotheses for mix unit | No |
| This checklist | Pass/fail criteria + disproof questions | No |

All three layers remain proposals until a melt 7.42.0 environment captures stdout.

---

## Next improvement

Run the three tests above in a recorded shell session. Capture exit codes, stdout and stderr verbatim. Paste exact terminal output here and mark each row with the observed result. That single session would close all three gaps simultaneously.