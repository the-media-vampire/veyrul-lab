# Minimal bad-changelog fixtures for manual testing

These are copy-paste inputs to test against changelog-lint.sh.
Run: `bash changelog-lint.sh <(cat fixture_N.md)`

---

## Fixture 1 — Missing [Unreleased] section

Expected: **silent exit 1** (no FAIL message) if D1 holds; FAIL message if D1 is wrong.

```
# Changelog

## [1.0.0] - 2026-01-01

### Added
- Initial release.

[1.0.0]: https://github.com/example/project/releases/tag/v1.0.0
```

---

## Fixture 2 — Fixed-only changelog (all six headings absent except Fixed)

Expected: PASS for [Unreleased] and links; FAIL×5 for Added/Changed/Deprecated/Removed/Security — or silent exits if D1 fires first.

```
# Changelog

## [Unreleased]

### Fixed
- Corrected a null pointer in the parser.

## [1.0.0] - 2026-01-01

### Fixed
- Initial release corrections.

[Unreleased]: https://github.com/example/project/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/example/project/releases/tag/v1.0.0
```

---

## Fixture 3 — Bad date format

Expected: FAIL on check #3; all others PASS (D1 not triggered because bad_dates is non-empty).

```
# Changelog

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [1.0.0] - 01/01/2026

### Added
- Initial release.

[Unreleased]: https://github.com/example/project/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/example/project/releases/tag/v1.0.0
```

---

## Fixture 4 — git log reference

Expected: FAIL on check #5; all structural checks PASS.

```
# Changelog

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [1.0.0] - 2026-01-01

See git log for details.

### Added
- Initial release.

[Unreleased]: https://github.com/example/project/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/example/project/releases/tag/v1.0.0
```