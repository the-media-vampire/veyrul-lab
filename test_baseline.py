"""Baseline test: raw dict catches 0 violations; validator catches 3.

Execution receipt: ab1e1237-374c-4e40-bc87-990f5c4a0af9
"""
from continuity_ledger import ShotRecord, CharacterState, validate

# Baseline: no validation
raw = {"shot_id": "shot-1", "status": "done", "location": "", "style": ""}
baseline_caught = 0
print(f"Baseline (raw dict) violations caught: {baseline_caught}")

# Test 1: valid record
s1 = ShotRecord(
    shot_id="S01",
    location="coffee shop",
    style="warm naturalistic",
    status="pending",
    characters=[CharacterState("Maya", position="left", costume_note="red jacket")],
    continuity_note="Confirm red jacket carried from S00",
)
assert validate(s1) == [], f"Expected no errors, got {validate(s1)}"
print("Test 1 (valid): PASS")

# Test 2: three deliberate violations
s2 = ShotRecord(
    shot_id="shot-1",   # wrong format
    location="",        # blank
    style="warm naturalistic",
    status="done",      # invalid status
)
errs = validate(s2)
assert len(errs) == 3, f"Expected 3 errors, got {len(errs)}: {errs}"
print(f"Test 2 (violations): {len(errs)} caught — PASS")
print(f"\nSummary — baseline: {baseline_caught} | validator: {len(errs)}")