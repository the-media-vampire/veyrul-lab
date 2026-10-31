# Integration contract: Alexandria Upspring → hook-analysis workflow

## Source
art_01M68F97NN9PTR3SSHK6MZ12QX revision 1 (documentary only; no live call made).

## Workflow being connected
**Alexandria ads/search** (upstream) → **hook-extraction / campaign-brief workflow** (downstream).

## Interface
| Layer | Detail |
|---|---|
| Entry point | `SearchRequest(q, limit, vertical, category, advertiser)` |
| Output unit | `HookPage` carrying a list of `AdRow` + `Provenance` block |
| Cost signal | `cost_gate(budget_usd, pages)` must pass before each call |
| Provenance | Every `AdRow` carries `schedule=J-1.0.0`, `veyrul_record` ref |

## License assumptions (Schedule J-1.0.0)
- Retain and use for any lawful purpose, including AI training.
- No standalone resale of Upspring data.
- Ad copyright in creatives is **not addressed** by Schedule J; treat as unknown.

## Key assumptions that must be tested
1. Alexandria credits == Firecrawl plan credits (arithmetic only; pages do not state it).
2. Free tier can reach Upspring endpoint (not stated).
3. `strength` field is a useful signal (field quality untested).
4. No additional provider acceptance step beyond Firecrawl account sign-up.

## Open research questions (queued)
- Do Alexandria credits draw from the same pool as plan credits?
- Is there a separate acceptance step for Schedule J?
- What is the actual distribution of `strength` values in real responses?