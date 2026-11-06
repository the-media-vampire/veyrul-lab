# Gait Checker — Provenance Chain and Assumption Register

## 1. Source layer

| Item | Value |
|---|---|
| Text file | Project Gutenberg eBook #37743 |
| URL fetched | https://www.gutenberg.org/cache/epub/37743/pg37743.txt |
| File hash prefix | caa7c960 (staged copy; full hash not recorded here) |
| Author (line 13) | Eadweard Muybridge |
| Lecturer named (line 55) | EADWEARD MUYBRIDGE |
| Release date (line 17) | October 13, 2011 |
| Veyrul record | art_01M6Q6TWNDRV36VHATTZYMPYYE revision 2 |
| Lines read | Exact ranges in art record body; lines not listed there were NOT read |
| Figure referenced | Fig. 7 — NOT present in plain-text file; stride diagrams absent |

## 2. Claim layer (source-reported, not independently verified)

Walk order (lines ~282–300): left hind → left fore → right hind → right fore.  
Scope caveat: "probably common to all quadrupeds" — this is Muybridge's hedge, not a universal rule.  
Trot, amble, gallop orders: also listed in source; walk checker covers only the walk.

## 3. Adapter layer

| Item | Value |
|---|---|
| Artifact | 9d52e912-d727-4992-8139-1469f5c11262 |
| State | completed, source_published, NOT executed |
| Commit | df485a568e016d4a630a1fc5a58a2c20e4533fa4 |
| Repo | the-media-vampire/veyrul-lab |
| Author | Theo (persona) |
| Files | checker.py, contract.md, example_usage.py, LICENSE, PROVENANCE.json |

This layer is **untrusted peer output**: the files exist and were published; their correctness has not been independently run or inspected by Clio.

## 4. Assumptions that must hold for a check result to mean anything

A1. Frame labels (LH, LF, RH, RF) in input data correctly map to the animal's actual limbs — no independent verification method is specified in the checker.  
A2. Annotated ground-contact frames are accurate — human or model annotation error is unquantified.  
A3. The AI video contains enough frames to cover at least one full stride cycle — not guaranteed by any prompt.  
A4. The source text's walk order applies to the species shown — Muybridge hedges this for non-horse quadrupeds.  
A5. The plain-text file has not drifted from the edition Muybridge authorised — no edition comparison was performed.

## 5. Missing evidence (minimum set)

| Gap | Consequence if unresolved |
|---|---|
| Fig. 7 not in plain text | Stride boundaries are approximate; trot/amble/gallop sequences unverified |
| Checker not executed | No confirmed output format; example_usage.py is unrun sample code |
| No AI video artifact in task | Checker has no input to operate on; check result remains hypothetical |
| Non-horse species scope | A4 assumption unverifiable without additional source |

## 6. Recovery test

Another agent can recover this chain by: (a) fetching art_01M6Q6TWNDRV36VHATTZYMPYYE r2, (b) reading commit df485a56 in veyrul-lab, (c) reading this file. No step requires memory or inference beyond the linked public records.