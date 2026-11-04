"""6x9 IngramSpark paperback, spine from printer calculator (placeholder 0.45 in)."""
from cover_preflight import SpreadSpec, validate

spec = SpreadSpec(
    printer="IngramSpark",
    trim_w=6.0, trim_h=9.0, spine_w=0.45,
    page_count=200, ppi=300,
    spread_width_px=3810,   # (0.125+6+0.45+6+0.125)*300 = 12.70in
    spread_height_px=2775,  # (0.125+9+0.125)*300 = 9.25in
    has_alpha=False, has_spine_text=True, has_barcode_zone_clear=True,
)
for f in validate(spec):
    print(f"{f.severity:4}  [{f.rule}]  {f.detail}")