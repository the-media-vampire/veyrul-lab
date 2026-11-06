# LosslessCut batch trim: output check and command review

Source: art_01M6KMVTQZT2J390V3Z12FJF4K revision 3 (source_inspected / not_run).  
All items below map to documented behavior; nothing here was executed.

---

## After exporting a test clip (rule 5)

The docs say the only way to review exported cutpoints is to run the export  
and check the output. Check these on the **first file before running a batch**:

| What to check | Why it matters (from docs) |
|---|---|
| **Duration** matches your intended segment length (within one keyframe interval) | Lossless cuts land at the keyframe before your point; a large gap signals a sparse-keyframe file |
| **Audio track count** matches the original | Disabling unneeded tracks can silently drop audio and cause wrong duration |
| **Playback at the cut boundary** (first and last second) | A file that won't play may carry the wrong codec tag (e.g. hev1 vs hvc1 for H.265) |
| **File is in a different folder from the original** | The docs say overwriting input is not allowed by design; a same-folder output with a conflicting name is a risk |
| **File is not in a cloud-synced folder** during export | Docs explicitly flag cloud-sync folders as a problem source |

If any check fails, change **one setting at a time** (rule 4) before re-running.

---

## Before running a generated FFmpeg command (rule 7)

The docs say a language model can help write batch scripts but give no  
verification step. Before running any generated command, confirm:

1. **Input path is explicit and correct.** A generated command may use a  
   placeholder (e.g. `input.mp4`). Substitute the actual file path and  
   verify it exists before running.

2. **Output path goes to a different folder from the input.**  
   FFmpeg will overwrite a file at the output path without prompting by default.

3. **The command does not contain `-vf`, `-af`, `-vcodec libx264` or similar  
   re-encoding flags** unless you intend to re-encode. Lossless copy uses  
   `-c copy`; a re-encode flag on 40 clips is a large silent cost.

Try the command on **one copy** of one file and apply rule 5 checks above  
before running it across the batch.

---

## What this checklist does not cover

- Smart cut behavior (rule 3): experimental, not recommended for problem files.
- Merge compatibility (rule 6): only merge clips with identical codec parameters.
- Detection quality (rule 8): treat detected cut points as suggestions; inspect before exporting.
- EDL/FCP handoff (rule 9): apply effects in the editor after handing over segments.

See art_01M6KMVTQZT2J390V3Z12FJF4K r3 for the full nine-rule checklist.