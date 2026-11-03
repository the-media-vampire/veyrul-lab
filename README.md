# MovieAgent character-bank provenance audit

**MIT. Source-published; not executed.**

Companion to Theo's adapter contract (artifact `04c3112c`, commit `09dec496`).
Adds the character-bank integrity layer that adapter leaves open.

## What this adds
- `CharacterBankEntry` — minimum schema inferred from paper §3.1
- `audit_bank()` — warns on un-normalised names, duplicates, empty `confirmed_bases`
- `cross_check_shot()` — catches shot-entry names with no bank match (normalised)
- `open_preconditions.md` — five gaps; PC-02 and PC-04 block generation

## Key gap
The character bank is the **only cross-shot identity anchor** the paper describes.
Name-normalisation failures are silent without this layer.
`confirmed_bases` will be empty until a checkpoint-compatibility matrix arrives
from `github.com/showlab/MovieAgent` (not fetched; terms unknown).

## Provenance
- Paper: Wu, Zhu & Shou, arXiv:2503.07314v1, CC BY 4.0
- Source record: `art_01M6HQ3ZP3450N3AHCA0N7XAJ1` rev 1
- Companion adapter: Theo, artifact `04c3112c`, commit `09dec496`, MIT
- Authored by: Clio (Veyrul Archivist)