def gate(samples, *, complete_sequence=False, identity_verified=None, effect_approved=None):
    """Caller supplies observations, not detections. None means unknown."""
    if not samples:
        return {'decision':'review','reasons':['no_samples']}
    seen=set()
    for s in samples:
        t=s['t']
        if isinstance(t,bool) or not isinstance(t,(int,float)) or not (0 <= t < float('inf')) or t in seen:
            raise ValueError('timestamps must be unique, finite, nonnegative')
        seen.add(t)
        for k in ('door_closed','crossing'):
            if s.get(k) is not None and type(s[k]) is not bool:
                raise ValueError(k+' must be bool or None')
    failures=[]
    for s in samples:
        if s.get('door_closed') is False:
            failures.append({'rule':'closed_throughout','t':s['t'],'evidence':s.get('evidence')})
            if s.get('crossing') is True:
                failures.append({'rule':'closed_at_crossing','t':s['t'],'evidence':s.get('evidence')})
    if failures:
        return {'decision':'reject','failures':failures}
    pending=[]
    if not complete_sequence: pending.append('temporal_coverage')
    if not any(s['t']==0 for s in samples): pending.append('frame_zero')
    if any(s.get('door_closed') is None for s in samples): pending.append('unknown_door_state')
    if identity_verified is not True: pending.append('reference_identity')
    if effect_approved is not True: pending.append('effect_review')
    pending.append('playback_and_motion_review')
    return {'decision':'review','reasons':pending}