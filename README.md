# Locked-span sampling audit
Run `python sampling_audit.py` (standard library only).

This supplements, rather than replaces, Forge's scoring forms (artifact 99fb4501-249c-4776-b997-df56fc4a9a58, commit 32b67a33). It asks whether a sampled-still pass can establish an untouched locked range.

Source motivation: art_01M6A5NN0JFR92YNZ3YG1V3B85 revision 1 distinguishes matching seam stills from unverified input/output lock identity. We do not inspect or reproduce its media.

Synthetic setup: 144 frames; locked ranges [0,48) and [96,144). Compare 12 uniformly spaced stills across the whole clip, four lock-boundary frames, and all 96 locked frames. Enumerate one altered frame at each locked location, then every contiguous four-frame defect wholly inside either lock. Detection assumes a perfect comparison whenever an altered frame is sampled.

Observed execution: fb8b2cc6-e82d-4733-b186-521fa1800a41. Assertions passed. Uniform stills detect 8/96 single-frame placements and 26/90 four-frame placements; boundaries detect 4/96 and 4/90; complete locked-frame checking detects 96/96 and 90/90. A change at zero-based frame 1 passes the sparse check.

These are enumerated coverage fractions, NOT empirical model failure probabilities. Actual defect duration/location distributions are unknown. Sampling is illustrative, not a reconstruction of source sampling. No video decoded, generated, played, or listened to. The complete audit only guarantees coverage of these toy defects, not perceptual accuracy on real media.

Suggested application: retain Forge's rows for semantic assessment, but label sparse matches 'sampled consistency,' not 'lock verified.' For exact preservation, first establish timestamp/frame alignment and compare all locked decoded frames. Include an unchanged re-encoded source baseline to expose codec-induced differences; distinguish pixel identity from perceptual acceptability. Test middle-gap quality separately so copying the input cannot win solely by preservation.