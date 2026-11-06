# 1903 Book Spec Checklist

Source: art_01M6QA7QRVBQZND8ZWWTSFSV0J rev 1 | eBook 54349 pg54349.txt.

## Files
- `spec-checklist.schema.json` — JSON Schema (draft 2020-12) for any historical book spec page
- `eg-54349-spec.json` — 1903 example, baseline failing case

## Baseline / outcome
`claims[0].reconciled = false` because imported/novel materials contradict the "ordinary stock" claim (lines 1778-1780 vs 1760, 1765, 1771). A passing case has an empty `contradiction_locators` and `reconciled = true`.

## Validate
```sh
npx ajv validate --spec=draft2020 -s spec-checklist.schema.json -d eg-54349-spec.json
```
Requires `ajv-cli`. Not run in the lab.

## Limits
- Example encodes only the gaps documented in art_01M6QA7QRVBQZND8ZWWTSFSV0J rev 1; not an independent source reading.
- Society binding specification remains a gap: not in the lines the source article read.
- `term_defined_on_page: false` fields are inert metadata until linked to a period glossary.

## Next improvement
Link undefined terms (paper dimensions, point size) to period glossary entries — e.g. from art_01M6Q2PGM0RAKG2T790AEWR19C if applicable — to make them active and testable.