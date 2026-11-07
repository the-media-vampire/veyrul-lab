# music-model-decision-provenance

Staleness guard and evidence manifest template to accompany
`check_decision_v5.py` (art_01M6SQH2ECQZH73P9EP9XHKB47 r1) and
Theo's CI gate (artifact a13eda04, commit efd62dbe).

## What this adds

The article says: *"read every page again within 30 days before release."*
The checker cannot enforce this — it has no clock and no network access.
This package adds the enforcement layer:

- **`evidence_manifest.json`** — one record per licence read: URL, file path,
  date, reader role, hash/ETag, quoted licence ID.
- **`check_staleness.py`** — exits non-zero if any entry is unfilled, missing,
  or older than 30 days (or older than `--release-on` minus 30 days).

## Integration with Theo's gate

Add one step before `gate.sh`:

```yaml
- name: Check evidence staleness
  run: python check_staleness.py evidence_manifest.json --release-on ${{ inputs.release_on }}
```

If this step fails, `gate.sh` never runs. The two layers are independent:
staleness check owns evidence recency; `check_decision_v5.py` owns
licence logic.

## What this does NOT do

- Cannot verify that a quote is real (same gap as the checker).
- Cannot fetch or hash remote files; the reader must supply `sha256_or_etag`.
- Does not replace reading the licence. A human must read; this records that they did.

## Open gaps (not closed here)

- Qwen3-1.7B upstream licence (research queued: rqr_01M6ST0YA9RE9JHE5GPZS8PN5A)
- Stable Audio Open Community License (gated at read time)

## License
MIT