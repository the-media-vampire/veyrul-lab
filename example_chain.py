"""example_chain.py — usage example, not executed.

Scenario: three-step pipeline
  1. Gemini API (unpaid) generates a caption from a reference image.
  2. Local Qwen-Image-Edit-2511 (Apache-2.0) edits the image.
  3. Gemini API (paid) refines the result.

Expected aggregate: publish_blocked=True (commercial-use gap from steps 1 and 3);
first_blocking_step='caption_gen' (earliest block).
Step 2 does not itself block commercial use (Apache-2.0 clear).
"""

from provenance_chain import ProvenanceChain, PipelineStep, Tier, OwnershipGap

chain = ProvenanceChain()

chain.add_step(PipelineStep(
    step_id="caption_gen",
    model_or_service="gemini-2.0-flash",
    tier=Tier.UNPAID,
    ownership_gap=OwnershipGap.NO_CLAIM_NO_GRANT,
    commercial_intended=True,
    source_record_id="art_01M6668GYBV9RJW3PX59D4KBBR r1",
))

chain.add_step(PipelineStep(
    step_id="image_edit",
    model_or_service="Qwen-Image-Edit-2511",
    tier=None,  # local, no hosted tier
    ownership_gap=OwnershipGap.APACHE_2_CLEAR,
    commercial_intended=True,
    source_record_id="art_01M5Z9WPX7FY4WPTTW9T1VXS34",
))

chain.add_step(PipelineStep(
    step_id="paid_refine",
    model_or_service="gemini-2.0-pro",
    tier=Tier.PAID,
    ownership_gap=OwnershipGap.NO_CLAIM_NO_GRANT,
    commercial_intended=True,
    source_record_id="art_01M6668GYBV9RJW3PX59D4KBBR r1",
))

if __name__ == "__main__":
    import json
    print("--- Per-step audit ---")
    print(json.dumps(chain.audit_report(), indent=2))
    print("\n--- Aggregate posture ---")
    print(json.dumps(chain.aggregate_posture(), indent=2))