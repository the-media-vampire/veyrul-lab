# Pre-flight assumptions checklist for CI integration

Run this checklist before wiring EffectCraft into a CI pipeline.
All items are derived from documentation at commit 9dd3193c (art_01M6B226HF13MGFQTTDXSPZSW1 rev 1).

- [ ] `effectcraft-cli --version` returns 0.19.x or the target version
- [ ] System Compatibility Report confirms GPU compositor is active
      (if not, size CI runner for CPU throughput)
- [ ] All footage paths in .ecproj are relative and resolve next to the project file
      (absolute paths from a dev machine will break on the CI runner)
- [ ] Target export format is confirmed in the build's Output Module list
      (H.264, HEVC, AV1, QuickTime ProRes, QuickTime Uncompressed, PNG Sequence,
       JPEG Sequence, Lottie JSON — alpha channel requires QuickTime or PNG Sequence)
- [ ] MCP bridge port 9877 is not blocked if using bridge mode
- [ ] `--automation-read-root` and `--automation-write-root` are set to the
      directories the runner has read/write access to
- [ ] No .aep/.aepx source files are expected — EffectCraft cannot open them
- [ ] CI timeout budget accounts for CPU fallback render time
- [ ] Retry logic treats only explicitly idempotent commands as safe to replay