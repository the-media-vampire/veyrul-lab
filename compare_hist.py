import math


def compare_hist(a, b, clip_fraction=0.0158):
    """One channel, identical signal/range/binning required.

    Resolution normalization does NOT undo resampling. Display transfer is
    a hypothetical gain=1 linear hard clip, not verified TrueScope UI code.
    """
    for h in (a, b):
        if len(h) != 256 or any(type(x) is not int or x < 0 for x in h) or sum(h) == 0:
            raise ValueError('need 256 nonnegative integer counts, positive total')
    if not math.isfinite(clip_fraction) or not 0 < clip_fraction <= 1:
        raise ValueError('invalid clip fraction')
    p = [x / sum(a) for x in a]
    q = [x / sum(b) for x in b]
    da = [min(x / clip_fraction, 1.0) for x in p]
    db = [min(x / clip_fraction, 1.0) for x in q]
    return {
        'total_variation': sum(abs(x-y) for x, y in zip(p, q)) / 2,
        'modeled_display_max_difference': max(abs(x-y) for x, y in zip(da, db)),
        'same_pixel_total': sum(a) == sum(b),
        'saturated_bins_a': sum(x >= clip_fraction for x in p),
        'saturated_bins_b': sum(x >= clip_fraction for x in q),
    }


def two_peak(a, b):
    h = [0] * 256
    h[64], h[192] = a, b
    return h


if __name__ == '__main__':
    a = two_peak(5000, 5000)
    collision = compare_hist(a, two_peak(9000, 1000))
    assert math.isclose(collision['total_variation'], 0.4)
    assert collision['modeled_display_max_difference'] == 0
    scaled = compare_hist(a, two_peak(500, 500))
    assert scaled['total_variation'] == 0 and not scaled['same_pixel_total']
    assert compare_hist(two_peak(10000, 0), two_peak(0, 10000))['total_variation'] == 1
    rejected = 0
    for bad in ([0]*256, [-1]+[1]*255, [True]*256, [1]*255):
        try:
            compare_hist(a, bad)
        except ValueError:
            rejected += 1
    assert rejected == 4
    print(collision)