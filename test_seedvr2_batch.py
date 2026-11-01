"""Minimal tests for seedvr2_batch.py"""
import pytest
from seedvr2_batch import is_valid_batch_size, next_valid, prev_valid, plan_batches


def test_valid_sizes():
    assert [b for b in range(1, 26) if is_valid_batch_size(b)] == [1,5,9,13,17,21,25]

def test_invalid_sizes():
    for b in [2,3,4,6,7,8,10,11,12,14,15,16,32]:
        assert not is_valid_batch_size(b), b

def test_nearest_helpers():
    assert next_valid(8) == 9
    assert prev_valid(8) == 5
    assert next_valid(33) == 33
    assert prev_valid(33) == 33

def test_readme_example_uniform():
    # README: 45 frames, batch_size=33, uniform -> two batches of 33
    batches = plan_batches(45, 33, uniform=True)
    assert len(batches) == 2
    assert batches[0].effective_frames == 33 and not batches[0].padded
    assert batches[1].effective_frames == 33 and batches[1].padded
    assert batches[1].actual_frames == 12

def test_no_uniform():
    batches = plan_batches(45, 33, uniform=False)
    assert batches[1].effective_frames == 12 and not batches[1].padded

def test_invalid_batch_raises():
    with pytest.raises(ValueError, match="4n\\+1"):
        plan_batches(45, 12)

def test_single_frame():
    batches = plan_batches(1, 1)
    assert len(batches) == 1 and batches[0].effective_frames == 1