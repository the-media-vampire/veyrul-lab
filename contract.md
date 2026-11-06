# Integration contract: ffsubsync sync → caption-timing check

## Purpose
Connect two documented workflows:
1. **ffsubsync** (smacke/ffsubsync, commit de310ac6; README says MIT) — fixes global offset.
2. **Caption-timing rules** (art_01M5P66MVH8XS2CQPFSHY6AWDT r1; Netflix/BBC rules) — validates per-event timing.

Neither source says one replaces the other. This contract makes the handoff explicit.

## Interface

| Slot | Producer | Consumer | Format |
|------|----------|----------|--------|
| Input SRT | user | ffsubsync | SRT |
| Reference | video file or reference SRT | ffsubsync | mp4/mkv or SRT |
| Synced SRT | ffsubsync (`-o`) | timing checker | SRT |
| Timing report | timing checker | user | text/JSON |

## Assumptions
- ffsubsync applies a **single global offset**; per-event drift is not corrected.
- `--split-penalty` is experimental (README); do not rely on it in a pipeline without manual review.
- Timing rules (cps, gap, min-duration) are defined in art_01M5P66MVH8XS2CQPFSHY6AWDT r1 for human-timed files; applying them after an automatic sync assumes residual aligner error is within 1–2 frames (not measured).
- The README documents no offset-report output; a check script must parse the SRT itself.

## Failure modes to handle
- ffsubsync `--skip-sync-on-low-quality` exits without writing output; the adapter must detect a missing output file.
- Split mode (`--split-penalty`) may leave a drift breakpoint; the timing check should flag events whose gap to neighbours is anomalous.
- cps or gap violations after sync mean the original SRT text needs editing, not re-syncing.

## License provenance
- ffsubsync: README says MIT (line 8 badge; line 340 explicit statement). LICENSE file has no licence name; both observations are from art_01M6N3Y4A4RTHK7PKXE3ZWES7K r3.
- Timing rules: Netflix and BBC pages (not read here); record is art_01M5P66MVH8XS2CQPFSHY6AWDT r1.
- This contract: MIT.