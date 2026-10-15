# Engraved 3D Surfaces — Phase 3 Research

Status: RESEARCH ONLY / NOT INTEGRATED
Date: 2026-10-15

## Verified upstream: ai-sci-computing/hatching
Repository: https://github.com/ai-sci-computing/hatching
README: https://raw.githubusercontent.com/ai-sci-computing/hatching/main/README.md
- C++20/OpenGL 4.1; Emscripten/WebAssembly + WebGL2 web build.
- Loads OBJ/OFF triangle meshes; interactive orbit camera, lighting and hatching parameters.
- Curvature-aligned globally optimal 2-direction fields; continuous stripe patterns; NPR hatching shader and silhouettes.
- Implements research from Knöppel et al., *Globally Optimal Direction Fields* (2013) and *Stripe Patterns on Surfaces* (2015).
- 42 tests claimed in README; no local build or runtime verification performed here.
- README license: free for personal, academic and research use; commercial use requires written permission. This is NOT an unrestricted OSI open-source license. Do not copy it into production without permission.

## Important distinction
Camera orbit around a static model is already supported. Character animation, skeletal deformation, frame-coherent hatching, export pipeline and cinematic production are NOT established by this repository alone. Recomputing direction fields each frame may be costly; evaluate UV/mesh-attached stripe stability.

## Other relevant leads
- https://github.com/mightyhorst/threejs-hand-sketching — investigate real-time cross-hatching and license.
- https://github.com/CreativeInquiry/ApparentRidges — view-dependent ridge extraction / silhouette research.
- https://github.com/ai-sci-computing/hatching — reference implementation, license restriction above.

## Phase 3 gate
Only after Phase 2 is accepted. First validate a simple rotating object with stable engraved strokes, then animated deformation. Keep rendering system modular and check reuse rights.
