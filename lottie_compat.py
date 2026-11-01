# Lottie Renderer Compatibility Checker
# Source: art_01M6AYJ7JV32VMXG3FCNFCEQSD rev 1
# Pinned commits: lottie-android 05ea92e9, lottie-react-native 7ac5e96c, ThorVG 31c5fa37
# None = undocumented at pinned commit (treat as unknown, not compatible)

RENDERERS = {
    "lottie-android": {
        "expressions": False,        # DESIGNER_NOTES: not supported
        "text_layers": False,        # DESIGNER_NOTES: not supported
        "illustrator_layers": "bitmap",
        "platforms": ["android"],
        "commit": "05ea92e9",
    },
    "lottie-react-native": {
        "expressions": None,
        "text_layers": None,
        "illustrator_layers": None,
        "platforms": ["ios", "android", "windows"],
        "commit": "7ac5e96c",
        "notes": "Requires RN 0.84+ and New Architecture",
    },
    "ThorVG": {
        "expressions": "optional",   # requires lottie_exp build flag
        "text_layers": None,
        "illustrator_layers": None,
        "platforms": ["web", "windows", "macos", "linux", "android", "ios", "embedded"],
        "commit": "31c5fa37",
    },
}

def check_compatibility(
    animation_features: dict,
    target_platform: str,
    thorvg_expressions_enabled: bool = False,
) -> dict:
    """
    animation_features: keys are feature names (str), values are bool.
      Supported keys: 'expressions', 'text_layers'
    target_platform: one of android, ios, windows, web, macos, linux, embedded
    thorvg_expressions_enabled: True if ThorVG was built with -Dextra=lottie_exp

    Returns dict of renderer_name -> {compatible: bool, reasons: list[str], commit: str}
    compatible=True with a reason means 'passes but note the caveat'.
    compatible=False means a documented hard block or platform mismatch.
    """
    results = {}
    for name, caps in RENDERERS.items():
        reasons = []
        compatible = True

        if target_platform not in caps["platforms"]:
            compatible = False
            reasons.append(f"platform '{target_platform}' not listed")

        if animation_features.get("expressions"):
            exp_cap = caps["expressions"]
            if exp_cap is False:
                compatible = False
                reasons.append("expressions not supported (documented)")
            elif exp_cap == "optional":
                if name == "ThorVG" and not thorvg_expressions_enabled:
                    compatible = False
                    reasons.append("expressions require lottie_exp build flag (off by default)")
                else:
                    reasons.append("expressions supported if lottie_exp enabled")
            elif exp_cap is None:
                reasons.append("expression support undocumented at pinned commit")

        if animation_features.get("text_layers"):
            txt_cap = caps["text_layers"]
            if txt_cap is False:
                compatible = False
                reasons.append("text layers not supported (documented)")
            elif txt_cap is None:
                reasons.append("text layer support undocumented at pinned commit")

        results[name] = {"compatible": compatible, "reasons": reasons, "commit": caps["commit"]}
    return results