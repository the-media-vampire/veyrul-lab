# Open questions requiring research

1. **Orchestrator configuration**: Does the Agents' Room implementation expose planning-agent call order as a parameter, or is it fixed in code? The paper (Section 3) says the orchestrator is deterministic but does not describe configuration surface.

2. **Scratchpad schema enforcement**: Do writing-agent prompt templates accept arbitrary scratchpad labels (permissive schema) or only the labels defined in the paper (fixed schema)? This determines whether `PLAUSIBILITY_GATE` can be injected without changing prompt templates.

3. **Evaluation signal for character-first ordering**: The Tell me a story dataset human evaluation (Section 5) uses plot, creativity, development and language-use dimensions. None explicitly measures 'situation emerges from character'. Is there a usable proxy dimension, or would a new evaluation item be needed to test this contract?