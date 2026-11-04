# write_good_lint.py

Report-only Python replica of the eight write-good rules bundled with [Vale](https://vale.sh).

## Source

Rule names, levels and check types from **art_01M6JYTD4PWJ0G1JBGM1Z6QXQR r1** (Veyrul).
Word/phrase lists are representative samples; the full Vale write-good package carries longer lists.

## Rules and levels

| Rule | Level | What it flags |
|---|---|---|
| Passive | warning | `(was/were/is/are/been/be) <word>ed` |
| Weasel | warning | Hedging/intensifying words (clearly, very, …) |
| TooWordy | warning | Wordy multi-word phrases |
| ThereIs | error | Sentences opening with *There is/are* |
| So | error | Sentences opening with *So* |
| E-Prime | suggestion | Forms of *to be* |
| Illusions | warning | Doubled words (*the the*, *needs needs*) |
| Cliches | warning | Stock phrases (*bite the bullet*, …) |

## Design note

No automatic rewrites. The source records that the repeated-word rule carries an `edit/truncate` action in real Vale; this tool deliberately omits it so author choices survive the pass.

## Usage

```bash
python write_good_lint.py chapter01.md
```

Or import:

```python
from write_good_lint import lint
for f in lint(open('chapter01.md').read()):
    print(f.line, f.rule, f.message)
```

## Limits

- Word lists are samples; the real write-good package lists are longer.
- Passive detection covers only regular `-ed` endings; the full rule ships a large irregular past-participle list.
- Not tested against real Vale output — differences are expected at the word-list boundary.
- Fiction: rule firings on deliberate passive, repetition or sentence openers are author choices, not errors.