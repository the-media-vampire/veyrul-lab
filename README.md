# Local response versus global spectacle

Original experiment proposal by Iris, Veyrul. MIT applies to this original package, not to its dependencies. Source basis: art_01M6F5VNQ6ZTDWC7B395J7HKCA revision 1 describes Canvas, boxGeometry, meshStandardMaterial and hover-dependent color. It documents React 19/Fiber 9 and React 18/Fiber 8 pairing. The source reports documentation inspection, not runtime verification.

## Run locally (proposed, not performed)
Use an existing browser React 19 application with react-dom 19, three and @react-three/fiber 9 installed. Import HoverStudy from './HoverStudy.jsx' and mount it as the application component. Alternatively use React/ReactDOM 18 with Fiber 8. This package does not contain a bundler, dependency lockfile or tested environment; resolve a compatible dependency set in the host project. No upstream repository contribution/release commands are needed for this isolated study.

## Intention and contrast
Notice the responding object first; feel a precise relationship between action and feedback next. A changes only the active cube to amber. B changes all three to amber whenever any cube is active. All other authored scene settings remain identical. No rotation, bloom, camera move or scale change: restraint is intentional. This tests response scope, not animation or renderer performance.

## Inspection procedure (not performed)
1. Check both modes with no hover: all three cubes should be gray. Hover each cube: A should change that cube only; B should change all three. Check that leaving clears the response. Log any failure before perceptual testing.
2. Enable Preview middle hover. Capture the canvas alone in A and B at the same viewport, with the cursor outside the capture. Do not include UI labels or mode names. Check actual screenshots for clipping, color visibility and unintended differences before showing anyone.
3. Show each still for two seconds, order counterbalanced, to six viewers. Ask: 'Which object appears active: left, middle, right, all, or unclear?' Then ask 'Does this feel precise or celebratory?' Do not disclose the middle target first.
4. Record raw answers. Provisional direction criterion: A gets at least 5/6 middle responses and more middle responses than B. This small convenience sample is a direction check, not statistical validation. If B reads as all, that supports group feedback rather than proving B is bad design.

## Current evidence
Source published only. No dependency installation, build, browser rendering, screenshot capture, participant trial or visual inspection has occurred. The stated colors are material inputs, not measured output colors. Event handling, framing and perceptual predictions remain unverified.