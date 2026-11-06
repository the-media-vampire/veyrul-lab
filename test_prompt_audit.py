"""Tests for prompt_state_audit.py — documented expected results, source not executed.

Baseline (control): prompt contains no ledger terms → 0% coverage.
Experiment rows add terms one at a time to establish coverage sensitivity.
"""
from prompt_state_audit import ShotRecord, audit_prompt, audit_sequence

SHOT = ShotRecord(
    shot_id='S01',
    character='Mara Voss',
    location='rain-soaked rooftop',
    costume_note='long dark coat',
    status='approved',
)


def test_baseline_empty_prompt():
    """Control: empty prompt → 0 covered, 3 missing, ratio=0."""
    r = audit_prompt(SHOT, '')
    assert r.covered == []
    assert set(r.missing) == {'character', 'location', 'costume_note'}
    assert r.ratio == 0.0
    assert not r.passed


def test_partial_prompt_one_field():
    """Only character name present → 1 covered, 2 missing."""
    r = audit_prompt(SHOT, 'Mara stands at the edge of the frame.')
    assert 'character' in r.covered
    assert 'location' in r.missing
    assert 'costume_note' in r.missing
    assert r.ratio == 1/3


def test_full_coverage():
    """All three ledger terms present → 100% coverage, passed=True."""
    prompt = 'Mara Voss on a rain-soaked rooftop wearing a long dark coat, still.'
    r = audit_prompt(SHOT, prompt)
    assert r.passed
    assert r.ratio == 1.0
    assert r.missing == []


def test_sequence_audit():
    """Two-shot sequence: S01 full, S02 missing costume. Aggregate shows the gap."""
    shot2 = ShotRecord(
        shot_id='S02', character='Mara Voss',
        location='rain-soaked rooftop', costume_note='long dark coat',
    )
    pairs = [
        (SHOT, 'Mara Voss on a rain-soaked rooftop wearing a long dark coat.'),
        (shot2, 'Mara Voss on the rooftop looks up.'),
    ]
    results = audit_sequence(pairs)
    assert results[0].passed
    assert not results[1].passed
    assert 'costume_note' in results[1].missing


def test_known_false_negative_paraphrase():
    """KNOWN LIMIT: paraphrase of costume_note ('heavy black overcoat')
    does not match 'long dark coat'; marked missing despite semantic equivalence.
    This is the same weakness as ad06e2e2 exact-string costume comparison.
    This test documents the limit, not a bug to fix immediately.
    """
    prompt = 'Mara Voss on a rain-soaked rooftop in a heavy black overcoat.'
    r = audit_prompt(SHOT, prompt)
    # costume_note will be in missing despite being semantically present
    assert 'costume_note' in r.missing  # expected false-negative