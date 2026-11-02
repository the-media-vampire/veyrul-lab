# HoverStudy — Mode C experiment brief

## Source artifacts
- Iris HoverStudy: artifact `8fbe25ea`, commit `470a0a40`
- Library documentation: `art_01M6F5VNQ6ZTDWC7B395J7HKCA` revision 1

## Structural observation (static analysis, executed)
Mode A logic: `selected === i ? accent : rest`
Inactive cubes and pre-hover rest are **visually identical** (#65717c).
The viewer cannot distinguish "no one is hovered" from "someone else is hovered."

Mode B collapses the other way: all cubes turn amber together.
The question "which cube is active?" has no answer.

## What Mode C changes
| State              | Hex       |
|--------------------|-----------|
| REST (no hover)    | `#65717c` |
| ACTIVE (hovered)   | `#ffb14a` |
| DIM (inactive nbr) | `#3a4550` |

Only the hovered cube turns amber; neighbors dim rather than hold rest gray.
Local specificity is preserved; inactivity becomes a distinct semantic state.

## Discriminating test (single variable)
1. A vs C, middle-hover preview, 2-second still, six viewers.
   Question: "What is the resting-but-inactive cube doing?" (nothing / dimming / glowing / unclear)
   Prediction: more "dimming" responses to C.
2. Threshold check: if DIM appears same as REST on-screen, replace #3a4550 with
   #2a343d and retest before adding any other variable.

## Evidence boundary
No build, render or viewer trial has been run. Colors are authored inputs.
Dependency pairing follows art_01M6F5VNQ6ZTDWC7B395J7HKCA rev 1 (React 18/Fiber 8 or React 19/Fiber 9).