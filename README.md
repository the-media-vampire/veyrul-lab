# Sampled observations -> editorial review cues

Run: `python3 review_cues.py` (Python standard library only).

Original MIT code by Patch, an AI collaborator for Veyrul. Conceptual context: art_01M64VKK2MPWCZP03XDVGKHM5S revision 2. No source text, media, or exact founder timestamps are packaged. Synthetic fixtures are not observations of those runs.

Input contract: list of dictionaries with required `t` (finite nonnegative seconds, strictly increasing) and `label` (a consistently assigned string or None for unknown). Caller must validate label vocabulary and maintain an external manifest with source ID/revision, run ID, media timebase, observer, sampling method, asset rights evidence, and permitted operations. The function does not enforce rights or validate that metadata is truthful.

Output: JSON-compatible cue list for human editorial review. Import intervals as review markers, NOT cuts, EDL entries or verified holds. Adjacent differing labels bracket a sampled difference; unknown intervening samples are not bridged. Equal labels can conceal intervening events. Empty cues do not mean a continuous shot. Audio is not assessed.

Compare with an edit-decision workflow: an EDL requires verified edit points and media mapping; this adapter deliberately stops at review intervals. Inspect authorized full playback before assigning cuts, transitions or durations. A source revision and original timebase must accompany exports; approximate cadence must not be expanded into invented timestamps.

License applies only to this original package, not source media or third-party records. No media consumption is required to run synthetic tests. A reviewed authorization record for each intended asset operation is required before adapting this to real media. Fixed seeds alone do not isolate causal effects: hold model/configuration and input assets constant and vary one factor across multiple paired seeds.