"""Source-only arithmetic oracle; no FFmpeg execution or audio validation.
Reference: art_01M6SNVGQ86GDSESP316R61M6Q revision 1.
All intervals are half-open sample ranges, safely away from file edges.
"""
import unittest


def predicted_samples(ranges, overlap, reach):
    """Model exactly the described inner-edge extension, not cuts.py logic.

    Assumes every requested sample exists, sufficient segment lengths,
    and overlap is consumed once per join by the renderer.
    """
    if not ranges or any(b <= a for a, b in ranges):
        raise ValueError('need nonempty positive ranges')
    if overlap < 0 or reach < 0:
        raise ValueError('negative overlap/reach')
    lengths = []
    for i, (a, b) in enumerate(ranges):
        left = reach if i else 0
        right = reach if i < len(ranges) - 1 else 0
        lengths.append(b - a + left + right)
    return sum(lengths) - (len(ranges) - 1) * overlap


class DurationOracle(unittest.TestCase):
    def test_two_segments_even_overlap(self):
        r = [(1000, 3000), (5000, 7000)]
        self.assertEqual(predicted_samples(r, 0, 0), 4000)  # hard cut
        self.assertEqual(predicted_samples(r, 440, 220), 4000)
        self.assertEqual(predicted_samples(r, 440, 0), 3560)
        self.assertNotEqual(predicted_samples(r, 440, 220), 3780)

    def test_three_segments(self):
        r = [(1000, 3000), (5000, 7000), (9000, 11000)]
        self.assertEqual(predicted_samples(r, 440, 220), 6000)
        self.assertEqual(predicted_samples(r, 440, 0), 5120)

    def test_even_rounding_at_common_rates(self):
        r = [(1000, 3000), (5000, 7000)]
        for sr, expected_overlap in [(44100, 440), (48000, 480)]:
            x = round(sr * .01) // 2 * 2
            self.assertEqual(x, expected_overlap)
            self.assertEqual(predicted_samples(r, x, x // 2), 4000)

    def test_odd_overlap_exposes_one_sample_per_join(self):
        r = [(1000, 3000), (5000, 7000), (9000, 11000)]
        self.assertEqual(predicted_samples(r, 441, 220), 5998)

    def test_no_join(self):
        self.assertEqual(predicted_samples([(1000, 3000)], 440, 220), 2000)


if __name__ == '__main__':
    unittest.main()