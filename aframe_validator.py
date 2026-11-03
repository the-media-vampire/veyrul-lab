"""A-Frame HTML snippet validator.
Rules sourced from: art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1

Only tests what the documentation states; does not load or render anything.
"""
import re

# Documented renderer system properties (renderer page, art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1)
VALID_RENDERER_PROPS = {
    "antialias", "colorManagement", "sortTransparentObjects",
    "toneMapping", "anisotropy", "stencil"
}

def baseline_check(html: str) -> list[str]:
    """Naive baseline: only checks for a-scene presence."""
    issues = []
    if "<a-scene" not in html:
        issues.append("MISSING: <a-scene> not found")
    return issues

def structured_check(html: str) -> list[str]:
    """Structured validator using documented A-Frame rules."""
    issues = []

    # Rule 1: a-scene required (intro page + README, art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1)
    if "<a-scene" not in html:
        issues.append("MISSING a-scene: documented as required root element")

    # Rule 2: gltf-model src must be .glb, .gltf, or a #asset-ref
    #         (gltf-model page, art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1)
    gltf_attrs = re.findall(r'gltf-model=["\'](["\']+)["\']', html)
    for src in gltf_attrs:
        if not (src.endswith(".glb") or src.endswith(".gltf") or src.startswith("#")):
            issues.append(
                f"gltf-model src '{src}' does not end in .glb/.gltf "
                "or use asset ref #id"
            )

    # Rule 3: renderer attributes must be in documented property set
    #         (renderer page, art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1)
    renderer_attrs = re.findall(r'renderer=["\'](["\']+)["\']', html)
    for attr_str in renderer_attrs:
        pairs = [p.strip() for p in attr_str.split(";") if p.strip()]
        for pair in pairs:
            key = pair.split(":")[0].strip()
            if key and key not in VALID_RENDERER_PROPS:
                issues.append(
                    f"renderer property '{key}' not in documented set "
                    f"{sorted(VALID_RENDERER_PROPS)}"
                )

    # Rule 4: a-asset-item should carry an id for # references
    #         (gltf-model page example, art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1)
    asset_items = re.findall(r'<a-asset-item([^>]*)>', html)
    for attrs in asset_items:
        if 'id=' not in attrs:
            issues.append(
                "a-asset-item missing id attribute "
                "(needed for # src reference per gltf-model example)"
            )

    # Rule 5: A-Frame must be included via CDN script or AFRAME import
    #         (installation page, art_01M6FH0RNNGRQAXE0CHRXHB3B2 r1)
    has_aframe = (
        'src="https://aframe.io' in html
        or "import AFRAME" in html
        or "aframe.min.js" in html
    )
    if not has_aframe:
        issues.append(
            "No A-Frame CDN script or AFRAME import detected "
            "(documented install methods: CDN, npm install aframe)"
        )

    return issues