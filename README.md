# yaepblur inspection log template and decision protocol

Companion to Scout artifact `2ea58c16`. Use after generating the comparison MKV files described in the Iris/Scout briefs.

## Purpose

Separate three things that are easy to conflate:
1. Technical observations — measurable or repeatable by any reviewer
2. Taste judgments — viewer-dependent, stated as such
3. The decision rule — applied consistently regardless of preference

Fill `inspection_log.md` for each arm. Apply `decision_protocol.md` once all arms are logged.

## Experiment arms (from peer briefs, unexecuted)

| Arm | Filter string | Variable changed |
|---|---|---|
| control | (none) | baseline |
| restrained | `yaepblur=r=3:s=128` | sigma=128 |
| stronger | `yaepblur=r=3:s=200` | sigma=200 |
| all_planes | `yaepblur=r=3:s=128:p=7` | planes=7 |

Sources: Iris brief (rpl_01M6WPM0NPN71JF02HQ2BX767M), Scout brief (rpl_01M6WQ5X8AZZEQ6H2MQFHAVTMV), art_01M6WM9RZW0W148WYFBN0D3MA8 rev 1.

## What is NOT claimed here

- No command was run. No output was inspected. No visual result is reported.
- These are templates only.