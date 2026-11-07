"""Arm B wiring sketch — untested; API surface unconfirmed.

Before running:
  1. Check the CrewAI LLMs page at commit 73f48320 for the real constructor.
  2. Set OLLAMA_MODEL and OLLAMA_URL in .env.
  3. Install: uv add "crewai[litellm]"
"""
import os
from crewai import LLM

# Construct the LLM object — shape confirmed from art_01M6W0HBATRWPKZ37KQXAYMSY5 r1
llm = LLM(
    model="ollama/" + os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

# Hypothesis only — verify Agent constructor kwargs before running:
# from crewai import Agent
# outliner = Agent.from_config("agents/outliner.jsonc", llm=llm)
# OR: outliner = Agent(..., llm=llm)
print("LLM object constructed:", llm)
print("Pass this object to your Agent constructor per the LLMs docs page.")