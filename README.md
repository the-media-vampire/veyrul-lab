# CutMapContract

A small Python validator for audio-led cut-map prompts, as documented in
`art_01M681XTD8NSXT3N2KQF8NQFZB` r1 (Veyrul). Structurally distinct from
`BeatOrderContract` (artifact `8670325a`) which targets narrative portrait
structure in the twelve-block workflow (`art_01M67CGQR5M8AXXN18VH6Z4ETM` r1).

## What it checks

| Check | Mismatch source |
|---|---|
| Beat timestamps time-ordered | authoring error |
| All beats within clip duration | authoring error |
| Each beat: music_event, camera_move, cut_type | authoring error |
| Camera direction per beat | mismatch-3 (toward vs backward) |
| world_head_count declared | mismatch-1 (dancer count drift) |
| >= 3 fence negatives on audio block | prompt structure requirement |
| final_pose_described precisely | mismatch-6 (arm count wrong) |
| loopable_end declared | recipe requirement |

## What it cannot check

- Whether the model complies with any beat (compliance is partial, per r1)
- Sound alignment — whether cuts land on kicks/snares (sound not verified)
- Macro insert timing within sub-second gaps between stills
- Whether a supplied audio reference is valid or licensed

## License
MIT. Source: Veyrul lab.