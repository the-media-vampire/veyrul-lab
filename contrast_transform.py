"""Contrast-reduction arithmetic for versions A, B, C.
Executed result (exit 0): run_python artifact dc914eb9-45f8-4de0-81df-a665ee61ec38
"""

def compress_to_mid(v: int, factor: float = 0.5) -> int:
    """Linear compression toward mid-gray (127)."""
    return round(v + (127 - v) * factor)

# Approx values from fixture inspection (artifact d269ac62)
doorway_A = (245, 240, 224)
bg_A      = (13, 13, 13)
figure_A  = (128, 128, 128)

doorway_B = tuple(compress_to_mid(c) for c in doorway_A)  # (186, 184, 176)
bg_B      = bg_A

bg_C      = tuple(compress_to_mid(c) for c in bg_A)  # (70, 70, 70)
doorway_C = doorway_A

def luminance(rgb):
    return 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]

if __name__ == '__main__':
    for name, d, b in [('A', doorway_A, bg_A), ('B', doorway_B, bg_B), ('C', doorway_C, bg_C)]:
        c = abs(luminance(d) - luminance(b))
        print(f'Ver {name}: doorway={d}  bg={b}  contrast={c:.1f}')