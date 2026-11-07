# DVC ↔ Mixxx Session Integration Contract

## Interface boundary

| Side | Unit | Mechanism |
|------|------|-----------|
| DVC (source) | `assets/stems/*.mp3` or `.wav` | Content-addressed cache; version pinned by `.dvc` pointer file committed in Git |
| Mixxx (consumer) | Library directory path | Mixxx scans a directory at startup; it does NOT track file identity by hash |

The only handshake is a **filesystem path**. DVC materialises files there;
Mixx reads whatever is present. This is both the whole interface and the
whole risk: if the path is populated by the wrong DVC version, Mixxx has no
way to detect it.

## Mechanism chain

```
git checkout <tag>          # pin pointer file to known version
dvc checkout                # materialise that version into assets/stems/
# Mixxx is then opened — it reads assets/stems/ as its library source
mixxx --settingsPath ./mixxx-profile   # optional: isolated profile per session
```

The two commands are the entire adapter. No format conversion is needed
because DVC stores files verbatim (no transcoding).

## Assumptions to test before trusting this in practice

1. **Mixxx library DB vs. filesystem**: Mixxx builds an internal SQLite
   library. If you switch DVC version while Mixxx is open (or while its DB
   already holds the previous path/hash), Mixxx may show stale metadata.
   Mitigation: close Mixxx, run `dvc checkout`, then reopen.

2. **Mixxx re-analysis on filename collision**: if a stem keeps the same
   filename across DVC versions (common), Mixxx may serve cached BPM and
   beatgrid from the previous version. The manual says analysis runs "the
   first time a track is loaded in a deck" (art_01M6N9PCZTJSX3MA9442WEFFDX
   rev 3, source-documented). Mitigation: delete `mixxxdb.sqlite` or force
   re-analysis after a DVC version switch.

3. **DVC pointer file must be committed**: a floating `dvc add` without a
   git commit cannot be reliably reproduced. The contract is only as stable
   as the Git tag or commit SHA used in step 1.

4. **Remote availability**: `dvc pull` is required on a fresh clone before
   any files exist in the working tree. Mixxx opened before `dvc pull`
   completes will find an empty directory.

## Provenance and licence

- DVC workflow: art_01M6V62C789085HJEBKN2AADB8 rev 1; source docs at
  commit 21fabba8 (Apache-2.0). Commands not run; outputs expected.
- Mixxx workflow: art_01M6N9PCZTJSX3MA9442WEFFDX rev 3; source is Mixxx
  manual RST files; no licence file was staged (see article rights).
- Your audio files carry their own licences — neither DVC nor Mixxx
  changes those terms.

## Missing evidence (not yet verified)

- Whether Mixxx exposes a CLI flag or config to force full re-analysis
  on library rescan (would make the rollback step safer).
- Whether `dvc checkout` on a directory correctly restores deleted files
  that existed in an earlier version but not the current one (directory
  rollback semantics, not tested in source docs).