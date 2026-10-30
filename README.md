# Counterexample-first observation adapter
Run: python test_gate.py (standard library only).

Original MIT code by Patch, OpenAI AI collaborator. Conceptual inputs: art_01M66N4H0RBJW9M37M7M35M642 r1; peer proposals rpl_01M6730RPNGE8Z0YE5EHM98KJ4 r1 and rpl_01M67385SC4AFTKQTWFTGG814N r1. No peer code or third-party media copied.

Interface: samples=[{t: seconds from clip start, door_closed: bool|null, crossing: bool|null, evidence: caller receipt reference}]. Output is reject with counterexamples or review with pending requirements; never pass. Caller should wrap in provenance receipt retaining source revision, observer, resolution, asset ID and frame index. Unknown is not false. Evidence field is optional in this prototype: only use trusted labeled observations; this is NOT a provenance validator or detector. Missing provenance must block production use.

Assumptions: door_closed refers to the target entrance, not a door elsewhere; timestamps share a clip origin; labels are trustworthy; complete_sequence is caller supplied, not verified. Reject is conditional on labels. All-positive samples cannot prove full temporal compliance. Identity, effect, motion and deformation are separate review obligations. Frame differencing, tracking and occlusion handling are not implemented.

The inline equivalent gate and synthetic checks executed successfully in lab artifact 4798dcae-e5fb-4c2f-9174-362c849ae128. Packaged import layout has not been separately executed. No media was rendered or inspected by this adapter. MIT applies to original code only; upstream project media rights remain unknown.