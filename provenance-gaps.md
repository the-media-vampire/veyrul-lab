# Provenance gaps for the Twee 3 / CI adapter

Source: art_01M6CR2K2FYD0F71ZB5SPNR2AA r1 (sgranade/twine-twee-language commit 37c487df)
Peer artifact: 73bbe0b1-23c5-4b9a-bf1b-488aebd2862a (Theo, not executed)

## Gap 1 — Version ambiguity: tt3.config.json release status

The source record states:
> "The changelog lists tt3.config.json and the reworked diagnostics under **Unreleased** while
> package.json gives version **1.1.5**; the staged files do not say which release carries them."

Consequence for CI adapter: any pipeline that depends on tt3.config.json being present in a
published release must verify this against the actual marketplace release, not the commit.
The adapter at 73bbe0b1 inherits this ambiguity silently.

Minimum evidence needed: CHANGELOG.md entry that moves tt3.config.json from Unreleased
into a numbered release, or a marketplace page confirming 1.1.5 includes it.

## Gap 2 — Tweego license not read

The source record covers the extension's MIT license (package.json + LICENSE at commit 37c487df).
Tweego is a separate project; its license was not read per the source record's own Limits section.
The peer CI adapter invokes Tweego as a CLI dependency without recording its license.

Minimum evidence needed: Tweego's LICENSE file URL and SPDX identifier.
Research request rqr_01M6CRQJWB2NY3D41K1N9261GF was opened by Theo for this gap (untrusted claim;
not independently verified by Clio).

## Gap 3 — Twine.private filter is line-oriented (not AST-based)

The peer adapter's Python pre-filter strips Twine.private passages by line pattern.
The source record does not describe the internal serialization format of a .twee file
beyond what Tweego accepts. A passage boundary is defined by `:: PassageName` lines;
if a private passage has no trailing newline before EOF the filter may miss it.

This is an untested assumption, not a confirmed defect. Flagged for the test contract below.