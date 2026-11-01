# Passage-tag contract

Source: art_01M6CR2K2FYD0F71ZB5SPNR2AA revision 1.

| Tag | Handled by | Behaviour | CI adapter gap |
|---|---|---|---|
| `Twine.private` | Extension build only | Passage omitted from built HTML | Must be stripped in pre-filter (see ci-adapter.sh) |
| `tt3-disable:<codes>` | Extension diagnostics only | Suppresses listed error codes for that passage | No Tweego equivalent; ignore in CI |

## Interface boundary

```
[.twee source] → [Extension build / Tweego CLI]
                       ↑
              tt3.config.json (extension)
              tweego flags   (CI adapter)
```

The two sides share the same source layout and format-dir convention.
Divergences: passage-tag semantics, disabledDiagnostics, and Watch mode
are extension-only; they have no Tweego equivalent.

## License and provenance
- Extension (sgranade/twine-twee-language): MIT, per package.json and LICENSE
  at commit 37c487df (named; not interpreted).
- Tweego: separate project with its own licence; not read.
- This contract: MIT (this artifact).

## Open questions (sent to research queue separately)
- Does Tweego honour any passage-tag convention analogous to Twine.private?
- Which Tweego version is assumed by the extension at 1.1.5?