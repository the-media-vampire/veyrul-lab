# Open questions requiring evidence before integrating

1. **Plot agent output format** — does the paper's appendix confirm that
   PLOT entries name scenes with tension levels? If PLOT is unstructured
   prose, the dialogue_spec_agent cannot reliably flag crisis moments.
   (Research queued in prior session: rqr_01M6H6CR5GQ15B0F7EFRH1CE3S —
   status not checked in this session.)

2. **Writing agent prompt templates** — the paper mentions Appendix prompt
   templates but they were not read (art_01M6H154J7KBB907MQWZ73VV2F r2).
   If a writing agent has a fixed input schema, DIALOGUE_SPEC must conform
   to it or be injected in the system prompt, not the scratchpad.

3. **Empirical coverage of Dowst's properties** — the Tell me a story
   dataset evaluation (human pairwise on plot, creativity, development,
   language use) does not isolate dialogue quality. A sub-evaluation on
   dialogue naturalness and distribution would be needed to test whether
   the adapter changes output measurably.

4. **License chain** — Dowst (pre-1928, public domain via Gutenberg) is
   freely reusable. Agents' Room paper is CC BY 4.0 (arXiv 2410.02603).
   This adapter is MIT. No conflict identified, but redistribution of the
   adapter should attribute both upstream sources.