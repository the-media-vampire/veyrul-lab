"""Illustrative usage — not executed; demonstrates the interface."""
from checker import check_stride

# A correctly ordered stride
good = {
    "stride_id": "stride_001",
    "contacts": [
        {"frame": 3,  "foot": "LH"},
        {"frame": 7,  "foot": "LF"},
        {"frame": 11, "foot": "RH"},
        {"frame": 15, "foot": "RF"},
    ],
}
print(check_stride(good))
# Expected: match=True, flags=[]

# A misordered stride (common AI video failure: hind/fore swap)
bad = {
    "stride_id": "stride_002",
    "contacts": [
        {"frame": 3,  "foot": "LF"},   # fore before hind — wrong
        {"frame": 7,  "foot": "LH"},
        {"frame": 11, "foot": "RF"},
        {"frame": 15, "foot": "RH"},
    ],
}
print(check_stride(bad))
# Expected: match=False, flags=["wrong_order"]

# Ambiguous frame (reviewer unsure which foot)
ambig = {
    "stride_id": "stride_003",
    "contacts": [
        {"frame": 3,  "foot": "LH"},
        {"frame": 7,  "foot": "?"},
        {"frame": 11, "foot": "RH"},
        {"frame": 15, "foot": "RF"},
    ],
}
print(check_stride(ambig))
# Expected: match=False, flags=["ambiguous_frame", "missing_contact"]