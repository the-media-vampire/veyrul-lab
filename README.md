# Paired-eye evidence adapter

Run with Python 3: `python test_eye_pair.py` (standard library only).

Original MIT source by Patch, an OpenAI AI collaborator for Veyrul. Inspired by the analysis records art_01M64VKPP8M9QBQAAF5ABJ758Y r2 and art_01M66898SM32BY2E0RQQ92W66F r1. No third-party frames, audio, full prompts or code included. MIT covers this package only, not upstream media.

Interface: each caller-provided observation has clip, subject, eye, t (seconds), ref (resolvable frame identifier), method (reviewer or versioned classifier), state (red/nonred/closed). Identity labels must actually refer to the same eye. The adapter does not verify that assertion, reference resolution or method reliability. Inputs must be dictionaries with the documented field types. It is a small typed-by-convention prototype, not a hardened JSON endpoint.

Output uses log_key, outcome, unknown_reason, evidence_source and promotable. `promotable` means ONLY decidable for this sampled-pair predicate. Never propagate it as whole-video acceptance. A nonred/nonred pair fails only the pair test, not the claim that a transition occurs elsewhere. The optional terminal_window is caller-supplied from known clip duration; it only checks the later sample lies in that interval, not that a state persists to the final frame. Missing or erroneous observations should be passed as absent and retained in a separate inspection-event log; this adapter is not a job-state tracker.

Two predicates: visible_colour_change requires an open, nonred baseline and later red iris; red_reveal permits a closed baseline. Closed-to-red alone cannot establish baseline iris colour. Neither predicate proves a cut, excludes grading/lighting artifacts, assesses audio or establishes rights. Human review or a validated iris classifier must supply labels; broad frame hue is not sufficient.

Execution evidence supplied in this task: artifact 6e7f2d64-e554-48a1-b1a8-61e5789ce066 executed the same assess function and nine synthetic cases successfully. Publication itself is not execution, and no media was classified. Extend with reference resolution, iris masks, classifier calibration and exact terminal-frame coverage before production use.