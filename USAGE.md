# Usage

## Prerequisites
Ollama installed. Base model available locally (`ollama list`).
See Ollama install docs for setup — not covered here.

## Steps

```bash
# 1. Edit Modelfile: replace llama3.2 with a model you have.
# 2. Build the custom model.
ollama create peer-reviewer -f ./Modelfile

# 3. Run it.
ollama run peer-reviewer

# 4. Inspect what was built.
ollama show --modelfile peer-reviewer
```

## Tradeoff table (from art_01M6TR98ET2K0WFZTVBRCYGFV8 r1)

| Symptom | Setting to change |
|---|---|
| Cuts off mid-reply | Raise num_ctx or num_predict |
| Never stops | Lower num_predict or add stop sequence |
| Repeats phrases | Raise repeat_penalty above 1.0 |
| Ignores system message | Base template may lack system slot; inspect with ollama show |
| Too random / too flat | Adjust temperature first, then top_p / top_k |

## Evidence status
Syntax is source-documented (Modelfile reference, commit 5e983d4f).
This Modelfile has not been run. Setting values are illustrative choices,
not tuned recommendations.

## Attribution
See artifact attribution. Adapts the instruction set documented in
art_01M6TR98ET2K0WFZTVBRCYGFV8 r1 (Veyrul import agent, 2026-11-07).