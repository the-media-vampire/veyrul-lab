# Baseline vs Camera-Locked V2V Checklist

Source: art_01M6B5GAK8852X5K2DNWV7F22Z r1

For each pair of outputs (baseline / locked), score these rows 0/1:

| Signal | Baseline | Locked | Notes |
|---|---|---|---|
| Camera drift vs source (landmark stays fixed?) | | | Spot-check 3 frames |
| Cut timing preserved (frame count matches input?) | | | Count output frames |
| Subject lighting direction matches BG source | | | Inspect shadow angle |
| Audio track unchanged | | | Waveform comparison |
| Simultaneous-addition cap respected (overlay) | | | Count new elements per second |
| Unwanted background alteration | | | Compare background crops |

**Minimum useful test**: run Prompt A and Prompt B on the same 5-second clip.
Record which signals differ. One generation each is enough to detect gross failures.

**What does not tell you**: A passing score here does not confirm the method
generalises to longer clips, different models or different subject types.