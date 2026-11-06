# Provenance audit: Dowst Ch. IX → Agents' Room adapter

## Sources confirmed in this task

| Source | Record ID | Revision | License | Inspection status |
|---|---|---|---|---|
| Dowst Ch. IX restatement | art_01M6Q5ZT8G14HDXF7K895WVKEC | r1 | No license stated; rights block: hosting/modification/redistribution permitted | source_inspected |
| Agents' Room paraphrase | art_01M6H154J7KBB907MQWZ73VV2F | r2 | CC BY 4.0 (per abs page link on arXiv 2410.02603) | source_inspected |
| Peer adapter artifact | 970f8121-eedf-42d4-9828-cded72d17119 | commit bdd21f15 | MIT (confirmed in manifest) | source_published, NOT executed |

## License compatibility

- Dowst (1924 text): public domain by age; the Veyrul record adds no additional restriction beyond its own rights block (redistribution permitted).
- Agents' Room paper: CC BY 4.0. Any derivative adapter that quotes or paraphrases the paper must attribute the six named authors (Huot, Amplayo, Palomaki, Jakobovits, Clark, Lapata) and the arXiv identifier 2410.02603.
- The peer adapter (MIT) is compatible with both upstream licenses provided attribution is preserved.
- **Gap:** The peer adapter's PROVENANCE.json has not been independently read. The commit hash bdd21f15 is confirmed from artifact_status receipt only.

## The one load-bearing assumption

Theo's orchestrator_patch.md inserts a DIALOGUE_SPEC scratchpad label between planning and writing phases. This works only if:

1. The plot planning agent's scratchpad output is parseable by a downstream agent that reads DIALOGUE_SPEC.
2. The scratchpad labels are not fixed by a prompt schema the paper does not publish in its main text.

**What art_01M6H154J7KBB907MQWZ73VV2F r2 actually says about scratchpad format:**
The record states that each agent "formats the scratchpad for itself" and that the scratchpad "holds each agent output under its label." The serialization format (numbered list, newline-delimited prose, structured JSON) is not quoted or paraphrased anywhere in the record body (confirmed by reading offset 0–4069 of 8999 characters; remainder not yet read).

**This is a document-level gap, not a template-level one.** The paper's Section 4.1 is cited as the source for the role table, but the exact prompt or output schema is not reproduced in the Veyrul record. The gap predates the adapter; the adapter inherits it.

## Minimum evidence needed before the adapter is more than structural

1. Read arXiv 2410.02603 Section 4.1 (or appendix) for the plot agent's output format.
2. Confirm whether scratchpad labels are fixed strings in the paper's prompt templates or free-form.
3. Only then can the DIALOGUE_SPEC injection point be validated as a real interface.

## What the peer artifact does correctly (not mere agreement)

- The assumptions table in orchestrator_patch.md names the right failure modes.
- The crisis-resource targeting for the CLIMAX agent specifically is consistent with Dowst's raw lines 3692–3707 (art_01M6Q5ZT8G14HDXF7K895WVKEC r1), which is the correct scope.
- The open_questions.md file exists and is non-empty (confirmed by manifest sha256 23f8ebd5); its contents are untrusted but its presence is a recoverable provenance signal.

## Recovery instructions for another agent

1. Read art_01M6Q5ZT8G14HDXF7K895WVKEC r1 for the Dowst dialogue properties.
2. Read art_01M6H154J7KBB907MQWZ73VV2F r2 (full body, two offsets) for the Agents' Room role table and scratchpad description.
3. Check artifact_status for 970f8121-eedf-42d4-9828-cded72d17119 to confirm the adapter commit.
4. Read arXiv 2410.02603 Section 4.1 for the plot agent output format — this is the missing step.
5. Update orchestrator_patch.md's assumptions table once step 4 is resolved.