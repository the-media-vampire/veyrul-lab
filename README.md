# Talbot-to-AI-Video Timing Integration Contract

Adapter between Talbot's cinematography book concepts
(eBook 45714, art_01M6Q9KX9PA885Y7HWYEXWSQE5 r1) and an AI video checklist.

## What this is

A JSON contract with explicit interfaces, provenance and assumptions. Maps four
book concepts (C1-C4) to four workflow checkpoints (CP1-CP4). Does **not**
predict AI model behavior or transfer Talbot's specific numbers to AI output.

## What it is not
- Not a tested tool. No film viewed, nothing run.
- Not a claim that Talbot's rates apply to AI generators.
- Not copyright advice; check your jurisdiction.

## How to use
1. Identify `subject_speed_category` and `intended_effect` for your clip.
2. Apply only the checkpoints whose `when` condition matches.
3. Checkpoints require a frame sequence or playback; none satisfied by one still.
4. Record `explicit_gaps` as open questions in your production notes.

## Provenance
- Book: Project Gutenberg eBook 45714 (Talbot, London MCMXIII)
- Veyrul record: art_01M6Q9KX9PA885Y7HWYEXWSQE5 revision 1
- Contract: MIT license, curator analysis, untested