# Scoring Rubric — Cup-ring experiment

## Stage 1: Consistency check (run before any editing decision)

Fill in one row per generated frame pair. If any FAIL row appears, stop — record as INCONSISTENT and do not proceed to Stage 2.

| Check | Frame A value | Frame B value | Delta | Pass threshold | Result |
|---|---|---|---|---|---|
| Table surface mean RGB (sample a 20×20 px patch, same position both frames) | | | ΔRGB | ≤ 10 | PASS / FAIL |
| Table brightness (L* in Lab, same patch) | | | ΔL* | ≤ 5 | PASS / FAIL |
| Ring centre X (px from left edge) | n/a | | — | ≤ 5 px from brief spec | PASS / FAIL |
| Ring centre Y (px from top edge) | n/a | | — | ≤ 5 px from brief spec | PASS / FAIL |
| Cup visible in Frame B? | — | — | — | Must be NO | PASS / FAIL |
| Ring visible in Frame A? | — | — | — | Must be NO | PASS / FAIL |

**Overall consistency:** CONSISTENT / INCONSISTENT

If INCONSISTENT, record which checks failed and stop. This result is itself the finding.

---

## Stage 2: Transition comparison (run only if Stage 1 = CONSISTENT)

### Technical observations — fill per variant, frame-by-frame at transition

| Observation | Crossfade variant | Hard-cut variant |
|---|---|---|
| Background displacement visible? (Y/N) | | |
| Brightness discontinuity at cut/blend? (Y/N) | | |
| Cup and ring simultaneously visible? (Y/N; crossfade only) | | |
| Generation instability artefacts? (Y/N; describe if Y) | | |
| Transition duration (frames counted) | | |

### Viewer response codes

Present each sequence without explanation. Record response before describing intention. Use these codes:

**Q1 — What changed?**
- `C` = Cup removed / cup is gone
- `R` = Ring appeared / wet ring
- `B` = Both cup and ring noted
- `O` = Other (write in)
- `N` = Nothing noticed

**Q2 — Where did you look next?**
- `S` = Same position (ring location)
- `E` = Elsewhere on table
- `F` = Frame edge / away from table
- `U` = Unsure

**Q3 — Transition felt like?**
- `RMV` = Removed / taken away
- `DSV` = Dissolved / faded
- `NTD` = Noticed but undecided
- `O` = Other (write in)

### Viewer response table

| Viewer ID | Sequence shown first | Q1 | Q2 | Q3 |
|---|---|---|---|---|
| V01 | | | | |
| V02 | | | | |
| V03 | | | | |

Alternate presentation order: even-numbered viewers see hard cut first.

---

## Stage 3: Summary record

| Field | Value |
|---|---|
| Artifact (Scout prompts+sheet) | `2bb3e31d-4098-4e87-8793-932329678ac2` |
| Artifact (this rubric) | `[fill in after publish]` |
| Source article | `art_01M6QDQ1SYGKQ8DRSECJ1VKZC8` revision 1 |
| Stage 1 result | CONSISTENT / INCONSISTENT |
| If inconsistent, failed checks | |
| Favoured variant (technical) | |
| Favoured variant (viewer majority on Q3) | |
| Disagreement between technical and viewer findings? | Y/N |