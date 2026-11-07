# Interface map: check_decision_v5 ↔ CI pipeline

## Data flow

```
You (human)
  reads primary licence source → writes record.json
        ↓
check_decision_v5.py  (pure function, no network, no clock)
  validates schema + logic → stdout JSON + exit code
        ↓
gate.sh  (thin shell boundary)
  wraps exit code → pass/block signal
        ↓
CI platform  (GitHub Actions / GitLab CI / etc.)
  blocks deployment on non-zero
```

## Failure propagation

| Failure point              | Effect                                | Recovery                              |
|----------------------------|---------------------------------------|---------------------------------------|
| Weights licence not read   | status=unknown → decision=hold → exit≠0 | Read the file, update record          |
| Qwen upstream unread       | same as above                         | Read upstream repo licence            |
| CC-BY-NC detected          | status=stop → exit≠0                 | Switch model or obtain commercial licence |
| Distributor refusal wording | status=stop → exit≠0                | Switch distributor or route           |
| read_on > 30 days old      | checker error → exit≠0               | Re-read sources, update dates         |
| record.json missing a part | checker error → exit≠0               | Add the missing part                  |

## Assumption: the checker is stable

The checker is pinned to art_01M6SQH2ECQZH73P9EP9XHKB47 r1.
If the article is revised, re-read the new checker code before updating the gate.
The adapter does not parse checker output: it only forwards the exit code.

## What the adapter cannot do

- Verify that quotes are genuine text from the named source.
- Re-read a licence automatically.
- Apply to models or checkpoints not listed in the record.
- Give legal advice.