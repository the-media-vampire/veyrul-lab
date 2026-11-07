"""Staleness guard for evidence_manifest.json.
Usage: python check_staleness.py evidence_manifest.json [--release-on YYYY-MM-DD]
Exit 0 only if every entry has a read_date within 30 days of today (or release_on).
Does not validate record.json; pair with check_decision_v5.py.
Our rules, not legal advice."""
import json, sys, re
from datetime import date, timedelta

ISODATE = re.compile(r'\d{4}-\d\d-\d\d')
WINDOW = timedelta(days=30)
REQUIRED = ('part', 'source_url', 'read_date', 'reader',
            'sha256_or_etag', 'licence_id_quoted')
FILL = re.compile(r'^FILL', re.I)

def main():
    args = sys.argv[1:]
    if not args:
        print('usage: check_staleness.py manifest.json [--release-on YYYY-MM-DD]')
        sys.exit(2)
    manifest_path = args[0]
    anchor = date.today()
    if '--release-on' in args:
        idx = args.index('--release-on')
        try:
            anchor = date.fromisoformat(args[idx + 1])
        except (IndexError, ValueError):
            print('ERROR: --release-on requires a YYYY-MM-DD date')
            sys.exit(2)

    with open(manifest_path) as f:
        manifest = json.load(f)

    entries = manifest.get('entries', [])
    errors = []
    for e in entries:
        part = e.get('part', '?')
        for field in REQUIRED:
            val = str(e.get(field, ''))
            if not val or FILL.match(val):
                errors.append(f'{part}: {field} is missing or unfilled')
        rd = e.get('read_date', '')
        if ISODATE.fullmatch(rd):
            read = date.fromisoformat(rd)
            age = (anchor - read).days
            if age < 0:
                errors.append(f'{part}: read_date {rd} is in the future')
            elif age > 30:
                errors.append(
                    f'{part}: read_date {rd} is {age} days before {anchor} '
                    f'(limit 30) — reread required')
        else:
            if f'{part}: read_date is missing or unfilled' not in errors:
                errors.append(f'{part}: read_date must be YYYY-MM-DD, got {rd!r}')

    if errors:
        print('STALE OR INCOMPLETE evidence_manifest.json:')
        for e in errors:
            print(' ', e)
        sys.exit(1)
    print(f'OK: all {len(entries)} entries read within 30 days of {anchor}')
    sys.exit(0)

if __name__ == '__main__':
    main()