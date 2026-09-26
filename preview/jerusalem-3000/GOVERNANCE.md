# Jerusalem 3000 — Engineering Governance

These rules exist because repeated prompt-only constraints proved insufficient.

## 1. Source authority gate

The spatial implementation authority is the adopted `threejs-architecture-effects` architecture: real Three.js scene, `PerspectiveCamera`, `WebGLRenderer`, `OrbitControls`, and shared reversible construction progress. CSS pseudo-3D is not an acceptable substitute.

## 2. Evidence authority gate

Historical geometry must be generated from project evidence ledgers. Objects whose registration is withheld or unresolved must not be invented merely to make the scene look complete. Evidence classes remain explicit: observed, reconstructed, inferred, disputed.

## 3. Completion gate

A PR, commit, merge, successful Pages deployment, or runtime boot is not by itself completion of an engineering step.

Step 1 may be called COMPLETE only when `STEP-1-COMPLETION.json` exists and records all of these as true:

- historical geometry runtime is active;
- placeholder geometry is removed;
- evidence/withheld policy is validated;
- timeline/lifecycle behavior is validated;
- Three.js runtime is validated;
- production deployment is validated;
- production visual behavior is validated.

Until then, status is IN PROGRESS. Intermediate events must not be represented as completion.

## 4. Merge discipline

Jerusalem 3000 changes should be isolated from unrelated project changes. Architecture/evidence governance checks must pass before a Jerusalem PR is treated as eligible for production. A failed unrelated repository workflow is not permission to alter unrelated authority data.

## 5. Human authority

Explicit human project constraints override convenience optimizations. If an implementation conflicts with a recorded project constraint, stop that implementation path rather than silently substituting a different architecture.
