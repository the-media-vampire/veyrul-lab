# hf CLI dry-run filter experiment brief

Source: art_01M6V3QCJ14FJA43G1632JNGJS revision 1  
Version context: huggingface_hub commit fd5dccbb (2026-11-07)

## Falsifiable question

Does `--include "*.gguf"` alone produce the same dry-run file list and byte total
as `--include "*.gguf" --exclude "*fp16*"` when the repo contains fp16 GGUF files?

- **H0 (no surprise):** totals differ by exactly the size of fp16 files; both arms
  behave as documented and independently composable.
- **H1 (interesting):** totals are identical (fp16 pattern was already absent from
  the include set, making `--exclude` a no-op — useful to confirm).
- **H2 (surprising):** totals differ in an unexpected direction, suggesting
  pattern-precedence or glob-expansion behaviour not covered by the guide.

## Held variables

- Same repo ID both runs
- Same `--revision` pin (use a commit hash, not `main`, to freeze the file list)
- Same machine, same `HF_HOME` / cache state
- Only the filter flags change between arms

## Commands

```sh
REPO="OWNER/REPO"          # replace with a public GGUF repo
REV="<commit-hash>"        # pin to freeze the file list

# Arm A: include only
hf download "$REPO" --include "*.gguf" --revision "$REV" --dry-run 2>&1 | tee arm_a.txt

# Arm B: include + exclude
hf download "$REPO" --include "*.gguf" --exclude "*fp16*" --revision "$REV" --dry-run 2>&1 | tee arm_b.txt

# Compare summary lines
grep -E '(files|bytes|MB|GB)' arm_a.txt arm_b.txt
diff arm_a.txt arm_b.txt
```

## What to record (observations, not taste)

| Field | Arm A | Arm B |
|---|---|---|
| Files listed | | |
| Bytes reported | | |
| Any fp16 files in Arm A? | | n/a |
| Diff output | | |
| hf version (`hf --version`) | | |

## Discriminating outcome

- **Diff is empty:** repo had no fp16 GGUFs; re-run with a repo that does.
- **Diff removes fp16 lines only:** H0 confirmed; filters compose independently.
- **Diff shows other differences:** document exactly which lines differ — this is the
  surprising result worth reporting back.

## If it fails

- `hf: command not found` — install per the guide (pip or standalone installer).
- Pattern matched nothing — widen `--include`, confirm filenames with `--dry-run`
  and no filter first.
- Revision not found — omit `--revision` for a first pass, then pin once you
  have a valid commit hash from the repo's commit history.

## Why this test is informative

The guide documents `--include` and `--exclude` as independent options
(art_01M6V3QCJ14FJA43G1632JNGJS r1) but does not show combined behaviour.
A two-arm dry-run costs zero bandwidth and answers the precedence question
before a multi-GB download is committed.