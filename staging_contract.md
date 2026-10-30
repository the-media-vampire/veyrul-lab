# Rose-window staging contract (proposal)

Source: art_01M64VKK2MPWCZP03XDVGKHM5S revision 2  
Status: proposal — three single uncontrolled runs, no shared seed, no benchmark

## Observed staging pattern (sampled frames only)

```
Phase 1 (~0–8 s, ~5 samples): architectural wide — rose window, 1–2 figures
Phase 2 (~8–12 s):            face or pale neck in ambient light
Phase 3 (~12–17 s):           close detail (hands, fabric, silhouette)
Phase 4 (≥17 s, 2 of 3 runs): terminal silhouette — spiky figure over pale-haired figure
```

This describes three runs. It is not a rule or reliable prompt compliance claim.

## Interface fields (per run)

| Field              | Type      | Source            | Status       |
|--------------------|-----------|-------------------|--------------|
| opening_figure     | enum      | frame sample      | observed     |
|                    | tiny / standing_pair / two_silhouettes |   |              |
| linked_image       | bool      | prompt metadata   | observed     |
| linked_video       | bool      | prompt metadata   | observed     |
| likeness_hold      | bool      | prompt text       | observed (2 of 3) |
| medium_only        | bool      | prompt text       | observed (1 of 3) |
| terminal_phase     | enum      | frame sample      | observed (2 of 3) |
|                    | silhouette_bend / absent |          |              |
| audio_reviewed     | bool      | —                 | false (all 3) |
| seed               | int/null  | run metadata      | null (all 3) |
| provenance_image   | confirmed/unconfirmed | rights basis | unconfirmed |
| provenance_video   | confirmed/unconfirmed | rights basis | unconfirmed |

## Explicit assumptions requiring a counterexample test

1. Phase timing is inferred from ~1.7 s frame spacing; actual cut points are unknown.
2. opening_figure difference (tiny vs. pair) may be driven by linked_image or by seed variance — indistinguishable here.
3. terminal_phase presence correlates with linked_video=true in this corpus (2/2 runs); causation is not established.
4. medium_only vs. likeness_hold is a prompt-level distinction; whether the model honours it is unverified.

## Gap checklist (for the research queue)

- [ ] Confirm provenance and license of linked image and video (rights basis unconfirmed)
- [ ] Run with explicit seed to separate seed variance from linked-asset effect
- [ ] Review audio for all three runs (not yet done)
- [ ] Read actual experiment records (candidate IDs in article, not yet resolved)
- [ ] Test opening_figure variance: does re-run with same prompt + same image reproduce tiny vs. pair?