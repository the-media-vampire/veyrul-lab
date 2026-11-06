#!/usr/bin/env bash
# Smoke test for check_log.py against the three known exit codes.
# Requires Python 3 (tested on 3.13 per source article).
# Run: bash smoke_test.sh
# Each case prints PASS or FAIL and what check_log.py reported.

set -euo pipefail
PY=${PYTHON:-python3}
FAILS=0

run_case() {
  local desc="$1" plan="$2" log="$3" bpm="$4" want="$5"
  set +e
  out=$("$PY" check_log.py "$plan" "$log" "$bpm" 2>&1)
  code=$?
  set -e
  if [ "$code" -eq "$want" ]; then
    echo "PASS  [$desc] exit=$code"
  else
    echo "FAIL  [$desc] expected exit=$want got exit=$code"
    echo "      output: $out"
    FAILS=$((FAILS + 1))
  fi
}

# Case 1: matching log -> exit 0
run_case "pass log"   plan.csv observed_pass.csv 92 0

# Case 2: faulty log -> exit 1
run_case "fail log"   plan.csv observed_fail.csv 92 1

# Case 3: bad BPM -> exit 2 (INPUT ERROR)
run_case "bad bpm"    plan.csv observed_pass.csv 0  2

echo ""
if [ "$FAILS" -eq 0 ]; then
  echo "All smoke tests PASSED."
else
  echo "$FAILS smoke test(s) FAILED."
  exit 1
fi