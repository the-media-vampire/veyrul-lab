# Experiment brief: JSONC `llm` key vs Python-side LLM object

**Source:** `art_01M6W0HBATRWPKZ37KQXAYMSY5` revision 1  
**Gap quoted verbatim:** "The pages read do not show how an LLM object is attached to a JSONC agent."

## The discriminating question

Does CrewAI's JSON-first scaffold accept an `llm` key directly in the agent JSONC file, or must the LLM object be constructed in Python and injected at crew-build time?

Three possible outcomes, three different beliefs:

| Outcome | Belief updated |
|---|---|
| Arm A (JSONC key) works, Arm B not needed | JSONC is self-sufficient; Python wiring is optional |
| Arm B (Python injection) works, Arm A silently ignored | JSONC has no `llm` key; Python is the only path |
| Both arms work | Framework accepts either; JSONC key may override Python object |
| Neither arm works | Misconfiguration in both; check Ollama server and litellm extra |

## Held variables (do not change between arms)

- Same Ollama model name and URL
- Same `agents/outliner.jsonc` role, goal, backstory
- Same `crew.jsonc` task text, expected output, output file
- Same `crewai run` command; only the LLM wiring mechanism changes
- Pin `--revision` / commit if pulling from git so environment is identical

## Arm A — JSONC `llm` key

Add an `llm` block directly in `agents/outliner.jsonc` (untested; key name is our hypothesis):

```jsonc
{
  "role": "{genre} Story Outliner",
  "goal": "Turn a one-line premise into a clear three-beat outline",
  "backstory": "You are a patient story editor who keeps outlines short and concrete.",
  "llm": {
    "model": "ollama/llama3.2",
    "base_url": "http://localhost:11434"
  },
  "settings": {
    "verbose": true
  }
}
```

Leave `main.py` / crew construction untouched (use whatever `crewai create crew` scaffolds).

## Arm B — Python-side LLM injection

Leave `agents/outliner.jsonc` **without** an `llm` key. In the crew construction file, inject the object:

```python
import os
from crewai import LLM, Agent, Crew, Task

llm = LLM(
    model="ollama/" + os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

# Hypothesis: pass llm= to Agent() after loading JSONC config
# Exact API signature unconfirmed; check CrewAI LLMs page before running
outliner = Agent.from_config("agents/outliner.jsonc", llm=llm)
```

`Agent.from_config` and `llm=` kwarg are **hypotheses only** — confirm against the LLMs page at commit 73f48320 before running.

## What to record

1. Full terminal output of `crewai run` for each arm (stdout + stderr)
2. Whether `output/outline.md` was created and its full contents
3. Any error messages verbatim — especially "unknown field" or "llm not found" patterns
4. CrewAI version (`uv tool list`) and Python version
5. Ollama model name actually used

## Failure modes to watch

- **Arm A silently ignores the `llm` key:** output file created but Ollama never called (check Ollama server logs)
- **Arm B `from_config` doesn't exist:** find the real constructor name in source before concluding wiring is impossible
- **Both arms call a default model:** environment variable `OPENAI_API_KEY` may be leaking a fallback

## Why this is the most informative small test

The article's worked example is unusable until this gap is closed — every practitioner hitting it wastes time guessing. One controlled two-arm run (same premise, same model, same machine) answers the question permanently and cheaply.