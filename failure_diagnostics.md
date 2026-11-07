# hf CLI failure-mode diagnostic scaffold

Source: art_01M6V3QCJ14FJA43G1632JNGJS revision 1  
Companion to: db24f4ac-32f8-4c45-9a6a-d5f616478911 (Scout, filter-composition)

> **Not executed.** Commands are proposals derived from source-documented behaviour.
> Run each probe and record actual stdout/stderr; replace the EXPECTED lines with what you observe.

---

## Failure 1 — `hf: command not found`

**Probe:**
```sh
hf --version 2>&1; echo "exit:$?"
```
**Expected symptom:** shell prints `hf: command not found` and exit code is non-zero.  
**Repair (source-documented):** install via the standalone installer or `pip install -U huggingface_hub`, then re-run the probe.  
**Observed (fill in):** ___

---

## Failure 2 — 401 / access denied on gated repo

**Probe:**
```sh
hf download meta-llama/Llama-2-7b --dry-run 2>&1 | head -20
```
Use a known-gated repo (accept or reject the licence first to control the state).  
**Expected symptom:** output contains `401` or `Access denied` or `gated`.  
**Repair (source-documented):** `hf auth login` then retry, or pass `--token $HF_TOKEN`.  
**Observed (fill in):** ___

---

## Failure 3 — Timeout on slow connection

**Probe (force a short timeout):**
```sh
HF_HUB_DOWNLOAD_TIMEOUT=1 hf download OWNER/REPO --dry-run 2>&1 | tail -5
```
Substitute a repo with large metadata; a 1-second timeout should trigger on most connections.  
**Expected symptom:** `TimeoutError` or `ReadTimeout` in stderr.  
**Repair (source-documented):** unset the env var or raise it: `export HF_HUB_DOWNLOAD_TIMEOUT=120`.  
**Observed (fill in):** ___

---

## Failure 4 — Pattern matched nothing (or too much)

**Probe A — nothing matched:**
```sh
hf download OWNER/REPO --include "*NOMATCH*.gguf" --dry-run 2>&1
```
**Expected symptom:** zero files listed, or a message indicating no files match.  
**Probe B — too much matched:**
```sh
hf download OWNER/REPO --include "*.gguf" --dry-run 2>&1 | wc -l
```
Compare line count against the count with a tighter pattern.  
**Repair (source-documented):** adjust `--include`/`--exclude` and re-run `--dry-run` until the listing is correct.  
**Observed (fill in):** ___

---

## Failure 5 — Unexpected commit (unpinned revision)

**Probe — unpinned then pinned, diff the file lists:**
```sh
hf download OWNER/REPO --dry-run 2>&1 > unpinned.txt
hf download OWNER/REPO --revision COMMIT_HASH --dry-run 2>&1 > pinned.txt
diff unpinned.txt pinned.txt
```
**Expected symptom:** diff is non-empty when the repo has changed since `COMMIT_HASH`.  
**Repair (source-documented):** always pass `--revision` with a commit hash in automated scripts.  
**Observed (fill in):** ___

---

## Recording template

| Failure | Probe exit code | Key stderr line | Repair applied | Result after repair |
|---------|----------------|----------------|----------------|--------------------|
| 1 cmd not found | | | | |
| 2 401 gated | | | | |
| 3 timeout | | | | |
| 4 pattern | | | | |
| 5 revision | | | | |