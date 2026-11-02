"""Shot-design parameter validator (no network, no model).
Mechanics are inference per source records; no result is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

WIDE_MAX_MM = 35   # art_01M5NP7E r1 rule-of-thumb
TELE_MIN_MM = 70
VALID_MOVES = {
    "static","pan","tilt","dolly in","dolly out",
    "truck left","truck right","pedestal up","pedestal down",
    "zoom","crane","handheld","whip pan","arc shot",
}  # art_01M5NNTZ r1

@dataclass
class ShotParams:
    focal_length_mm: Optional[float] = None
    lens_word: Optional[str] = None
    dof_intent: Optional[str] = None  # "shallow"|"deep"
    fstop: Optional[float] = None
    move: Optional[str] = None
    usd_focal_length: Optional[float] = None
    usd_h_aperture: Optional[float] = None
    usd_v_aperture: Optional[float] = None
    usd_has_distortion: bool = False
    estimate_tags: list[str] = field(default_factory=list)

def validate(p: ShotParams) -> list[str]:
    v: list[str] = []
    if p.focal_length_mm and p.lens_word:
        fl, w = p.focal_length_mm, p.lens_word.lower()
        if "telephoto" in w and fl < TELE_MIN_MM:
            v.append(f"Contradiction: telephoto word but {fl}mm < {TELE_MIN_MM}mm threshold.")
        if "wide" in w and fl > WIDE_MAX_MM:
            v.append(f"Contradiction: wide-angle word but {fl}mm > {WIDE_MAX_MM}mm threshold.")
    wide = ((p.focal_length_mm or 999) <= WIDE_MAX_MM or
            "wide" in (p.lens_word or "").lower())
    if wide and p.dof_intent=="shallow" and p.fstop and p.fstop < 2.0:
        v.append(f"Flagged blend: wide-angle+shallow DOF+f/{p.fstop} (art_01M5NHNG r1).")
    if p.move and p.move.lower() not in VALID_MOVES:
        v.append(f"Move '{p.move}' not in Veo vocabulary (art_01M5NNTZ r1).")
    if p.usd_focal_length is None:
        v.append("USD: focalLength missing (art_01M5NPJC r1).")
    if None in (p.usd_h_aperture, p.usd_v_aperture):
        v.append("USD: aperture(s) missing (art_01M5NPJC r1).")
    if p.usd_has_distortion:
        v.append("USD: distortion absent from base UsdGeomCamera schema (art_01M5NPJC r1).")
    return v

if __name__=="__main__":
    good=ShotParams(focal_length_mm=35,lens_word="wide-angle",dof_intent="deep",
        move="dolly in",usd_focal_length=35.0,usd_h_aperture=23.8,usd_v_aperture=13.4)
    bad=ShotParams(focal_length_mm=24,lens_word="telephoto",dof_intent="shallow",
        fstop=1.2,move="spin",usd_has_distortion=True)
    print("Clean:",validate(good))
    print("Flagged:",[*validate(bad)])