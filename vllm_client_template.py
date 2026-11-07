"""vLLM chat-completions client template.

Source basis: art_01M6VVM14PS4BVTG89KP9KHPEK r1 (vLLM quickstart at commit c9e4cb2b).
Nothing in this file has been executed; every output is expected, not observed.

USAGE
-----
1. Start the server first (see SETUP below).
2. Set VLLM_BASE_URL in your environment (default: http://localhost:8000).
3. If you started the server with --api-key, set VLLM_API_KEY too.
4. Run: python vllm_client_template.py

SETUP (source-documented, not run here)
----------------------------------------
    uv venv --python 3.12 --seed
    source .venv/bin/activate
    uv pip install vllm --torch-backend=auto   # Linux + CUDA; other hardware: see quickstart tabs
    vllm download-kernels                       # avoids per-startup kernel compilation
    vllm serve Qwen/Qwen2.5-1.5B-Instruct      # add --host / --port to change defaults

DECISION POINTS
---------------
- MODEL_NAME must match the model you passed to `vllm serve`.
- api_key: "EMPTY" works when no --api-key was set on the server.
  If you set one, replace "EMPTY" with the actual key or read it from env.
- generation_config: the server uses the model repo's generation_config.json by default.
  Pass --generation-config vllm to vllm serve to use vLLM sampling defaults instead.
  Source-documented; tradeoff not tested here.
- Offline LLM class (not shown): llm.generate does NOT apply the chat template automatically;
  apply it yourself for instruct models. Source-documented.
"""

import os
from openai import OpenAI

# --- Contributor-supplied values ---
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"  # change to match your served model
SYSTEM_PROMPT = "You are a story editor."
USER_PROMPT = "Suggest three titles for a lighthouse ghost story."

# --- Connection (source-documented defaults) ---
base_url = os.environ.get("VLLM_BASE_URL", "http://localhost:8000") + "/v1"
api_key = os.environ.get("VLLM_API_KEY", "EMPTY")  # placeholder when no key is set

client = OpenAI(api_key=api_key, base_url=base_url)

# --- Request ---
reply = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": USER_PROMPT},
    ],
    # Uncomment to override sampling (server-side flag must also be set):
    # temperature=0.7,
    # max_tokens=256,
)

print(reply.choices[0].message.content)