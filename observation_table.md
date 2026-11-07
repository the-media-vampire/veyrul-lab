# Observation table

Fill in after each arm of the experiment. Source: art_01M6W0HBATRWPKZ37KQXAYMSY5 r1.

| Check | Expected | Observed exit / output | Repair applied | Result after repair |
|-------|----------|------------------------|---------------|---------------------|
| Python version | 3.10–3.13 | | | |
| uv present | version string | | | |
| crewai CLI | version string | | | |
| litellm extra | Name: litellm | | | |
| Ollama reachable | JSON models list | | | |
| Target model found | name match | | | |
| Project files exist | agents/ + crew.jsonc | | | |
| inputs block shape (Arm A: included) | crewai run uses defaults, no prompt | | | |
| inputs block shape (Arm B: omitted) | crewai run prompts for genre + premise | | | |
| output/outline.md created | file present, three beats | | | |

## Notes
- Run `preflight.sh` before `crewai run` and paste the log path here.
- Record crewai version (`uv tool list`) and Ollama model tag at time of run.
- For the LLM-attachment arms, see Scout's artifact 4f27bad4-8715-449e-9571-75a111e626b1.