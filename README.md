# lottie_compat.py

Maps documented Lottie renderer limits to a given animation's features and target platform.

## Source
Built from **art_01M6AYJ7JV32VMXG3FCNFCEQSD rev 1** (documented limits only; nothing was installed or run at source read time).

## Pinned commits
| Renderer | Commit |
|---|---|
| lottie-android | 05ea92e9 |
| lottie-react-native | 7ac5e96c |
| ThorVG | 31c5fa37 |

## Usage
```python
from lottie_compat import check_compatibility

result = check_compatibility(
    animation_features={"expressions": True, "text_layers": False},
    target_platform="android",
    thorvg_expressions_enabled=False,  # set True if built with -Dextra=lottie_exp
)
for renderer, info in result.items():
    mark = "OK" if info["compatible"] else "FAIL"
    print(f"{mark} {renderer}: {info['reasons']}")
```

## Limits
- Matrix reflects documentation only; no renderer was installed or run.
- `None` means undocumented at the pinned commit, not confirmed compatible.
- lottie-react-native expression/text support is `None` (not addressed in read docs).
- Update the RENDERERS dict when commits advance.

## Next improvement
Read ThorVG Lottie support wiki (linked from its README but not read at source-inspection time) to fill in text-layer and feature detail for ThorVG.