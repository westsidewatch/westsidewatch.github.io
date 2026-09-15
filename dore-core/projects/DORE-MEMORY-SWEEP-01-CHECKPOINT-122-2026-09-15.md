# DORÉ Memory Sweep 01 — Checkpoint 122

Date: 2026-09-15
Status: BOUNDED PASS / SWEEP CONTINUES

## Evidence family reviewed

- Checkpoint 121 unresolved chronology for `.dore-upload/lam03-hq/` and `static/one/studio/lamentations-03-dore-studio-v1.avif`;
- commit history around 2026-08-19/20 for `Lamentations 3`;
- commit `f356b1d2d982c8791090b7eab33c3a7e41586ba9` (`stage(dore): wire verified Lamentations 3 AVIF cover`);
- merge commit `78da6172f6df2335ef3e497c959c7e200cd63eca` / PR #188 (`Hydrate Lamentations 3 Doré cover from verified staged binary`);
- commit `52b65109398a2c12a456893ac3921790313173a0` (`test(dore): publish Lamentations 3 verified static asset pack`).

## Reconciliation

1. The historical chronology left open by Checkpoint 121 is now materially resolved: the 92,695-byte AVIF payload was verified and deliberately used, but the evidence found does **not** show the intended canonical binary target being committed as `static/one/studio/lamentations-03-dore-studio-v1.avif`.
2. Commit `f356b1d...` updated the staged manifest so `static/one/one-cover-policy.js` was intended to move from the older WebP URL to the AVIF target; this is staging/wiring intent, not proof that the binary target itself existed in Git.
3. PR #188 instead introduced `static/one/studio-binary-runtime.js`, explicitly documenting a workaround for a repository connector that could not persist binary files directly. The runtime reconstructed the verified AVIF in-browser from 13 base64 chunks and exposed it as a Blob URL for Lamentations 3. This is positive evidence that the binary payload was usable while canonical binary persistence remained unavailable.
4. Commit `52b6510...` then copied the same verified manifest/chunks into a same-origin `static/one/studio-packs/lam03/` pack. This is another transport/runtime packaging form, not the canonical AVIF target itself.
5. Current `main` no longer contains the target AVIF or references to the historical `025-003` identifier found by Checkpoint 121. Therefore the historical completion claim should be bounded to **verified payload + runtime hydration/packaging**, not canonical binary persistence.
6. The old `.dore-upload/lam03-hq/`, `studio-binary-runtime.js` pattern and same-origin chunk-pack strategy are superseded historical transport techniques. They must not be reactivated as current asset architecture merely because their residue remains in history.
7. The Lamentations 3 visual milestone itself did reach a meaningful historical component completion: an approved/verified Doré Studio cover payload was wired and served through workaround machinery. That completion is distinct from, and weaker than, durable canonical asset persistence.

## Classification

- Lamentations 3 Doré Studio verified visual payload: `COMPLETED_COMPONENT / HISTORICAL`.
- Canonical persistence of `static/one/studio/lamentations-03-dore-studio-v1.avif`: `NOT_EVIDENCED` in the reviewed history; do not claim it completed.
- `.dore-upload/lam03-hq/` chunk staging: `SUPERSEDED / HISTORICAL_PROVENANCE`.
- `static/one/studio-binary-runtime.js` chunk-to-Blob hydration workaround: `SUPERSEDED / HISTORICAL_PROVENANCE` as an architectural pattern.
- `static/one/studio-packs/lam03/` same-origin base64 pack: `SUPERSEDED / HISTORICAL_PROVENANCE` as a canonical-asset substitute.

## Canonical-register implication

The Master Work Register's current VIS-GRAMMAR direction remains correct and should not be altered by this history: current work requires purpose-built provenance-bearing assets and rendered/human-accepted proof. Historical Lamentations runtime hydration is useful provenance, not a reason to revive chunked binary delivery. This checkpoint closes the specific `UNKNOWN_NEEDS_EVIDENCE` chronology recorded by Checkpoint 121 and is durable input for the next canonical-register frontier reconciliation.

## Smallest future evidence

Inspect the later removal/supersession commits for `studio-binary-runtime.js` and `static/one/studio-packs/lam03/` only if needed to establish exact retirement dates. The completion/transport classification above no longer depends on that date evidence.

## P01 isolation

No P01 subtitle state, runtime, deployment, ordering, blocker, audio/transcription dependency or action was modified. The existing P01 `ENVIRONMENT_BLOCKED` condition remains unchanged.

Sweep 01 remains `ACTIVE_PARALLEL`; this bounded pass resolves Checkpoint 121's Lamentations persistence chronology but does not justify `VERIFIED_COMPLETE`.