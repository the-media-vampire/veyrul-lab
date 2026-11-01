"""ltx23_i2v_footprint.py
Mandatory vs optional file manifest for ComfyUI template video_ltx2_3_i2v.
Sizes are template_bytes from art_01M6BYD28NTGF22DVC33XQ60FH revision 2.
Decimal units assumed (units basis not stated in source). Nothing is downloaded.
"""

FILES = [
    {
        "name": "ltx-2.3-22b-dev-fp8.safetensors",
        "folder": "checkpoints",
        "size_gb": 27.14,
        "mandatory": True,
        "nodes": [316, 279, 317],
        "note": "Used by checkpoint, audio VAE and text-encoder loaders; no switch",
    },
    {
        "name": "ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors",
        "folder": "loras",
        "size_gb": 2.55,
        "mandatory": True,
        "nodes": [285],
        "note": "LoRA loader; model output feeds main pipeline; saved strength 0.5",
    },
    {
        "name": "ltx-2.3-spatial-upscaler-x2-1.1.safetensors",
        "folder": "latent_upscale_models",
        "size_gb": 0.9496,
        "mandatory": True,
        "nodes": [311],
        "note": "Spatial upscaler in main pipeline path",
    },
    {
        "name": "gemma_3_12B_it_fp4_mixed.safetensors",
        "folder": "text_encoders",
        "size_gb": None,  # NOT stated in template note
        "mandatory": True,
        "nodes": [317],
        "note": "Text encoder; size NOT stated in template; verify before download",
    },
    {
        "name": "<gemma_lora — filename not given in record>",
        "folder": "loras",
        "size_gb": 0.5991,
        "mandatory": False,
        "nodes": [324],
        "note": "Prompt-enhance path only; switch (node 327) default=false; skippable",
    },
]


def footprint_report(decimal=True):
    unit = "GB (decimal assumed)" if decimal else "GB (binary GiB assumed)"
    mandatory_known = sum(f["size_gb"] for f in FILES if f["mandatory"] and f["size_gb"] is not None)
    optional_known = sum(f["size_gb"] for f in FILES if not f["mandatory"] and f["size_gb"] is not None)
    return {
        "mandatory_known_gb": round(mandatory_known, 4),
        "mandatory_unknown": [f["name"] for f in FILES if f["mandatory"] and f["size_gb"] is None],
        "optional_skippable_gb": round(optional_known, 4),
        "partial_sum_4_files_gb": round(mandatory_known + optional_known, 4),
        "unit_basis": unit,
        "source": "art_01M6BYD28NTGF22DVC33XQ60FH revision 2 (template_bytes)",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(footprint_report(), indent=2))
    print()
    for f in FILES:
        flag = "MANDATORY" if f["mandatory"] else "OPTIONAL"
        size = f"{f['size_gb']} GB" if f["size_gb"] is not None else "SIZE UNKNOWN"
        print(f"[{flag}] {f['folder']}/{f['name']}  {size}")
        print(f"         {f['note']}")