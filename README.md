# beets × watcher integration contract

Documentary adapter. Not run. Commands follow beets commit e978874d (art_01M6W4Z5RADW934RZ896E8A5RE r1).

## Interface table

| Side       | Interface            | Type          | Notes |
|------------|----------------------|---------------|-------|
| Watcher    | stdout / exit code   | text stream   | emits absolute directory paths, one per line |
| Adapter    | stdin → beet import  | shell pipe    | validates path, calls beet import |
| beets      | YAML config file     | file          | directory, library, import.copy, import.write |
| beets      | exit code 0 / non-0  | process       | 0 = success; adapter must check |

## Assumptions to verify before combining

1. **beets is on PATH** after `uv tool install beets`; watcher runs in the same shell environment.
2. **Config is read-only style** (copy: no, write: no) or the caller deliberately accepts mutations.
3. **Watcher fires on directory-complete events**, not mid-copy; partial directories corrupt the import.
4. **Single-consumer**: beets holds an exclusive lock on the SQLite library file; two concurrent imports will fail.
5. **Path encoding**: both sides must agree on UTF-8 paths; filenames with spaces or special chars need quoting.

## Failure modes (cause → consequence)

- Watcher fires before copy completes → beet import sees partial album → incomplete library entry, no clean rollback.
- Two watcher events fire simultaneously → second `beet import` hits locked DB → non-zero exit, silently dropped.
- Config file absent or malformed YAML → beets exits non-zero on every call → watcher loop floods logs.
- Tool bin not on PATH in cron/systemd context → `beet: command not found` → silent failure unless adapter checks exit code.

## Minimal adapter shell sketch (documentary)

```sh
#!/usr/bin/env sh
# watch-import.sh — untested sketch
# Requires: inotifywait (inotify-tools) or equivalent; beets installed via uv tool
# License: MIT

WATCH_DIR="${1:?usage: watch-import.sh <drop-dir>}"

inotifywait -m -e close_write,moved_to --format '%w%f' "$WATCH_DIR" | \
while IFS= read -r path; do
  # Only act on directories (music drop folders)
  [ -d "$path" ] || continue
  echo "[adapter] importing: $path"
  beet import --noautotag "$path"
  if [ $? -ne 0 ]; then
    echo "[adapter] FAILED: $path" >&2
  fi
done
```

## Provenance and licenses

- beets: MIT License, Adrian Sampson and contributors. Source: art_01M6W4Z5RADW934RZ896E8A5RE r1.
- inotify-tools: GPL-2.0. **License mismatch**: this adapter shell script is MIT, but the tool it calls (inotifywait) is GPL. The script does not link or bundle inotify-tools; it invokes it as a subprocess. Shell invocation is generally considered separate. Verify your use case.
- watchman (Facebook): MIT License — a GPL-clean alternative if that matters.
- This file: MIT.

## Integration contract (summary)

```
PRECONDITION:  drop dir contains a complete album directory
CALL:          beet import --noautotag <dir>
POSTCONDITION: tracks appear in `beet ls`; DB file updated
FAILURE:       non-zero exit; DB unchanged (beets is transactional per import)
SIDE EFFECTS:  none if copy:no, write:no; files moved/copied if other import styles
```