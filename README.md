# shot_clause_check v2

Orientation-rule reinforcement checker for multi-shot AI video prompts.

## Why

From art_01M6815JBN1Q0KJ0FNYFG9B38R r1: a rule restated in 2 positions
(global orientation section + post-shot physics law) did not prevent a
mismatch in one sampled frame. The recipe skeleton's fix: also state the
facing rule **inside the shot's own action list**.

This script scores how many of three reinforcement positions contain a
given orientation keyword:

1. `orientation_section` — global orientation/geography block
2. `shot_action_list` — the individual shot's action list
3. `physics_law` — post-shot physics law section

Fully reinforced = all three. Risk: HIGH (<2), MEDIUM (2), LOW (all 3).

## Confirmed execution

- v1 run: artifact `22acc437` (exit 0) — revealed hyphen-matching bug:
  `"screen-face"` in shot action list didn't match keyword `"screen face"`.
- v2 run: artifact `622313e3` (exit 0) — `normalise()` collapses hyphens;
  all three cases score correctly.

| Case | Hits | Risk | Fully reinforced |
|---|---|---|---|
| law only | 1 | HIGH | False |
| orientation + law | 2 | MEDIUM | False |
| all three | 3 | LOW | **True** |

## Limits

- Keyword matching only; synonyms and paraphrases are not caught.
- Caller supplies plain-text strings; no prompt file parser included.
- A LOW score does not guarantee model compliance; it only confirms
  the rule appears in all three positions in your written prompt.
- Three synthetic test cases, not a benchmark over real prompts.

## Next improvement

Replace keyword regex with colour/orientation-name embedding lookup so
`screen-side` matches `screen face` and `toward lens` matches `facing camera`.