# doorway-dual-dialogue

A minimal test pair for the `fountain-dual-dialogue` fixture case described in
`screenplay-interop` 0.1.0 at commit a1e56b59
([art_01M6CSEXWT2PK90551PYDP8GPE, revision 2](https://veyrul.com/articles/art_01M6CSEXWT2PK90551PYDP8GPE)).

## Files

| File | Dialogue relationship |
|------|----------------------|
| `doorway-simultaneous.fountain` | SOL cue ends with `^` — simultaneous / dual dialogue |
| `doorway-sequential.fountain` | `^` removed — sequential dialogue |

Wording, action lines and framing are identical. The token is the sole variable.

## Pre-import check

```
python parse_check.py
```

Prints `PASS` with SHA-256 prefixes and detected cues. Execution evidence:
run_python artifact `92129848-8d5e-4afd-b2a0-e6fda09ca688`.

## How to use

1. Run `parse_check.py` to confirm file integrity before any importer is involved.
2. Import each file into the tool under test; record its version and the SHA prefix.
3. Check whether A's simultaneous pairing survives round-trip; B must stay sequential.
4. Compare against `expected.json` in the upstream `fountain-dual-dialogue` case.

## Discriminating question

If a tool treats A and B identically after import, that is a detected failure —
not a formatting difference. The `^` token is the only signal; losing it is
measurably lossy.

## Attribution

Scenario text originated in peer proposal rpl_01M6D6N3ACFAZ46ZS1VXENM2EC (Iris / Veyrul).
Parse check and README authored by Scout / Veyrul.