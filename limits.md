# Limits — model_selector.py

Source: `art_01M66YP3XWTDRSW8X0YA8R8AQV` revision 1

## What the data is
- Every VRAM, step and guidance figure is a **vendor card claim**, not a measured result.
- Licence names are as stated on cards; licence text was not reviewed.

## Known gaps
| Model | Gap |
|---|---|
| Qwen-Image-Edit-2511 | VRAM not stated on card; returned in `unknowns` bucket |
| FLUX 3 Image Klein | VRAM not stated; `vram_file_gb=11.1` is checkpoint size, not runtime VRAM |
| FLUX 3 Image Klein | Read via ml-resources ComfyUI mirror, not official owner card |
| FLUX.2 klein 9B | Read via Unsloth ungated mirror |
| FLUX.1 Kontext dev | Not included; no archived card source |
| FLUX 3 Klein official | Not included; card is gated |

## Commercial flag semantics
- `True` = Apache-2.0 as stated on card
- `False` = non-commercial as stated on card
- `"conditional"` = Kommunity licence with commercial exception for Qualifying Users; consult the actual licence before use

## Next improvement
When actual VRAM measurements exist for Qwen-Image-Edit-2511 and FLUX 3 Image Klein,
add a `vram_measured_gb` field and update `select_models` to prefer it over the card figure.