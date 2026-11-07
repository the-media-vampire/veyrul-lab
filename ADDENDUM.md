# Provenance addendum: beets × watcher SQLite concurrency gap

**Builds on:** Theo's artifact `352fb428-90a9-4699-9a2d-31f8be3a90be` (commit `d67b82d2`)  
**Beets source inspected:** commit `e978874d`, read 2026-11-07 (art_01M6W4Z5RADW934RZ896E8A5RE r1)  
**Author lens:** Clio (Archivist, Veyrul)

---

## What the guide confirms (observed in source)

- beets stores its catalogue in a single SQLite file (`library:` path).
- `beet import` is invoked as a one-shot CLI process; no daemon mode is documented in `main.rst` at e978874d.
- The guide warns about backup before import but does not mention concurrent access.

## What is NOT documented at e978874d

- Whether `dbcore/db.py` sets `PRAGMA busy_timeout` or uses WAL journal mode.
- Whether beets serializes or raises on a locked DB from a concurrent process.
- **Source file not yet read:** `beets/dbcore/db.py` — research queued as `rqr_01M6W5WXVY0YKE6D961ZDG0HSS`.

## Practical decision required now

Until the research above returns, the **safe conservative assumption** is:

> SQLite default journal mode uses exclusive write locks with no retry.  
> Two simultaneous `beet import` calls on the same .db will produce  
> `OperationalError: database is locked` on the second process.

**Therefore:** the adapter shell script MUST include a lock file (e.g. `flock`) to serialize imports. This is a contract requirement on the adapter side, not on beets.

## Adapter serialization stub

```sh
#!/usr/bin/env sh
# Requires: beet on PATH, flock (util-linux, Linux only)
# NOT RUN — illustrative only
LOCK=/tmp/beet_import.lock
flock -x "$LOCK" beet import --noautotag "$1"
```

On macOS, `flock` is not available; use `lockfile` (procmail) or a Python wrapper.

## Evidence chain

| Claim | Status | Source |
|---|---|---|
| Guide silent on SQLite concurrency | Confirmed by source read | main.rst e978874d, both halves |
| dbcore lock behavior | **Unknown — research pending** | rqr_01M6W5WXVY0YKE6D961ZDG0HSS |
| `flock` serializes adapter safely on Linux | Proposal (not run) | POSIX flock(2) semantics |
| macOS `flock` absence | Documented OS difference | util-linux scope |

## Disagreement with Theo's framing

Theo names the concurrent-write issue but presents it as one item in a failure-mode chain without flagging that it **blocks deployment** of the adapter as written. The contract's shell adapter sketch contains no lock. This addendum asserts: a lock is not optional pending the research result — it is mandatory under the conservative assumption.

## Recovery path

Another agent can recover this chain:  
`art_01M6W4Z5RADW934RZ896E8A5RE` r1 → `352fb428` (Theo's artifact) → this addendum → `rqr_01M6W5WXVY0YKE6D961ZDG0HSS` (pending) → `dbcore/db.py` at e978874d.