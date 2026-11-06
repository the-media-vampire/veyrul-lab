# TimelineJS unique_id stability and repeat-per-strand experiment brief

Source: art_01M6K4N37MCKDM0TZB5V9ZGS30 revision 3  
Status: **not run** — this is a proposed experiment, not a report of results.

## Two untested inferences this brief targets

From the source record (inference section, our words):

1. **unique_id stability**: "a regenerated file keeps links stable only if ids come from the canon" — the page documents the field and says ids drive goToId() and hash_bookmark, but we have not observed what actually happens when unique_id is absent vs. present across two JSON regenerations.

2. **repeat-per-strand**: "an event shared by two strands needs one slide per strand, each with its own unique_id; that repeat-per-strand rule is our convention, not something the page defines" — the page says group is one value per slide; it says nothing about duplicate events.

## Experiment A — unique_id stability

### Intention
Test whether TimelineJS hash-bookmark URLs survive a JSON regeneration when unique_id is set from a stable canon key vs. derived from the headline.

### Contrasting alternatives
| Condition | unique_id | Expected behaviour per docs |
|---|---|---|
| Canon-keyed | `"evt-001"` (fixed) | Bookmark URL unchanged after rename |
| Headline-derived | absent | Bookmark URL changes after headline rename |

### Minimal fixture — baseline slide (see `timeline_A1_canon_key.json`)
Edit the headline in both files, reload, check whether the hash in the URL bar changes. That is the discriminating observation.

### What would change our mind
- If the headline-derived id stays stable despite what the docs say: TimelineJS may normalise ids in a way the page source doesn't document.
- If the canon-keyed id still breaks: either the field is not read, or another mechanism overrides it.

---

## Experiment B — repeat-per-strand

### Intention
Test whether placing the same narrative event on two group rows (via two slides with matching headline but different group and unique_id) renders both entries cleanly in the navigation, without collision or missing entries.

### Contrasting alternatives
| Condition | Slides | Expected |
|---|---|---|
| Repeat-per-strand | Two slides, same start_date, different group and unique_id | Both appear, in respective group rows |
| Single shared slide | One slide, one group | Only one group row gets the event |

### Minimal fixture — see `timeline_B_strands.json`
Load in a local TimelineJS instance. Inspect the navigation bar: are both group labels visible? Does the event appear once per group row or only once total?

### What would change our mind
- If two slides with the same start_date but different groups both render: our convention is correct.
- If only the first slide renders: the viewer deduplicates by date, and the repeat-per-strand convention fails silently.
- If the navigation shows one entry straddling both groups: group is a layout hint, not a filter.

---

## Observation sheet (fill in after running)

```
Experiment A
  Condition 1 (canon-keyed):  URL after headline rename = ____________
  Condition 2 (headline-derived): URL after headline rename = ____________
  Stable? [ ] Yes  [ ] No  [ ] Unclear
  Unexpected behaviour: ____________

Experiment B
  Both group rows visible in nav? [ ] Yes  [ ] No
  Event count in nav: ____________ (expected 2)
  Rendering anomalies: ____________
```

## What is NOT tested here
- The media type page (not staged in source record)
- The spreadsheet route
- Cosmological scale
- BCE years
- display_date override fidelity