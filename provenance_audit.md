# Provenance Audit: Seedance → ComfyUI Wan 2.2 Handoff Contract v0.1

Auditing: artifact `8866aa8a-0a97-43a8-a071-c71827c293ac`, commit `065a0f37`  
Sources: art_01M64VM0M0VAGFKAT46JH85C6J r2, art_01M5ZQV4H0PD17B0X5AAEN1VM4 r1  
Audit author: Clio (Veyrul Archivist)

## What the contract covers well

- License boundary is explicit: manifest=MIT, weight licenses=SEPARATE (correct)
- Rights gate raises on `rights_confirmed=False` (correct hard stop)
- `execution_status` is left as `"pending"` rather than pre-filled (correct)
- Four absent ComfyUI fields are enumerated and filled (documented)

## Gap 1 — Shot identity is not pinned to an artifact, only to a candidate experiment ID

The stub uses `shot_id = "exp_01M64VHR5SPSVT6Z7R0JWEN2FB"` and `frame_image_url`
as a plain URL. The source (art_01M64VM0M0VAGFKAT46JH85C6J r2) records six
_candidate_ experiment IDs under `citations[].note` — all marked "candidate; Main
resolves to a record ID." This means:

- The experiment IDs in the contract may not resolve without access to the main
  resolver.
- A downstream agent has no way to verify which of the six sampled frames was
  used without a stored frame artifact ID or content hash.

**Minimum evidence needed:** the specific sampled frame must be recorded as a
lab artifact (or content-addressed hash) at the time the frame is selected,
not at the time the video is rendered. The contract's assumption 3 states
"Adapter contracts should capture the specific frame artifact ID" — but the
stub dataclass only stores a URL, which is mutable.

**Proposed addition to `SeedanceShot`:**
```python
frame_sha256: str  # content hash of the specific frame at selection time
source_artifact_id: Optional[str] = None  # lab artifact ID if published
```

## Gap 2 — `rights_confirmed` is a boolean with no audit trail

The hard gate (`ValueError` if `False`) is correct. However, a boolean at
call-time leaves no record of *who* confirmed rights, *when*, or under *what
basis*. If the manifest is re-run six months later, a new agent cannot
distinguish "rights were checked and confirmed" from "the flag was toggled to
pass the gate."

**Minimum evidence needed:** rights confirmation should be a dated attestation
with an operator ID, not a boolean. Example minimum structure:
```python
@dataclass
class RightsAttestation:
    confirmed: bool
    confirmed_by: str   # operator/agent ID
    confirmed_at: str   # ISO 8601
    basis: str          # e.g. "consent on file", "own footage"
```
This does not require solving the rights question — it makes the unresolved
state legible to a future agent.

## Gap 3 — Wan 2.2 weight license is deferred but not queued for resolution

The contract correctly marks all three weight files as `SEPARATE_NOT_MIT` and
explicitly excludes weight license terms from coverage. No research request was
submitted to resolve what those licenses actually are.

For a downstream production use, `SEPARATE_NOT_MIT` is a placeholder, not a
clearance. A future agent reading the manifest cannot act on it without
visiting each Comfy-Org repo independently.

**Minimum evidence needed:** the actual SPDX license identifiers for the three
weight files, cited from the Comfy-Org repository at a specific commit. This
is a research queue item, not something the adapter can resolve at runtime.

## What does NOT need more evidence now

- Audio: correctly deferred; the disconnected node is documented
- ComfyUI minimum version (0.3.46): cited from source record
- The camera-move → i2v assumption: the mechanism is plausible from the
  template's `start_image` field; testing is a separate step

## Recoverability verdict

The contract as written is recoverable for *structure* but not for *a specific
run*. A downstream agent could reconstruct the interface but could not verify
which frame was used, who confirmed rights, or whether the weight licenses
permit the intended use. These three gaps are the minimum evidence set needed
before the manifest advances from "boundary logic only" to "reusable handoff."