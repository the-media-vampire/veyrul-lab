"""Predict luminance contrast for a pygfx transparency experiment.

Context: Iris's 'Reveal the signal, quiet the structure' brief
[art_01M6F68R6DTRP106T3W8BRANEK, revision 3].

All colors are sRGB tuples (R, G, B) in [0, 1].
Blending uses straight alpha-composite in linear light.
"""

def to_linear(c: float) -> float:
    """sRGB component to linear light."""
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminance(r: float, g: float, b: float) -> float:
    """WCAG relative luminance."""
    return 0.2126 * to_linear(r) + 0.7152 * to_linear(g) + 0.0722 * to_linear(b)


def wcag_contrast(L1: float, L2: float) -> float:
    lighter, darker = max(L1, L2), min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)


def blend_luminance(fg_rgb, alpha: float, bg_rgb) -> float:
    """Luminance of fg composited over bg at given alpha."""
    fg_lin = [to_linear(c) for c in fg_rgb]
    bg_lin = [to_linear(c) for c in bg_rgb]
    comp = [alpha * fg_lin[i] + (1 - alpha) * bg_lin[i] for i in range(3)]
    return 0.2126 * comp[0] + 0.7152 * comp[1] + 0.0722 * comp[2]


def report(focal_rgb=(1.0, 0.6, 0.0),
           surround_rgb=(0.0, 0.8, 0.8),
           bg_rgb=(0.08, 0.08, 0.08),
           panel_alpha: float = 0.25):
    """Print contrast table for Control / Condition A / Condition B."""
    L_focal   = luminance(*focal_rgb)
    L_surround = luminance(*surround_rgb)
    L_bg      = luminance(*bg_rgb)

    # Control: all opaque
    ctrl_f_bg = wcag_contrast(L_focal, L_bg)
    ctrl_s_bg = wcag_contrast(L_surround, L_bg)
    ctrl_f_s  = wcag_contrast(L_focal, L_surround)

    # Condition A: focal opaque, surround at panel_alpha
    L_s_A = blend_luminance(surround_rgb, panel_alpha, bg_rgb)
    A_f_s = wcag_contrast(L_focal, L_s_A)
    A_f_bg = ctrl_f_bg  # unchanged

    # Condition B: both at panel_alpha
    L_f_B = blend_luminance(focal_rgb, panel_alpha, bg_rgb)
    L_s_B = blend_luminance(surround_rgb, panel_alpha, bg_rgb)
    B_f_s  = wcag_contrast(L_f_B, L_s_B)
    B_f_bg = wcag_contrast(L_f_B, L_bg)

    print(f"{'Condition':<14} {'Focal:Surround':>16} {'Focal:BG':>10}")
    print("-" * 44)
    print(f"{'Control':<14} {ctrl_f_s:>15.2f}:1 {ctrl_f_bg:>9.2f}:1")
    print(f"{'A (sel. transp)':<14} {A_f_s:>15.2f}:1 {A_f_bg:>9.2f}:1")
    print(f"{'B (shared transp)':<14} {B_f_s:>15.2f}:1 {B_f_bg:>9.2f}:1")
    print()
    print("Scout note: if A >> Control on Focal:Surround but Control >> A on")
    print("Focal:BG, transparency helps disambiguation but weakens pop. This")
    print("suggests a D-condition swap (interchange focal/surround colors) to")
    print("test whether alpha or hue is the primary load-bearing variable.")


if __name__ == "__main__":
    report()