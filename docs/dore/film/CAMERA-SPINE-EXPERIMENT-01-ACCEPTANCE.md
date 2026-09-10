# DORÉ FILM — Camera Spine Experiment 01 Acceptance Gate

Status: ACTIVE ENGINEERING GATE  
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

## Current engineering state

- Canonical experiment data: `camera-spine-experiment-01.json`
- Web motion lab: `camera-spine-experiment-01.html`
- Public motion lab source: `static/dore/film/camera-motion-lab-01.html`
- Blender importer: `tools/import-camera-spine.py`
- P001–P020: present
- One continuous spline: present
- Camera / Top / Split views: present in web lab
- Scrub: present
- Time bridges: present
- Blender import path: implemented
- Web authored speed/dwell timing: NEXT PATCH / not yet accepted
- Doré canvases: intentionally not added

## Next engineering action

Activate authored speed/dwell in the web runtime and validate its rhythm against the Blender import. Only after the naked Camera Spine passes this gate may the first small set of canonical Doré canvases be inverse-placed onto the approved camera path.
