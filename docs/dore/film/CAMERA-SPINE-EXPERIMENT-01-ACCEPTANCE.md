# DORÉ FILM — Camera Spine Experiment 01 Acceptance Gate

Status: **OBJECTIVE ENGINEERING PASS / VISUAL DIRECTOR REVIEW REQUIRED**  
Experiment: DF-CAM-EXP-01  
Passage: Abraham → Isaac → Jacob

## What this experiment is testing

This experiment does not test Doré artwork quality. It tests whether the camera path itself already has cinema before the canvases are laid down.

> 先有路，再有畫。

The camera is not a 2D storyboard line. The Camera Spine is spatial production data: position, look target, lens, speed, dwell, grammar, action, narrative beat and time bridge.

## Required pass conditions before Doré canvases are added

1. One camera traverses P001 → P020 without a conventional cut.
2. The path is visibly spatial rather than behaving like a flat diagram.
3. Authored `speed` and `dwell` values produce perceptibly different motion rhythm; they must not remain metadata only.
4. `ABRAHAM_TO_ISAAC` and `ISAAC_TO_JACOB` can be felt as generational/time handoffs without a cut.
5. Tarr-derived sections can carry embodied following/walking.
6. Angelopoulos-derived sections can let history/time change while camera consciousness continues.
7. Antonioni-derived sections can allow the person to stop/disappear while the world and camera continue narrating.
8. Camera motion is motivated by narrative attention, not by demonstrating technique.
9. No Doré image, golden Light, miracle animation or visual polish may be used to conceal a weak Camera Spine during this gate.
10. The same canonical JSON must be able to drive both web previs and Blender previs. Blender and Three.js are views of the data, not the database.

## Objective engineering state — PASS

- Canonical experiment data: `camera-spine-experiment-01.json`
- Web motion lab: `camera-spine-experiment-01.html`
- Public motion lab source: `static/dore/film/camera-motion-lab-01.html`
- Direct GitHub Pages publication: `gh-pages:dore/film/camera-motion-lab-01.html`
- Blender importer: `tools/import-camera-spine.py`
- Timing solver: `tools/camera-spine-timeline.js`
- Parity checker: `tools/camera-spine-parity-check.py`
- CI gate: `.github/workflows/dore-film-camera-spine-parity.yml`
- P001–P020: present
- One camera / zero conventional cuts: enforced
- Camera / Top / Split views: present
- Scrub + Reset: present
- Authored speed/dwell: active in Web Motion Lab
- Timing duration: 52.00s
- Dwell budget: 30.20s
- Travel budget: 21.80s
- `ABRAHAM_TO_ISAAC` arrival: ~9.921s at P006
- `ISAAC_TO_JACOB` arrival: ~30.706s at P014
- GitHub Actions parity run #1: PASS
- Public-page raw-ES-module risk: removed; timing solver is inlined in the public page
- Temporary gh-pages HTML loader: removed; the complete Motion Lab now lives directly on gh-pages
- Doré canvases: intentionally not added

## What is NOT being claimed

- No claim that Blender visual output has been rendered and visually matched in this environment; Blender runtime is not available here.
- No claim that the current P001–P020 rhythm is artistically final.
- No claim that the naked Camera Spine has passed director-level visual judgment until it is watched as motion.

## Remaining acceptance — one director review, not another engineering sub-gate

The engineering work that can be objectively validated without Doré artwork is now assembled. The remaining decision is visual and should be made by watching the naked Camera Spine as a continuous 52-second piece.

Review only these questions:

- Does the line itself feel spatial and cinematic?
- Do the two time bridges feel like generations changing without a cut?
- Does the alternation between follow / empty-world / still-space have rhythm rather than mechanical node traversal?
- Are there any obvious points where the camera feels dead, rushed, or technically self-conscious?

If the answer is broadly yes, do **not** keep polishing the naked skeleton indefinitely. Freeze Camera Spine Experiment 01 as the first accepted route and move to inverse placement of the first small set of canonical Doré canvases.

If the answer is no, revise only the specific weak interval(s); do not restart the entire path.

## Next production action after visual acceptance

`Approved Camera Spine → first canonical Doré canvas placement → Canonical Frame Moment → camera enters/leaves canvas without breaking the one-camera path`

The first canvas pass remains deliberately small. Its purpose is to prove that the world can be laid onto the already-approved camera route — **先定鏡頭，再看世界。**
