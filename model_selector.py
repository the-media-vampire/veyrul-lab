# model_selector.py
# Source: art_01M66YP3XWTDRSW8X0YA8R8AQV revision 1
# All VRAM / step / guidance figures are vendor card claims, NOT measurements.
# Licence names are as stated on the cards; licence text was not reviewed.

MODELS = [
    {
        "name": "FLUX.2 klein 4B",
        "params_b": 4,
        "vram_gb": 13,
        "licence": "Apache-2.0",
        "commercial": True,
        "steps": 4,
        "guidance": 1.0,
        "multi_ref": True,
        "notes": "4B params; 4-step distilled; multi-reference editing",
    },
    {
        "name": "Qwen-Image-Edit-2511",
        "params_b": None,
        "vram_gb": None,   # not stated on card
        "licence": "Apache-2.0",
        "commercial": True,
        "steps": 40,
        "guidance": 4.0,   # card calls this 'true CFG 4.0'
        "multi_ref": True,
        "notes": "40 steps, true CFG 4.0; mitigated image drift; VRAM not on card",
    },
    {
        "name": "FLUX.2 klein 9B (Unsloth mirror)",
        "params_b": 9,
        "vram_gb": 29,
        "licence": "non-commercial",
        "commercial": False,
        "steps": 4,
        "guidance": 1.0,
        "multi_ref": True,
        "notes": "Read via Unsloth ungated mirror; non-commercial licence",
    },
    {
        "name": "FLUX.2 klein 9B-KV",
        "params_b": 9,
        "vram_gb": 29,
        "licence": "non-commercial",
        "commercial": False,
        "steps": 4,
        "guidance": 1.0,
        "multi_ref": True,
        "notes": "KV-cache on ref images; up to 2.5x faster multi-ref (card claim)",
    },
    {
        "name": "FLUX 3 Image Klein (ml-resources mirror)",
        "params_b": 5.6,
        "vram_gb": None,        # card gives file size, not VRAM
        "vram_file_gb": 11.1,   # bf16 checkpoint size only
        "licence": "Kommunity",
        "commercial": "conditional",
        "steps": 50,
        "guidance": 3.5,
        "multi_ref": True,
        "notes": "Up to 10 refs; 11.1 GB bf16 file; needs prompt upsampler; unofficial mirror",
    },
]


def select_models(vram_budget_gb: float, commercial_only: bool = False):
    """
    Filter models by VRAM budget and optional commercial-licence requirement.

    Returns (viable, unknowns) where:
    - viable: models with card-stated VRAM <= budget
    - unknowns: models whose VRAM is not stated on the card (always returned
      unless filtered out by commercial_only)

    All comparisons are against vendor card figures, not measurements.
    """
    viable, unknowns = [], []
    for m in MODELS:
        if m["vram_gb"] is None:
            unknowns.append(m)
        elif m["vram_gb"] <= vram_budget_gb:
            viable.append(m)

    if commercial_only:
        viable = [m for m in viable if m["commercial"] is True]
        unknowns = [m for m in unknowns if m["commercial"] is True]

    return viable, unknowns