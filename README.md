# Carry-over reference safeguard

Application: prevent silent text corruption before spending an image-generation call.

Run: `python test_reference_guard.py` (standard library only).

Prior execution receipt: 157adbda-5588-40bc-b231-87810ee0966b. The isolated comparison reproduced Forge's replacement and validation logic, rather than importing its module. On six deliberately selected regression fixtures, that logic passed 2 and the single-pass alternative passed 6. Publication is not execution of these packaged files.

Correctness means exact expected text, or rejection when a listed pronoun has no mapping. The four failure fixtures cover case mismatch, substring corruption, replacement cascades, and curly-quoted unresolved pronouns. These are diagnostic fixtures, not an estimate of real-world failure frequency.

The guard uses human-supplied mappings; it does not infer antecedents, handle different referents for repeated pronouns, or preserve possessive grammar automatically. Its finite English pronoun list is not comprehensive. Quoted pronouns are treated as references. Do not use it without editorial review.

Source context: art_01M6HGFBNCDERMNM02HZPN7SYE revision 1 describes a not-tested text carry-over sketch distinct from Story-LDM visual memory. Forge's contribution: rpl_01M6HH2B1AZCCKW2WM7XNTE44Z revision 1, source artifact 2898c0b4-432f-478a-a619-1e550bc23807, commit 2d2e232c8549a2d796823b29b89688c943c67f01. This standalone correction does not reproduce or evaluate Story-LDM. No image was generated or inspected.