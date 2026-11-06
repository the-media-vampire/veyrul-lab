# TimelineJS Observation Sheet

Companion to Scout artifact `933c013a-a5a4-4345-8c33-9d6aaeaf3558` (commit `b51d844`).
Source: `art_01M6K4N37MCKDM0TZB5V9ZGS30` revision 3.

## Purpose

Scout's brief defines **what to test** (Experiment A: unique_id stability; Experiment B: repeat-per-strand rendering).  
This sheet defines **what to record** so two different testers can compare results without prose ambiguity.

## How to use

1. Serve `index.html` (or any TimelineJS local instance) pointing at the fixture file listed in each row.
2. Open `observation_log.csv` and fill in the OBSERVED_* columns only — do not edit FIXTURE or STEP columns.
3. Treat every OBSERVED cell as either a literal string, a pixel measurement, or one of the coded values listed in `codebook.md`.
4. If a cell cannot be determined (e.g. element not found), write `NOT_FOUND`.

## Thresholds (proposals — record what you used)

- URL hash stability: hashes match character-for-character across reload = STABLE; any difference = CHANGED.
- Strand label visibility: both group labels appear in nav bar = BOTH; only one = ONE; none = NONE.