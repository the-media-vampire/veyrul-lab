"""Example: THREAD contract and partial render-log from stills.
Observations from art_01M66898SM32BY2E0RQQ92W66F r1 only.
Video playback, audio and full prompt not available.
"""
from prompt_contract import PromptContract, CameraWindow, FailedTakeRule, check_render
import json

contract = PromptContract(
    source_id="art_01M66898SM32BY2E0RQQ92W66F#r1",
    continuation_anchor="exact last frame of source video, no break",
    lens_mm=50,
    dialogue_lock=(3, "three short lines; nothing else spoken"),
    camera_plan=[
        CameraWindow(0,  4,  "orbit right to front; settle left edge", "stands rooted, eyes on bed"),
        CameraWindow(4,  8,  "hold frontal",        "helper enters, takes arms, speaks, turns away"),
        CameraWindow(8,  14, "ease back with steps", "steps back, asks; she half-turns, gone"),
        CameraWindow(14, 22, "retreat step for step; mirror enters right", "walks backward slowly"),
        CameraWindow(22, 30, "medium CU: man left, mirror right", "back to wall; holds"),
    ],
    failed_take_rules=[
        FailedTakeRule("cut_framing",   "framing changed without physical travel",          "no_physical_travel"),
        FailedTakeRule("room_exit",     "door opened or person leaves",                     "door_opened"),
        FailedTakeRule("clean_bundle",  "bundle reads clean; lower half must be soaked",    "bundle_not_soaked"),
        FailedTakeRule("clean_hands",   "hands clean/lightly marked in final frame",        "hands_clean"),
        FailedTakeRule("centred_frame", "centred or symmetrical frame at any moment",       "frame_centred"),
        FailedTakeRule("mirror_absent", "final frame lacks mirror",                         "mirror_absent"),
        FailedTakeRule("grade_clean",   "look cleaner/brighter/sharper than source grade",  "grade_lifted"),
        FailedTakeRule("face_bright",   "face or bed brightly/evenly lit",                  "face_bright"),
    ],
)

# Partial log derived from 8 stills (art_01M66898SM32BY2E0RQQ92W66F r1).
# Keys absent = not verifiable from stills alone.
partial_log = {
    "door_opened":       False,
    "bundle_not_soaked": True,   # stills show white linen + red smears, not soaked
    "hands_clean":       False,  # smeared red at 0:29
    "frame_centred":     True,   # 0:19 near-centre mismatch noted in record
    "mirror_absent":     False,
    "grade_lifted":      False,
}

report = check_render(contract, partial_log)
print(json.dumps(report, indent=2))