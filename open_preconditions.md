# Open preconditions before any generation call

Source: `art_01M6HQ3ZP3450N3AHCA0N7XAJ1` rev 1.

| ID | Description | Status | Minimum evidence needed |
|----|-------------|--------|--------------------------|
| PC-01 | Character-bank machine-readable schema | Open | Fetch `github.com/showlab/MovieAgent`; terms unknown |
| PC-02 | Checkpoint compatibility per character (`confirmed_bases`) | **Blocking** | Per-character compatibility row from upstream repo |
| PC-03 | No inter-level confirmation hook; planning rationale absent from shot entries | Open | Confirm whether released code adds a hook; story-bible human-gate is our design only |
| PC-04 | Generator API schema (`shot_to_prompt()` emits plain string; structured APIs differ) | Blocking | Read generator API docs before wiring |
| PC-05 | Audio/voice components | Held | Intentionally out of scope per source record |

PC-02 and PC-04 are the minimum blocking gaps before any generation attempt.
See Clio memory `2c8752f2` and research request `rqr_01M6FGTBDWFF166S18JZ36MGJ6` for PC-02 lineage.