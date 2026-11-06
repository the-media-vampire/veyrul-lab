# Dialogue-spec scratchpad entry

This block is written by a Dialogue-Spec agent that runs **after** the four
planning agents (conflict, character, setting, plot) and **before** the five
writing agents. It appends one labeled entry to the Agents' Room shared
scratchpad. Each writing agent should be instructed to read it.

Source authority: Dowst, *The Technique of Fiction Writing*, Chapter IX
(Gutenberg 32092, captured 2026-11-05), restated in art_01M6Q5ZT8G14HDXF7K895WVKEC r1.
Agents' Room scratchpad interface: art_01M6H154J7KBB907MQWZ73VV2F r2.

---

## DIALOGUE_SPEC (scratchpad label)

```
DIALOGUE_SPEC:
  distribution:
    rule: Interleave dialogue with narration and description; do not place
          speech in unbroken blocks. Break any long speech with a beat of
          action or description.
    applies_to: all writing agents

  naturalness:
    rule: Speech should sound clipped and fragmentary, not bookish. Gaps
          the reader fills in are acceptable. Stilted dialogue loses the
          reader faster than stilted narration.
    applies_to: all writing agents

  purpose:
    rule: Every exchange must carry a definite payload: information,
          character revelation or plot movement. Transcribing talk for
          supposed wit alone is not sufficient.
    applies_to: all writing agents

  situation_fit:
    rule: The same character speaks differently under different conditions.
          Speech must match both the established character voice and the
          current moment's emotional charge.
    applies_to: all writing agents

  crisis_resources:
    # Only the CLIMAX writing agent is required to apply all three.
    # Rising-action and falling-action agents may apply resource_2.
    resource_1: Narrate the physical effect on the character before giving
                words; step outside dialogue at the peak.
    resource_2: Use broken, exclamatory, clipped speech to signal strain.
    resource_3: Prefer plain, short, emotionally direct word choices in the
                highest-tension lines.
    applies_to: climax (required), rising_action + falling_action (optional)

  verbs_of_utterance:
    rule: Vary dialogue tags across the section; do not repeat the same verb
          on every line.
    applies_to: all writing agents
```