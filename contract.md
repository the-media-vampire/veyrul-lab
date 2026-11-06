# Integration contract: ffsubsync → pysubs2

## Provenance
- ffsubsync: MIT (README badge + line 340); commit de310ac6; source art_01M6N3Y4A4RTHK7PKXE3ZWES7K r2
- pysubs2: MIT (README claim; LICENSE.txt names no licence); commit 6371ae8b; source art_01M6M7RTZQAYHCT8C265GC68C9 r2

## Interface boundary

ffsubsync writes a `.synced.srt` file to disk (or the path given with `-o`).
pysubs2 reads that file with `pysubs2.load(path)` and returns an `SSAFile`
object whose `.events` list exposes each cue's `.start` and `.end` in milliseconds.

The two tools share no in-process interface; the contract is a filesystem path
and the SRT format. That is a stable, low-coupling join point.

## Preconditions
1. ffsubsync must have written a valid SRT to `OUTPUT_SRT` before pysubs2 reads it.
2. The file encodes as UTF-8 (ffsubsync default; verify if the source SRT is legacy-encoded).
3. pysubs2 converts all formats internally to ASS; timing is preserved in ms.

## Failure assumptions
- If ffsubsync exits non-zero, `OUTPUT_SRT` may not exist or may be incomplete.
  The adapter must check the exit code before handing the path to pysubs2.
- ffsubsync's default `--max-offset-seconds 60` silently leaves the file
  unsynced if the true offset exceeds 60 s. pysubs2 will load it without error.
  This is the main silent-failure path in the combined workflow.
- pysubs2 loads a broken SRT without raising on many malformed cues; downstream
  validation must be explicit.

## Explicit assumptions NOT in either README
- Neither tool reports whether sync succeeded or by how much. The user has
  no machine-readable signal from this pipeline beyond the exit code.
- The 10 ms window granularity in ffsubsync sets a floor on timing accuracy
  that pysubs2 cannot improve post-hoc.