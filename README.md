# ink runtime loop reference (Python)

Models the Continue/ChooseChoiceIndex loop documented in inkle/ink commit 35c63e52.
Source: art_01M6CFFV3P2X8HW39BHHK0H0W5 rev 2.

## What this is
A minimal teaching/test harness. Not a full ink engine. The real engine is
inklecate (C#); this mirrors only the API surface documented in RunningYourInk.md.

## JSON format
Top-level fields `inkVersion` and `root` match the documented format.
The `passages` array is a simplified stand-in for real inklecate-compiled `root` containers.

## Usage
```python
from ink_loop import InkStory, run_story
import json

with open('example_story.json') as f:
    story = InkStory(f.read())

# Scripted (for tests)
run_story(story, choice_fn=lambda cs: 0)

# Interactive
run_story(story, choice_fn=lambda cs: int(input('> ')))
```

## Limits
- No VAR variables, diverts, gathers, tunnels, threads, tags or external functions.
- once-only choices not modelled.
- Real inklecate JSON root format differs; replace InkStory._passages with a real parser.

## Next improvement
Wire `inkVersion` to a version check and add a shim that accepts real inklecate JSON.