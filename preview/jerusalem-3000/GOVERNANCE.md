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

## 4. Execution-until-stage-complete directive

When the human gives an instruction such as `不可停留在通報層`, `完成再通報`, `中間不要停`, `繼續工程不用停`, `不要一直通報`, or another instruction with the same clear meaning, it establishes an execution boundary for the current engineering stage.

While that directive is active:

- acknowledgement is not execution and must not terminate the work turn;
- a commit, PR, CI result, merge, deployment trigger, or intermediate diagnosis is not a reporting boundary;
- the agent must continue performing the next available engineering action inside the current stage instead of returning an intermediate status report;
- reporting is permitted only after the stage Definition of Done has been satisfied and verified;
- the only permitted early return is a genuine hard blocker that the agent cannot resolve with its available tools or authority, such as missing human-only authorization, unavailable required source data, or a tool/permission boundary that prevents further execution;
- when a hard blocker occurs, the report must identify the blocker precisely and must not describe the stage as complete.

This directive is semantic, not phrase-specific. Equivalent wording carries the same execution requirement.

For Jerusalem 3000 Step 1, the Definition of Done is the Completion Gate in section 3. Therefore `STEP-1-COMPLETION.json` is the machine-readable release of the reporting gate: until its requirements are genuinely satisfied, intermediate engineering events are not completion reports.

## 5. Merge discipline

Jerusalem 3000 changes should be isolated from unrelated project changes. Architecture/evidence governance checks must pass before a Jerusalem PR is treated as eligible for production. A failed unrelated repository workflow is not permission to alter unrelated authority data.

## 6. Human authority

Explicit human project constraints override convenience optimizations. If an implementation conflicts with a recorded project constraint, stop that implementation path rather than silently substituting a different architecture.
