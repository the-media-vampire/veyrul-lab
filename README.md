# Story Bible Carry-Over

Operationalises the per-scene carry-over table from **Make-A-Story**
(Rahman, Lee, Ren, Tulyakov, Mahajan, Sigal — arXiv 2211.13319v3, CC0 1.0),
summarised in Veyrul record `art_01M6HGFBNCDERMNM02HZPN7SYE` rev 1.

Story-LDM keeps character/setting consistency via visual memory.
This tool puts the same decisions in a story bible any artist can read and edit.

| Field | Paper cue |
|---|---|
| `carried_characters` | Recurring characters, weighted by sentence similarity |
| `new_characters` | No separate paper rule; bible fills the gap |
| `setting` | Background kept or changed to match text |
| `reference_map` | Co-references resolved by memory; here resolved by the artist |

**Limits:** no diffusion model runs; prompt injection reduces but does not
eliminate drift; reference resolution is exact-string; a human must check
each frame. Dataset/model/code licence from the paper was not read (see source record).

```
python example_usage.py
```