# LoRA strength validator
# Source: art_01M66JVTQPRBASJFZ4PK2DM74A r1 (eleven archived model cards)
# Values are author statements; nothing was run or measured.

CARDS = {
    # key: (min, max, base_model, card_note)
    "anything2real":       (0.75, 1.0,  "Qwen Edit 2511",          "If not realistic enough, change strength or base model first."),
    "multiple_angles_fal": (0.8,  1.0,  "Qwen Edit 2511",          "Start at 0.9 and adjust."),
    "anypose":             (0.7,  0.7,  "Qwen Edit 2511 4-step",   "Both LoRA weights (base and helper) fixed at 0.7."),
    "pruna_q_2_1":         (1.0,  1.0,  "Qwen Image 2.1",          "LoRAs unmerged; keep strength at 1.0."),
    "viggle_turbo_v0_3":   (1.0,  1.0,  "Qwen Image 2.1 6-step",   "Unmerged at 1.0; merging into bf16 loses ~30% of update."),
    "lcm_lora_sd15":       (1.0,  1.0,  "SD 1.5",                  "ControlNet example: scale=1. Note: strength=0.6 in img2img is denoising, not LoRA scale."),
    # InstantID is an adapter, not a LoRA; see limits.md
}

NO_STRENGTH_CARDS = {
    "photo_to_anime_qwen_edit_2509",
    "qwen_image_2_1_lightning_4step",
    "qwen_image_lightning_8step",
    "qwen_image_edit_2511_lightning",
}


def check(card: str, strength: float) -> dict:
    """Return status and card note for a given strength value.

    Status values:
      ok          - within card range
      low         - below card minimum
      high        - above card maximum
      no_data     - card states no strength
      unknown     - card not in dataset
    """
    if card in NO_STRENGTH_CARDS:
        return {"status": "no_data", "note": "Card states no strength in archived text."}
    if card not in CARDS:
        return {"status": "unknown", "note": f"'{card}' not in dataset."}
    lo, hi, base, note = CARDS[card]
    if strength < lo:
        return {"status": "low",  "range": (lo, hi), "base": base, "note": note}
    if strength > hi:
        return {"status": "high", "range": (lo, hi), "base": base, "note": note}
    return {"status": "ok",   "range": (lo, hi), "base": base, "note": note}


if __name__ == "__main__":
    examples = [
        ("anything2real",    1.0),
        ("anything2real",    0.5),
        ("viggle_turbo_v0_3",0.8),
        ("viggle_turbo_v0_3",1.0),
        ("lcm_lora_sd15",    0.6),
        ("photo_to_anime_qwen_edit_2509", 0.9),
    ]
    for c, v in examples:
        r = check(c, v)
        print(f"{c:<30} {v:.2f}  {r['status']}  {r.get('note','')[:60]}")