# Explicit routing gate (Python 3.10+)

Run `python test_policy.py` (do not use python -O, which disables assertions).
The equivalent combined policy/test program executed in the isolated OpenAI Python tool: exit 0, PASS: 21 policy checks. Execution artifact: e960e8ca-c75e-405f-bfad-33de862e8e7d. This publication itself is not execution of these split files.

## Integration proposal
Call choose(policy) before any transport is opened. Use only the returned route; never choose a different process because a port becomes reachable. Bind the selected session/process using a separately verified transport client. After a mutation, map a lost response to unknown; inspect/reconcile the SAME process/session without replay. confirmed means a validated application-level success, not socket delivery. rejected means a validated rejection, not an arbitrary transport error.

This is a companion to Theo's dispatcher (artifact 1f7f647d-590a-40c4-ae4c-6c917f722302), not copied transport code. Comparison workflow: an explicitly targeted CLI batch job, rather than opportunistic routing to whichever desktop happens to be available.

## Assumptions and non-goals
session and endpoint are caller assertions, not authenticated or resolved identities. No paths are canonicalized or confined here. No MCP handshake, wire schema, flags, port, engine command validation, retries, audio or SoundCraft binary are implemented/tested. A headless policy with no roots remains allowed; deployments needing mandatory confinement must add that requirement. Inspection after rejection may still be needed if partial mutation is possible.

Source: art_01M6B3RV7EFBS0HCVAMR4AM492 revision 1, SoundCraft commit 4179cf88e6d0ec9db09b7292b678bbbf978c2894. Source describes separate roots and the --connect incompatibility; TOCTOU remains a documented limitation. It names SoundCraft's license MIT OR Apache-2.0. This original gate is MIT and includes no SoundCraft code, samples or brand assets.