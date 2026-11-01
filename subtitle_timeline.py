"""Original timeline arithmetic; seconds, hard cuts, unit playback speed.
Input segments: source/start/end in output order.
Input cues: id/source/start/end in source time.
Clipped cues require review; this function does not establish safe word cuts.
"""

def map_cues(segments, cues):
    """Intersect half-open source intervals, map to output, retain provenance."""
    out = []
    cursor = 0.0
    for index, seg in enumerate(segments):
        start, end = seg['start'], seg['end']
        if end <= start:
            raise ValueError('segment must have positive duration')
        for cue in cues:
            if cue['source'] != seg['source']:
                continue
            lo, hi = max(start, cue['start']), min(end, cue['end'])
            if hi > lo:
                out.append(dict(id=cue['id'], segment=index,
                    start=cursor + lo-start, end=cursor + hi-start,
                    clipped=(lo != cue['start'] or hi != cue['end'])))
        cursor += end-start
    return out