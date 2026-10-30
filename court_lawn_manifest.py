"""Instantiated manifest for the three-run court-and-lawn session.

Source: art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2 (Seedance 2.5, 25 Sep 2026 UTC).
Observations from H01 sampled-frame inspection; not independently verified.
"""

from cut_manifest_schema import ClipEntry, CutManifest, SpatialContinuityAssertion

# Three clips as described in art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2.
# Candidate experiment URLs from source citations; not resolved to stable IDs.
clips = [
    ClipEntry(
        clip_id="exp_01M64VHHFXDAZTSDB4C8NWSTJV",
        duration_s=30.0,
        camera_path="Wide lawn → near-lens pass → court fence → hoop → woman running away",
        key_action="Master coverage; woman runs, man hangs from hoop",
        seed_set=False,
        rights_confirmed=False,   # article: 'unconfirmed in disclosure and rights'
        audio_reviewed=False,     # article: 'audio was not listened to'
        holds_likeness=True,      # article: 'hold likeness'
    ),
    ClipEntry(
        clip_id="exp_01M64VH7Z81MJ2V7DD44D0HYWA",
        duration_s=19.0,
        camera_path="Outside fence; static/near-static",
        key_action="Hanging man, leg kick, fall to sitting recovery",
        seed_set=False,
        rights_confirmed=False,
        audio_reviewed=False,
        holds_likeness=True,
    ),
    ClipEntry(
        clip_id="exp_01M64VHDN2EWMQFSGSVWDS6S2X",
        duration_s=15.0,
        camera_path="Single wide view",
        key_action="Man clutches chest, ends lying on grass",
        seed_set=False,
        rights_confirmed=False,
        audio_reviewed=False,
        holds_likeness=True,
    ),
]

manifest = CutManifest(
    session_id="court-lawn-2026-09-25",
    source_article="art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2",
    clips=clips,
    spatial_continuity=SpatialContinuityAssertion(
        basis="Sampled-frame inspection by H01 (12 frames per clip)",
        scope="Court and lawn treated as one continuous place across all three runs",
        generalises=False,   # article: 'describes these three runs, not a rule'
        evidence_record="art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2",
    ),
    assembly_note=(
        "Spatial continuity supports cutting these three clips together. "
        "All three rights and audio gates must clear before distribution. "
        "No seed was set; runs are unrepeatable."
    ),
)

if __name__ == "__main__":
    issues = manifest.validate()
    blocked = manifest.is_assembly_blocked()
    print(f"Assembly blocked: {blocked}")
    print(f"Issues ({len(issues)}):")
    for i in issues:
        print(f"  - {i}")