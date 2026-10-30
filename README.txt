Nothing arrives — single-endpoint fidelity review card
=======================================================

Source: art_01M67BHF7NH8G09AV1W8NEGWSB revision 2
Source image artifact: 7689067d-2edd-405d-8883-79173e7e0a36
Image SHA-256: f07df0e95b2adb04c68faca9e34e20f11a2e0d6489dcbfa17c3cea0af6bda8ae

Test type: single-endpoint image-to-video (harder probe)
Rationale: No endpoint anchor. Maximum model freedom to invent.
           A failure here is more informative than a first/last-frame pass.
           A pass here is more reassuring than a constrained-endpoint pass.

Usage
-----
1. Run your i2v tool with source image artifact 7689067d and the brief in REVIEW_CARD.json.
2. Extract frames: python3 collect_frames.py --video clip.mp4 --brief CASE.json --output review-001
3. Inspect all frames against the four falsification criteria in REVIEW_CARD.json.
4. Record every triggered criterion with frame index, time span and uncertainty.
5. Label the result single_endpoint_i2v, not first_last_frame.

Control
-------
Treatment A is a static 5-second hold of the source image. No criteria can trigger.
Compare both if B renders: does any motion strengthen waiting, or merely advertise generation?

Execution status at time of publication
---------------------------------------
- Source image: generated and inspected (artifact 7689067d).
- Inspection: empty platform, edge visible, no arrivals, dusk lighting confirmed.
- Video render: not submitted (serial_busy).
- No motion fidelity claim is made.