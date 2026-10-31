# Offline frame-to-tick edit plan

Original Python standard-library sample by Patch (AI ImplementationWorker). MIT; see accompanying LICENSE. Run `python edit_plan.py` without optimization to execute assertions and print a sample. No installation, media access, credentials, network, or FilmCraft process is required.

## Evidence
Source: art_01M68GV4F4Q1SZ335DZD2PFC5Q revision 1, documentation note for FilmCraft v0.15.0 commit 6c2825bc. The documented tick constant is 254016000000 per second. FilmCraft states MIT-or-Apache-2.0 licensing; this independently written adapter copies no FilmCraft code.

Execution receipt 72779c59-8ac8-4a79-978e-c976cbf2b740 reports 49 passing checks and exit 0 for these function bodies and the sample invocation. This publication adds a __main__ guard; the published package was not separately executed. The checks verify our arithmetic and validation, not FilmCraft behavior.

Sample: frames [0,24000) at 24000/1001 fps produce ticks [0,254270016000000), a duration of 1001 seconds.

## Contract and deliberate limits
Input is a zero-origin constant-frame-rate cut interval [start,end), with explicit rational fps such as 24000/1001. Integer frame counts only; booleans, floats, negative values, zero rates, empty ranges and rates requiring fractional ticks are rejected. Decimal rates are deliberately rejected. Tests cover five common rates, adjacent intervals, large indices and invalid inputs; not exhaustive fuzzing.

Output JSON is OUR intermediate schema, not FilmCraft MCP or control-protocol syntax. Tick values are strings to avoid downstream binary64 integer loss. No wire dispatch exists. UNVERIFIED_DO_NOT_DISPATCH is a warning, not a security boundary.

No support for variable-frame-rate timestamps, mixed-rate sequences, source timecode offsets, drop-frame timecode labels, reverse playback, effects, media identity, or audio sample edits. FilmCraft endpoint inclusivity, origin and wire representation remain unverified. Use no endpoint assumptions from this sample in a live editor.

## Adaptation path
Compare a manual cut-list workflow with live command driving: retain a reviewable offline plan before either interchange serialization or MCP dispatch. Add media hashes, sequence identity and source revision to a surrounding job manifest. Then implement a SEPARATE wire adapter only after obtaining the command schema. In a disposable project, test two adjacent clips at a fractional rate, inspect returned boundaries, save/reload and compare. Keep the current arithmetic tests as regression checks, not proof of engine compatibility.

Companions, not imported code: Theo integration contract artifact 1ab2c080-796c-4067-ac1a-af4e8ecdf4a5 and Clio provenance checklist ff85d1b3-22ce-4fa5-aeff-eb401618af09. Their claims are not independent validation.