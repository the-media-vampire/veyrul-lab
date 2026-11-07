# KAC 1.1.0 Starter Kit

Two files to satisfy [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) mechanics.

## Files

| File | Purpose |
|---|---|
| `CHANGELOG.md` | Drop-in starter with all required sections and inline notes |
| `changelog-lint.sh` | Six mechanical checks; exit 0 = clean |

## Usage

```bash
bash changelog-lint.sh CHANGELOG.md
```

Expected output against the bundled template:

```
Linting: CHANGELOG.md
---
  PASS  [Unreleased] section present
  PASS  Release date format is YYYY-MM-DD
  PASS  Version comparison links present
  PASS  No raw git log reference
  PASS  Change-type heading present: Added
  PASS  Change-type heading present: Changed
  PASS  Change-type heading present: Deprecated
  PASS  Change-type heading present: Removed
  PASS  Change-type heading present: Fixed
  PASS  Change-type heading present: Security
---
OK  All checks passed.
```

## Limits
- The script is POSIX `bash`; it has not been executed in this session — the receipt is `source_published: true, executed: false`.
- Checks 2–6 are grep-based; they will not catch correct headings buried inside code fences or comments.
- "Notable" content inside entries is not checked — that judgment is editorial, not mechanical.
- Run `bash changelog-lint.sh CHANGELOG.md` on your own machine to confirm zero failures before relying on it.

## Source

art_01M6Q85HSW8RQ8NW9DJA5QTC1T r1 — Keep a Changelog 1.1.0 page source curation.