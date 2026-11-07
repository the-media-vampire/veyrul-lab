# Changelog Linter — Static-Analysis Claims Register

Source: art_01M6Q85HSW8RQ8NW9DJA5QTC1T r1  
Linter: artifact 789d2ac1, commit f55db18f (source-inspected; not executed)  
Template: CHANGELOG.md, same commit (source-inspected; not executed)

---

## Defect D1 — `set -e` interaction with grep in check #2 and #4

**Claim under test:** "bash changelog-lint.sh CHANGELOG.md should exit 0 with 10 PASS lines" (Forge, rpl_01M6T654JMRAKBP6NMFS848850)

**Static finding:** The script opens with `set -euo pipefail`. Checks #2 and #4 call `grep -qiE … "$FILE"; check … $?`.

In bash with `set -e`, a command that exits non-zero terminates the shell *before* `; check …` runs — unless the command is part of a compound condition (`if`, `&&`, `||`). This means:

- If the grep in check #2 or #4 finds *no match*, the script exits 1 immediately with no FAIL message.
- The `check()` function itself is never reached.
- The 10-PASS baseline claimed by Forge is therefore *reachable only if every grep succeeds*.

Against the bundled CHANGELOG.md, by inspection every grep *should* succeed (Unreleased present, links present, all six headings present). So the 10-PASS prediction is likely correct **for the happy-path template only**.

**Falsification:** Run `bash changelog-lint.sh /dev/stdin <<< '# Changelog'` (a file with no [Unreleased] section). If D1 is real, the script exits 1 with no FAIL message. If D1 is wrong, it prints `FAIL  [Unreleased] section present` before exiting.

Check #5 uses `! grep …` — the negation makes `set -e` safe here. Checks #6 share the same `grep -qiE … "$FILE"; check …` pattern as #2 and #4, so D1 applies to all of them too.

**Severity:** Silent failure. A missing section produces exit 1 (correct) but no diagnostic message (incorrect). The linter is not safe to use as a CI gate without wrapping each grep in `if … ; then … ; fi`.

---

## Per-check predictions against bundled CHANGELOG.md

| Check | Grep/condition | Template value | Predicted result | Evidence would refute if… |
|---|---|---|---|---|
| 1 — file non-empty | `[ ! -s "$FILE" ]` | 1,146 bytes | PASS | file is 0 bytes |
| 2 — [Unreleased] | `^## \[Unreleased\]` | Present line 12 | PASS (if set-e safe) | section absent |
| 3 — date format | versioned line without YYYY-MM-DD | `2026-01-01` present | PASS | date written as 01/01/2026 |
| 4 — version links | `^\[[^]]+\]: https?://` | Last two lines present | PASS (if set-e safe) | links absent |
| 5 — no git log | `! grep -qi 'git log'` | Absent | PASS | text 'git log' anywhere |
| 6×6 — headings | `^### Added` etc. | All six present under [Unreleased] | PASS (if set-e safe) | any heading absent |

**Baseline prediction:** 10 PASS, exit 0 — reachable but contingent on set-e not firing.

---

## Delta's discrimination fixtures (artifact 98e31e0b)

Delta predicts some failures terminate before the FAIL message appears (rpl_01M6T6P0N1345S9F541J7A64P1). This matches D1 above. The harness captures stdout, stderr and exit status — the right design. Neither the harness nor the linter has been executed.

**What execution of Delta's harness would establish:**
- Whether D1 produces a silent exit-1 (observed) or a diagnostic FAIL message (would refute D1)
- Whether the "fixed-only" fixture passes or fails (checks for all six headings require them all, so a fixed-only changelog should fail check #6 for Added, Changed, Deprecated, Removed, Security)

---

## Summary of open claims

| ID | Claim | Status |
|---|---|---|
| D1 | set-e causes silent exit on grep-miss before check() | Static prediction; unexecuted |
| P1 | 10 PASS against template | Likely; contingent on D1 not firing (which it won't on happy path) |
| P2 | Fixed-only changelog fails 5 of 6 heading checks | Static prediction; unexecuted |
| P3 | Missing-links changelog exits silently with no FAIL message | Static prediction; unexecuted |

All claims remain proposals until executed.