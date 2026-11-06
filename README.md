# FxNorm-Automix Pre-Run Harness

Companion to Scout artifact `5a438a01`. Source: `art_01M6JV03D8SRF5T8MH86SJWF0N` rev 2. Not executed.

## Run order
```
# Set REPO_ROOT in each script first
python verify_env.py                   # -> env_check.json
python probe_stem_layout_extended.py   # -> stem_layout.json
python collate_prereport.py            # -> pre_run_report.json + CSV row
```

## Exit codes
- `verify_env.py` exit 1: environment not ready; IR sourcing premature.
- `probe_stem_layout_extended.py` exit 1: entry point not found; inspect manually.
- Both pass: proceed to Scout's Condition A vs B.

## Sequencing disagreement with Scout
Scout treats IR quality as the top discriminating variable. This harness argues environment and stem-layout must resolve first — a broken environment makes IR quality untestable by definition. Correct order: environment -> stem layout -> IR substitution.

## Weight terms
Not stated in files read (art_01M6JV03D8SRF5T8MH86SJWF0N rev 2). Confirm before any checkpoint use.