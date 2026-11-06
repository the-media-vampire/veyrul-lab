# Open assumptions and blockers

## Must resolve before combining
1. **OSC bridge**: Mixxx OSC output configuration not documented in staged chapters.
   Research needed: does Mixxx support OSC out natively, or does it require a controller mapping script?
2. **Audio bus**: JACK routing between Mixxx main out and ChucK dac not demonstrated.
3. **ChucK license**: `rqr_01M6QD9G5ZTQ26GF3JWBGKRVQR` (prior session) queued but status unknown here.
   Block: cannot redistribute adapter_sketch.ck patterns if ChucK examples are unresolved.
4. **Jitter**: ChucK logical time vs. wall clock drift over a full DJ set — not answerable from sources.
5. **Reverb exception**: Mixxx manual names Reverb as the one effect that does NOT follow deck tempo.
   ChucK equivalent (JCRev, NRev) also has no tempo parameter — consistent gap, not a conflict.

## Safe to proceed without resolving
- BPM→duration conversion formula (pure math, no dependency)
- Bounded shred termination pattern (no license constraint on the pattern itself)
- Mixxx recording: use Mixxx's own recorder; ChucK side irrelevant