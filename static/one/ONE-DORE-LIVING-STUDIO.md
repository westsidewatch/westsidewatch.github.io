# ONE — Doré Living Studio

Status: **LIVING / EVOLVING / REQUIRED RESEARCH MEMORY**

This is not a static image folder. It is the accumulating visual, biblical and editorial intelligence behind ONE Studio's Doré continuation work.

## Mandatory reading order

Before every ONE Studio / Doré-continuation production cycle, Doré AI must read:

1. `ONE-PRODUCTION-ROADMAP-TEMP.md` — current production truth and next task;
2. `ONE-DORE-LEARNING-CURVE.md` — how to study, expand the source corpus, synchronize progress, and harvest learning;
3. this `ONE-DORE-LIVING-STUDIO.md` — accumulated evolving intelligence;
4. `ONE-DORE-VISUAL-GRAMMAR.md` — locked minimum generation/review constraints.

The Learning Curve is permanent learning architecture. The temporary roadmap is deleted after production is complete.

## Temporary production memory — mandatory while backlog remains

While `ONE-PRODUCTION-ROADMAP-TEMP.md` exists, it is the Studio's temporary execution memory. Before every ONE Studio / Doré-continuation production cycle, read it together with the Learning Curve, this Living Studio and `ONE-DORE-VISUAL-GRAMMAR.md`, then take the first unchecked task that is ready.

The ledger is the normal fast path for production progress. Doré AI must not repeatedly rescan all 66 books merely to rediscover which approved illustration candidates are finished. It should trust ledger entries that are already `DONE`, inspect the active/changed chapter, and use the ledger's exact-key reconciliation protocol. The canonical candidate source is the current first-chapter list produced by the cover-mode audit.

But synchronization is not merely bookkeeping. At book, wave, and final-canon reconciliation gates, Doré AI must also perform the learning harvest defined in `ONE-DORE-LEARNING-CURVE.md`: revisit canonical Doré originals, review the completed visual sequence, identify stable grammar, detect Studio drift, and persist reusable discoveries into this Living Studio or the Visual Grammar. Progress checking and corpus learning therefore reinforce each other without requiring a full 1,189-chapter scan after every plate.

### Doré AI progress recognition

Doré AI must recognize that an image moves through distinct production states:

`TODO → GENERATED → APPROVED → PERSISTED → ASSIGNED → DEPLOYED → LIVE_VERIFIED/DONE`

Only `LIVE_VERIFIED` is complete. The AI must not infer completion from any earlier state, from a successful generation, from an editor saying the artwork looks right, from a local registry entry, or from a commit existing. Completion requires the exact final asset/revision to be visibly resolved by the intended public ONE chapter after deployment.

Every generated chapter uses a stable zero-padded `BOOK-CHAPTER` key such as `025-003`. For a completed chapter, Doré AI must be able to identify the compact proof record in the ledger: chapter key, `DONE`, stable asset ID, revision, assignment source, deploy commit/PR, live route, and verification date. If the live route or registry no longer matches that proof, the AI must downgrade/reconcile the entry rather than silently trusting an obsolete checkmark.

After each newly verified chapter, update the ledger counters and proof row immediately. At the end of a book, reconcile that book only. At the end of a production wave, reconcile global totals only. This keeps ledger progress and live-site progress equivalent without a full-canon scan after every plate.

The temporary ledger is research/production memory only. It must never be imported, fetched or referenced by the ONE reader runtime, `index.html`, loaders, scripts, styles, service workers, `ONE_DATA`, `ONE_COVER_POLICY` or Canon Index. When its completion/deletion gate is reached, delete it; this Living Studio remains.

## Product vision

The long-term goal is not merely to fill chapters that Gustave Doré did not illustrate. The Studio must learn how Doré translated Scripture into images: what textual moment he selected, what he omitted, where he placed the viewer, how theology became scale/light/gesture/space, and how one plate relates to the biblical passage around it.

The mature Studio is intended to support an independent Westside Watch / ONE image product: Scripture-led plates that can stand on their own outside the chapter reader while remaining traceable to a specific passage and interpretive rationale.

Quality aspiration: when a new Studio plate is placed among the canonical Doré Bible plates, the visual and narrative continuity should be strong enough to evoke the impression of a plausible lost plate from the same biblical picture-world. Provenance must nevertheless always remain truthful: Studio works are never attributed to Doré.

## 1. The Studio learns two grammars at once

Every study cycle must learn:

1. **Doré pictorial grammar** — composition, figure, animal, gesture, value, light, line, landscape, architecture, crowd, scale and visual rhythm.
2. **Scripture-to-image grammar** — how a biblical text becomes one selected visual moment.

Neither is sufficient alone. A visually Doré-like image that misunderstands the passage fails. A biblically accurate scene rendered with generic fantasy or generic engraving language also fails.

## 2. Scripture-to-image study record

For every canonical Doré plate studied, record where possible:

- biblical book, chapter and verse/range;
- narrative unit around that verse;
- theological center of the passage;
- exact instant Doré chose to depict;
- what occurs immediately before and after the chosen instant;
- principal figure/action;
- secondary narrative evidence included in the frame;
- important textual details Doré deliberately omitted;
- viewer position and viewing distance;
- whether the plate uses intimate detail, medium narrative staging or monumental spectacle;
- how gesture expresses the text;
- how light/dark expresses theological hierarchy;
- how landscape/architecture participates in interpretation;
- whether the image is literal, compressed, typological, symbolic or a mixture;
- what makes this choice recognizably Doré rather than merely an illustration of the same verse.

This record becomes reusable precedent for future passages with related visual problems.

## 3. Do not assume spectacle

Doré's biblical storytelling includes both vast scenes and small human moments. Generation must not default to epic scale.

Before composition, ask:

- Where would Doré place the viewer?
- Which second of the biblical event would he freeze?
- What should be noticed first, second and only later?
- Is the passage best served by one hand, one face, one kneeling body, a doorway, a small group, a procession, a landscape, or a cosmic scene?
- Which textual details should remain outside the frame?

Background people are never filler. Every group must have a narrative function: witnessing, recoiling, mourning, worshipping, fleeing, arguing, waiting, following, opposing, or establishing scale.

## 4. Visual ancestry

Before inventing something Doré did not directly illustrate, locate its **visual ancestors** in his actual corpus. Follow the corpus tiers and anti-contamination rules in `ONE-DORE-LEARNING-CURVE.md`: Bible originals first; non-Bible Doré works may solve visual problems but never interpret Scripture in place of the Bible corpus.

Examples:

- Revelation sea beast / earth beast: begin with Doré's own Revelation dragon, then Danielic monsters, predatory animals, crowd reaction and landscape grammar. Do not begin with modern fantasy creature design.
- White-horse rider: begin with Doré horses, cavalry, riders, battle compression and Revelation's Pale Horse.
- Heavenly throne: begin with Doré celestial hierarchy, enthroned figures, angels, worship crowds and supernatural light.
- Quiet church scene: begin with Doré prophets, apostles, interiors, doorways, lamps, kneeling and intimate encounters rather than forcing a cosmic tableau.

A generated subject should feel genetically related to Doré's existing picture-world.

## 5. Learning loop

Every generation cycle adds knowledge back into the Studio.

### Before generation
- read `ONE-PRODUCTION-ROADMAP-TEMP.md` when it exists and take the first ready unchecked production task;
- read `ONE-DORE-LEARNING-CURVE.md` and apply its source hierarchy;
- read the current Living Studio;
- read the current Doré Visual Grammar;
- study the Scripture in context;
- select 3–8 canonical Doré references first, then add non-Bible Doré visual ancestors only when a specific visual problem remains unresolved;
- write the reference ancestry, transfer boundary and scene-choice rationale.

### After generation
Record:
- what succeeded;
- what looked generic rather than Doré;
- anatomy/gesture/animal problems;
- composition problems;
- Scripture interpretation problems;
- line/light/value problems;
- what a next revision should change;
- any new general principle worth promoting into the Visual Grammar;
- after FINAL persistence, assignment, deployment and live verification, update `ONE-PRODUCTION-ROADMAP-TEMP.md` before starting the next production item;
- at book/wave reconciliation, perform the Learning Curve's required learning harvest.

Failures are retained as learning, not silently discarded.

### Every plate must advance Doré AI — mandatory

Every generation cycle is a training cycle, not merely an image-delivery task. A cycle is incomplete if it produces an image but leaves Doré AI with no durable, reusable improvement.

Before a plate may be called FINAL, the cycle must preserve all of the following:

1. a visual-ancestry record naming the authenticated Doré works studied and the specific compositional, anatomical, value, line or spatial knowledge borrowed from each;
2. a stated training objective identifying what Doré AI is intended to learn in this chapter;
3. a comparison of generated revisions against the selected originals, including what remained generic, modern or recognizably AI-generated;
4. retained failure evidence and a concrete explanation of what the next revision changed;
5. at least one reusable observation written back into Living Studio memory, or an explicit statement that the experiment confirmed an existing rule without creating a new one;
6. promotion into `ONE-DORE-VISUAL-GRAMMAR.md` only after the same principle proves stable across more than one task or corpus comparison.

The required deliverable is therefore:

`final plate + visual ancestry + revision/failure record + durable learning harvest + deployment proof`

Missing any component means the production cycle is not complete. A visually attractive image is not evidence of learning.

The failed workflow “generate a modern cinematic colour image, then convert it into monochrome engraving texture” is a permanent negative example. It changes surface treatment without learning Doré's Scripture selection, pictorial grammar or hand-built value structure and must not be used as a production method.

### Durable memory, not conversation memory

Doré AI must never claim that model weights or a chat session guarantee memory. Continuity is guaranteed operationally by repository-backed research memory.

- useful source studies and transfer boundaries belong in the Learning Curve research record;
- task-specific successes, failures and revisions belong in this Living Studio;
- repeatedly validated minimum rules belong in the locked Visual Grammar;
- production state and live proof belong in the temporary roadmap while it exists;
- the mandatory reading order must be completed before every generation cycle, including after a new chat, model change or long interruption.

Knowledge that exists only in a prompt, chat transcript or an uncommitted local note is not learned Studio memory.

### FINAL means persisted — mandatory
When editorial review explicitly approves a generated plate as **FINAL**, approval must not remain only in conversation history. In the same production cycle, persist the actual image file and its identity:

1. preserve the approved binary image as a stable ONE Studio / Doré-generated asset;
2. assign a stable Studio asset ID and revision;
3. register the asset in the separate ONE Studio asset library — never in the canonical Doré Original Library;
4. map it to its book/chapter through the shared registry/resolver;
5. record Scripture, title, provenance, palette, approval state and relevant learning/revision notes;
6. commit the asset and registry change together whenever technically possible.

A plate is not operationally `DONE` until the approved binary and registry mapping are persistent, the deployment containing them is live, and the public chapter has been checked to render that exact asset/revision. Do not require the editor to re-upload or rediscover an already-approved plate merely because later conversation context has moved on; search existing conversation/library assets first.

## 6. Growing knowledge domains

The Living Studio should progressively accumulate specialist notes for:

- Scripture scene selection;
- biblical narrative sequencing;
- prophetic and apocalyptic symbolism;
- Christ / prophets / apostles / kings / ordinary people;
- face, hand and gesture;
- drapery;
- horses and riders;
- sheep, lions, serpents, dragons and invented biblical beasts;
- angels and celestial beings;
- intimate scenes;
- small groups;
- crowds and armies;
- battle;
- death, grief and judgment;
- worship;
- wilderness, mountain, sea and storm;
- ancient city and architecture;
- heaven / paradise / New Jerusalem;
- supernatural light and darkness;
- engraving line systems;
- cover-safe and 5:8 plate composition.

These domains are not final chapters. They are living notebooks and may split or merge as the Studio learns.

## 7. Independent image-product readiness

A Studio plate should eventually carry enough structured knowledge to function outside ONE chapter pages. Its asset record should be able to expose:

- stable asset ID and revision;
- Scripture reference;
- short plate title;
- biblical scene summary;
- visual ancestry references;
- generation/revision history;
- monochrome or approved colour status;
- review status;
- provenance: `ONE Studio`;
- rights/usage metadata when required;
- links back to the ONE chapter and related plates.

This permits future products such as a Scripture plate gallery, print series, devotional image cards, exhibition/editorial layouts, or a standalone Doré-continuation collection without contaminating the canonical Doré Original Library.

## 8. Lost Plate Test

Before ACTIVE status, ask two separate questions:

### Biblical test
Would a careful reader of the passage understand why this exact moment, gesture, light and spatial relationship were chosen?

### Doré continuity test
If the attribution were hidden and the plate were inserted among Doré's Bible illustrations, would its scene intelligence as well as its drawing language plausibly belong to the same visual world?

Texture alone cannot pass this test.

## 9. Provenance boundary

The aspiration may be a "lost Doré plate" visual experience, but metadata must never falsely claim that a generated image was drawn, engraved, published or discovered as an original work by Gustave Doré.

Canonical Doré originals and ONE Studio works remain separate libraries permanently.

## 10. Living status

This document is intentionally not `LOCKED` in its artistic conclusions. It must improve as more Doré plates are studied and more Studio images are reviewed.

Stable architectural rules belong in the master policy. Growing artistic intelligence belongs here. The method for acquiring and validating that intelligence belongs in `ONE-DORE-LEARNING-CURVE.md`.

The Studio is expected to become stricter, more specific and more Doré-literate over time.
