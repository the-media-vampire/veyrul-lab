from cut_map_contract import Beat, CutMapContract, validate

# Test 1: conforming contract
conforming = CutMapContract(
    audio_ref="@Audio 1",
    fence_negatives=["no invented music","no voiceover","no lip-sync"],
    genre="hip-hop", tempo_bpm=98, world_head_count=6,
    clip_duration_s=15.0,
    beats=[
        Beat(0.0,"intro bar","static wide","hard cut",direction="static"),
        Beat(2.0,"kick drop","push in","hard cut",direction="toward"),
        Beat(5.0,"hi-hat roll","orbit","orbit",direction="clockwise"),
        Beat(12.5,"breakdown","dutch slide","dutch slide",direction="low"),
        Beat(13.5,"final bar","static wide","hard cut",direction="static"),
    ],
    final_pose_described=True, loopable_end=True,
)
assert validate(conforming) == [], f"Expected valid: {validate(conforming)}"

# Test 2: missing camera direction + no final pose
missing_fields = CutMapContract(
    audio_ref="@Audio 1",
    fence_negatives=["no invented music","no voiceover","no lip-sync"],
    genre="hip-hop", tempo_bpm=98, world_head_count=6,
    clip_duration_s=15.0,
    beats=[
        Beat(0.0,"intro","static wide","hard cut"),   # direction=None
        Beat(2.0,"kick","push in","hard cut"),         # direction=None
    ],
    final_pose_described=False, loopable_end=True,
)
errs = validate(missing_fields)
assert any("mismatch-3" in e for e in errs)
assert any("mismatch-6" in e for e in errs)

# Test 3: out-of-order beats + too few fence negatives
bad_order = CutMapContract(
    audio_ref="@Audio 1",
    fence_negatives=["no invented music"],  # only 1
    genre=None, tempo_bpm=None, world_head_count=None,
    clip_duration_s=15.0,
    beats=[
        Beat(5.0,"snare","orbit","orbit",direction="cw"),
        Beat(2.0,"kick","push in","hard cut",direction="toward"),  # wrong order
    ],
    final_pose_described=True, loopable_end=False,
)
errs = validate(bad_order)
assert any("fence negatives" in e for e in errs)
assert any("not after" in e for e in errs)
assert any("world_head_count" in e for e in errs)

print("All assertions passed.")