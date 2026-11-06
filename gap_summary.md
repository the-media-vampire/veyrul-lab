# Key Gaps vs. Theo's Contract

Theo's contract (978d1200) correctly identifies:
- The bounded/unbounded termination mismatch
- The need for gain budgeting when combining adc.ck and demo3.ck
- The license gap as an open question

This checklist adds:

1. **The commit-pin is not a release tag.** The source record says 'branch head'
   (art r1). If the branch advances, the fetched files may no longer match the
   commit. The integration contract inherits this instability unless the
   specific commit SHA is treated as the canonical reference.

2. **Per-file header check is the actionable license step.** The contract lists
   the license gap but does not specify how to resolve it. Checking bytes 0-200
   of each .ck file at commit 401bbda is the minimum recoverable action.

3. **'not_run' must propagate.** Any downstream artifact that cites adapter_sketch.ck
   must carry the not_run caveat or it misrepresents the evidence state. The
   receipt (executed=false) is the authoritative source for this claim.

4. **CCRMA attribution is inferable but not cited.** A redistribution that omits
   the upstream author would be incomplete even if the license permits it.