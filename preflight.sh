#!/usr/bin/env bash
# preflight.sh — Pre-flight checks for the one-agent outline crew
# Source: art_01M6W0HBATRWPKZ37KQXAYMSY5 r1 "If it fails" section
# NOT EXECUTED. Placeholders: OLLAMA_MODEL, OLLAMA_URL, PROJECT_DIR.
# Record each line's exit code and stderr in preflight.log.
set -uo pipefail
LOG="preflight_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee "$LOG") 2>&1

echo "=== 1. Python version (need 3.10–3.13) ==="
python --version || python3 --version
# Expected: Python 3.10.x – 3.13.x
# Fail: version outside range → use pyenv or system Python that qualifies

echo "=== 2. uv present ==="
uv --version
# Expected: uv 0.x.x
# Fail: command not found → install uv per https://docs.astral.sh/uv/

echo "=== 3. crewai CLI present ==="
crewai --version || echo "FAIL: run: uv tool install crewai && uv tool update-shell"
# Expected: crewai, version x.x.x
# Fail: not found → install and re-source shell PATH

echo "=== 4. litellm extra installed ==="
uv pip show litellm 2>/dev/null || echo "FAIL: run: uv add 'crewai[litellm]' in project root"
# Expected: Name: litellm with a Version line
# Fail: not found → uv add 'crewai[litellm]'

echo "=== 5. Ollama server reachable ==="
curl -sf "${OLLAMA_URL:-http://localhost:11434}/api/tags" | head -c 200 || \
  echo "FAIL: Ollama not running or wrong URL — start ollama serve"
# Expected: JSON with models list
# Fail: connection refused → start Ollama; wrong port → set OLLAMA_URL

echo "=== 6. Target model present in Ollama ==="
curl -sf "${OLLAMA_URL:-http://localhost:11434}/api/tags" | \
  grep -o '"name":"[^"]*"' | grep "${OLLAMA_MODEL:-llama3}" || \
  echo "FAIL: model not found — run: ollama pull ${OLLAMA_MODEL:-llama3}"
# Expected: "name":"<your model>" line
# Fail: no match → ollama pull <model>

echo "=== 7. Project directory exists ==="
ls "${PROJECT_DIR:-.}"/{agents,crew.jsonc} 2>/dev/null || \
  echo "FAIL: missing agents/ or crew.jsonc — run crewai create crew <name> first"
# Expected: agents/ directory and crew.jsonc listed
# Fail: not found → scaffold project first

echo "=== All checks complete. Review $LOG for any FAIL lines. ==="