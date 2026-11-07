#!/usr/bin/env bash
# changelog-lint.sh — checks five mechanical failures KAC 1.1.0 calls bad practices.
# Source: art_01M6Q85HSW8RQ8NW9DJA5QTC1T r1
# Usage: bash changelog-lint.sh [path/to/CHANGELOG.md]
# Exit 0 = no failures found; exit 1 = one or more failures.

set -euo pipefail

FILE="${1:-CHANGELOG.md}"
FAILS=0

check() {
  local desc="$1" result="$2"
  if [ "$result" -eq 0 ]; then
    echo "  PASS  $desc"
  else
    echo "  FAIL  $desc"
    FAILS=$((FAILS + 1))
  fi
}

echo "Linting: $FILE"
echo "---"

# 1. File must exist and be non-empty.
if [ ! -s "$FILE" ]; then
  echo "  FAIL  File missing or empty: $FILE"
  exit 1
fi

# 2. Must have an [Unreleased] section (KAC 1.1.0 lines 100-110).
grep -qiE '^## \[Unreleased\]' "$FILE"; check "[Unreleased] section present" $?

# 3. Must NOT use an ISO date in an unsupported format; require YYYY-MM-DD on release lines.
#    Bad: ## [1.0.0] - 01/01/2026 or ## [1.0.0] - January 1 2026
#    Good: ## [1.0.0] - 2026-01-01
#    Check: any versioned release line must match YYYY-MM-DD.
bad_dates=$(grep -E '^## \[[0-9]' "$FILE" | grep -vE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | grep -v YANKED || true)
[ -z "$bad_dates" ]; check "Release date format is YYYY-MM-DD" $?

# 4. Must have at least one version link at the bottom (KAC 1.1.0: linkable versions).
grep -qE '^\[[^]]+\]: https?://' "$FILE"; check "Version comparison links present" $?

# 5. Must NOT contain the string 'git log' (commit-log diff dumping — KAC 1.1.0 lines 124-126).
! grep -qi 'git log' "$FILE"; check "No raw git log reference" $?

# 6. Must have all six KAC change-type headings represented at least once total
#    (Added, Changed, Deprecated, Removed, Fixed, Security).
for t in Added Changed Deprecated Removed Fixed Security; do
  grep -qiE "^### $t" "$FILE"; check "Change-type heading present: $t" $?
done

echo "---"
if [ "$FAILS" -eq 0 ]; then
  echo "OK  All checks passed."
  exit 0
else
  echo "FAIL  $FAILS check(s) failed."
  exit 1
fi