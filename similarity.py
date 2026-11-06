"""Shared similarity utility for shot-ledger consistency checks.

Motivation: art_01M6HRDNCF7PCNDKZNAN1K6R1X r3 open problem:
  'inconsistent temporal coherence: frame-to-frame continuity breaks
   down in longer sequences.'

Used by:
  - cross_shot_v2.py (c3feea2d): costume-note drift detection
  - audit_prompt()  (c5ffe102): prompt-state coverage auditing

Strategy
--------
First compute word-Jaccard. If it clears the threshold, done.
If it falls below, compute character-trigram Jaccard as a fallback;
return the MAXIMUM of the two. This handles:
  - paraphrases (same words, different order): word-Jaccard already
    covers these after tokenisation
  - morphological variants / near-spellings: trigrams help
Known remaining limit: distant synonyms with different letter sequences
('jacket' vs 'coat') still score low on both measures. That requires a
model-based approach and is noted as the next open improvement.
"""
from __future__ import annotations


def _word_tokens(text: str) -> set[str]:
    return {w.strip('.,;:\'"').lower() for w in text.split()
            if w.strip('.,;:\'"')}


def _trigrams(text: str) -> set[str]:
    s = text.lower()
    if len(s) < 3:
        return {s} if s else set()
    return {s[i:i+3] for i in range(len(s) - 2)}


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def similarity(text_a: str, text_b: str) -> float:
    """Return combined similarity score in [0, 1].

    Takes max(word_jaccard, trigram_jaccard) so that either
    lexical overlap or sub-word overlap can rescue a near-match.
    """
    word_sim = _jaccard(_word_tokens(text_a), _word_tokens(text_b))
    trig_sim = _jaccard(_trigrams(text_a), _trigrams(text_b))
    return round(max(word_sim, trig_sim), 3)