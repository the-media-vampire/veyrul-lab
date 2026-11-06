# bisect.sh — Desk-Audit Verification Checklist

Artifact under test: `b7a41532-e592-4bea-a2f9-ac72c2dd0309`  
Source record: `art_01M6JVW9DS5T7W9T9659ARG0S2` rev 2 (Veyrul)  
Documentation commit: Comfy-Org/docs `4a9f856b`  
Script status at time of this audit: **source-published, not executed**.

---

## Claim table — what would falsify each improvement?

| # | Claim (from artifact README) | Test observation required | Falsified if |
|---|---|---|---|
| C1 | `start` writes a timestamped tar.gz backup before moving anything | Run `start`, confirm tar.gz exists in staging dir **before** any folder has moved | Tar.gz absent, or created after first move |
| C2 | JSON session file records staged list and round history | After `bad` or `good`, inspect JSON; confirm moved folders listed and round count incremented | JSON absent or stale after command |
| C3 | `reset` restores all staged nodes | Move 3+ nodes via `bad`, run `reset`, confirm all folder names present in `custom_nodes` and absent from staging | Any folder missing from `custom_nodes` after reset |
| C4 | Script prints suspect name when one folder remains | Iterate until 1 folder in active set; confirm stdout names it without ambiguity | Script exits silently or prints wrong path |

---

## Setup (minimum viable)

```bash
# 1. Create a scratch tree — no live ComfyUI install needed for C1–C4
mkdir -p /tmp/cn_test/custom_nodes /tmp/cn_staging
for n in alpha beta gamma delta epsilon; do
  mkdir /tmp/cn_test/custom_nodes/$n
done

# 2. Download bisect.sh from artifact commit
curl -O https://raw.githubusercontent.com/the-media-vampire/veyrul-lab/\
1df4479236bdf23d9abaf7f93dfe62fba49e5145/bisect.sh
chmod +x bisect.sh
```

---

## Protocol per claim

### C1 — backup timing
```bash
./bisect.sh start /tmp/cn_test/custom_nodes /tmp/cn_staging
# RECORD: timestamp of tar.gz vs timestamp of first moved folder
ls -lt /tmp/cn_staging | head -6
```
Pass: tar.gz mtime is earlier than any moved folder mtime.

### C2 — session JSON
```bash
./bisect.sh bad
cat /tmp/cn_staging/bisect_session.json   # or equivalent path
```
Pass: file exists, `staged` array non-empty, `history` has one entry.

### C3 — reset fidelity
```bash
# From state after at least one bad/good round
./bisect.sh reset
diff <(ls /tmp/cn_test/custom_nodes | sort) <(echo -e 'alpha\nbeta\ngamma\ndelta\nepsilon' | sort)
```
Pass: diff is empty.

### C4 — suspect identification
```bash
# Keep calling bad/good until one folder remains
# Confirm terminal output includes the folder name
```
Pass: printed name matches the sole remaining folder in custom_nodes.

---

## Known limits (from artifact README, confirmed by desk read)

- Not tested on a live ComfyUI install (this protocol also does not test live ComfyUI).
- Symlinks in `custom_nodes` are not handled; add symlink folders to test if needed.
- Staging dir should be on the same partition as `custom_nodes`; cross-partition moves may behave differently.
- Windows Portable not supported without WSL.

---

## Two-state confirmation (from artifact README, unautomated)

After identifying the suspect:
1. Disable **only** the suspect node; start ComfyUI; confirm issue **absent**.
2. Re-enable it; restart; confirm issue **returns**.

This is what turns a bisect result into a confirmed finding.
Neither the script nor this checklist automates it.

---

## Next improvement flagged

The artifact README notes alphabetical ordering may cluster related nodes.
A random shuffle before splitting is a one-line change.
If C1–C4 all pass on the scratch tree, that shuffle change is the logical next PR.