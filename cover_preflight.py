"""Cover spread preflight — specs from art_01M6K1452AX5GW86HWQAVGQBNE rev 1.
Not printer advice. Printer pages captured 2026-11-03; may have changed."""
from dataclasses import dataclass
from typing import List, Literal

Printer = Literal["IngramSpark","Lulu","KDP"]
Severity = Literal["PASS","WARN","FAIL"]

@dataclass
class SpreadSpec:
    printer: Printer
    spread_width_px: int
    spread_height_px: int
    ppi: int
    trim_w: float   # single-page trim width, inches
    trim_h: float
    spine_w: float  # from printer calculator — not computed here
    page_count: int
    has_alpha: bool = False
    has_spine_text: bool = False
    has_barcode_zone_clear: bool = True

@dataclass
class Finding:
    printer: Printer
    severity: Severity
    rule: str
    detail: str

_S = {
    "IngramSpark": dict(bleed=0.125,safe=0.25,min_ppi=300,spine_pg=48),
    "Lulu":        dict(bleed=0.125,safe=0.5, min_ppi=300,max_ppi=600),
    "KDP":         dict(bleed=0.125,safe=0.125,min_ppi=300,spine_pg=79),
}

def validate(spec: SpreadSpec) -> List[Finding]:
    out: List[Finding] = []
    s = _S[spec.printer]
    p = spec.printer

    # Resolution
    if spec.ppi < s["min_ppi"]:
        out.append(Finding(p,"FAIL","resolution",f"{spec.ppi}ppi < {s['min_ppi']}"))
    elif spec.printer=="Lulu" and spec.ppi > s["max_ppi"]:
        out.append(Finding(p,"WARN","resolution",f"{spec.ppi}ppi > Lulu max {s['max_ppi']}"))
    else:
        out.append(Finding(p,"PASS","resolution",f"{spec.ppi}ppi ok"))

    # Transparency
    if spec.has_alpha:
        out.append(Finding(p,"FAIL","transparency","Alpha present; flatten before export"))

    # Canvas geometry
    b = s["bleed"]
    exp_w = round((2*b + 2*spec.trim_w + spec.spine_w) * spec.ppi)
    exp_h = round((2*b + spec.trim_h) * spec.ppi)
    tol = 2
    sev_w = "PASS" if abs(spec.spread_width_px-exp_w)<=tol else "FAIL"
    sev_h = "PASS" if abs(spec.spread_height_px-exp_h)<=tol else "FAIL"
    out.append(Finding(p,sev_w,"canvas_width", f"{spec.spread_width_px}px (expect ~{exp_w}px)"))
    out.append(Finding(p,sev_h,"canvas_height",f"{spec.spread_height_px}px (expect ~{exp_h}px)"))

    # Spine-text page threshold
    mn = s.get("spine_pg")
    if spec.has_spine_text and mn and spec.page_count < mn:
        out.append(Finding(p,"FAIL","spine_text",
            f"{p} needs >={mn} pages for spine text; book has {spec.page_count}"))
    if spec.has_spine_text and p=="KDP":
        out.append(Finding(p,"WARN","spine_text",
            "KDP threshold ambiguous in record (79 vs >79); verify on current page"))

    # IngramSpark barcode zone
    if p=="IngramSpark" and not spec.has_barcode_zone_clear:
        out.append(Finding(p,"FAIL","barcode",
            "Keep 1.75x1 inch back-cover area clear for barcode (black on white)"))

    return out