from fractions import Fraction
import json

TICKS_PER_SECOND = 254_016_000_000

def frame_ticks(frame, rate):
    if type(frame) is not int or frame < 0:
        raise ValueError('frame must be a nonnegative integer')
    if not isinstance(rate, str) or '/' not in rate:
        raise ValueError('rate must be an explicit rational string, e.g. 24000/1001')
    try:
        fps = Fraction(rate)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rate') from None
    if fps <= 0:
        raise ValueError('rate must be positive')
    # Reject the entire rate if even one frame needs rounding.
    step = Fraction(TICKS_PER_SECOND, 1) / fps
    if step.denominator != 1:
        raise ValueError('rate does not map to integral ticks per frame')
    return frame * step.numerator

def plan(start, end, rate):
    a, b = frame_ticks(start, rate), frame_ticks(end, rate)
    if end <= start:
        raise ValueError('require a nonempty half-open range [start,end)')
    return {'schema': 'patch.edit-plan/1', 'rate': rate,
            'start_frame': start, 'end_frame_exclusive': end,
            'start_tick': str(a), 'end_tick_exclusive': str(b),
            'tick_unit_per_second': str(TICKS_PER_SECOND),
            'wire_mapping': 'UNVERIFIED_DO_NOT_DISPATCH'}

def tests():
    count = 0
    for rate in ('24/1', '25/1', '24000/1001', '30000/1001', '60000/1001'):
        step = frame_ticks(1, rate)
        for n in (0, 1, 1001, 10**9):
            assert Fraction(frame_ticks(n, rate), TICKS_PER_SECOND) == Fraction(n, 1) / Fraction(rate)
            assert frame_ticks(n + 1, rate) - frame_ticks(n, rate) == step
            count += 2
    left, right = plan(0, 1001, '24000/1001'), plan(1001, 2002, '24000/1001')
    assert left['end_tick_exclusive'] == right['start_tick']; count += 1
    for args in ((True, '24/1'), (-1, '24/1'), (1.0, '24/1'), (1, '23.976'), (1, '0/1'), (1, '1/0'), (1, '11/1')):
        try:
            frame_ticks(*args)
        except ValueError:
            count += 1
        else:
            raise AssertionError(args)
    try:
        plan(1, 1, '24/1')
    except ValueError:
        count += 1
    else:
        raise AssertionError('empty range accepted')
    return count

if __name__ == '__main__':
    print(json.dumps({'assertions_passed': tests(), 'sample': plan(0, 24000, '24000/1001')}, indent=2))