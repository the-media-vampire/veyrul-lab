from story_bible import StoryBible, SceneEntry

bible = StoryBible(title="Demo: forest adventure")
bible.add_scene(SceneEntry(
    scene_id=1,
    story_text="Mara and Leon set off through the forest at dawn.",
    carried_characters=[], new_characters=[
        "Mara: young woman, red cloak, brown satchel",
        "Leon: tall man, grey coat, lantern"],
    setting="changed: dense forest trail, dawn light", reference_map={}))
bible.add_scene(SceneEntry(
    scene_id=2,
    story_text="She found a glowing stone. He called out to her.",
    carried_characters=["Mara: red cloak, brown satchel","Leon: grey coat, lantern"],
    new_characters=[], setting="same",
    reference_map={"She":"Mara","He":"Leon","her":"Mara"}))
bible.add_scene(SceneEntry(
    scene_id=3,
    story_text="They crossed the bridge to the market.",
    carried_characters=["Mara: red cloak, brown satchel","Leon: grey coat, lantern"],
    new_characters=[], setting="changed: stone bridge, sunlit village market",
    reference_map={"They":"Mara and Leon"}))

print("VALIDATION:", bible.validate() or "none")
for s in bible.scenes:
    b = bible.baseline_prompt(s.scene_id)
    c = bible.carry_over_prompt(s.scene_id)
    print(f"\nScene {s.scene_id} baseline ({len(b)}c): {b}")
    print(f"Scene {s.scene_id} carry-over ({len(c)}c): {c}")