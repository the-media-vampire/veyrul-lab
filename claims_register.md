# Claims Register — art_01M6S6H21MK5NVE4FB3NJ4YFCM r1

Source: art_01M6S6H21MK5NVE4FB3NJ4YFCM revision 1  
Forge artifact: ff8620e2 (commit 746619ae) — covers per_arm and verdict branches  
This artifact: covers read() interval formula (Claim C)

---

## Claim A — per_arm formula produces 3,213 for the worked example
**Stated inputs:** baseline=0.08, lift=0.02, alpha=0.05, power=0.8  
**Stated output:** 3,213 per arm  
**Status:** Covered by Forge harness ff8620e2 (unexecuted proposal)  
**What would disprove it:** Running test_harness.py and seeing a different ceiling value.

---

## Claim B — four verdict branches are mutually exclusive and exhaustive
**Stated logic:** low>0 → B beat A; high<0 → A beat B; both within ±lift → tie; else → inconclusive  
**Status:** Covered by Forge harness ff8620e2 (unexecuted proposal)  
**What would disprove it:** A (low, high) pair that matches two branches or none. The boundary case low==0 or high==0 is unspecified in the article and not tested in ff8620e2.

---

## Claim C — worked-example actual result is inconclusive, interval −0.22 to +2.24
**Stated inputs:** A: 311/3890, B: 360/3996, alpha=0.05  
**Stated output:** interval −0.22 to +2.24 percentage points  
**Status:** NOT covered by Forge harness. Covered by interval_probe.py (this artifact, unexecuted)  
**What would disprove it:** interval_probe.py printing values that differ from −0.22/+2.24 outside rounding tolerance.

---

## Claim D — stopping-rule enforcement (looks != 1 triggers exit 3)
**Stated logic:** `if type(r.get("looks")) is not int or r["looks"] != 1: sys.exit(3)`  
**Status:** NOT covered by either artifact. Requires file I/O and full compare.py on disk.  
**What would disprove it:** Passing looks=2 and observing the script proceeding to a READING line.

---

## Boundary gap (open)
The article does not specify behaviour when low==0 exactly (B beat A branch fires, but diff==0 is impossible with integer counts unless both rates are equal — this is very low probability but not impossible if n and conversions are chosen adversarially). Not a blocker; noted for completeness.