# Doré UI Skills Exploration R4 — Preference Field, Uncertainty, and Taste Compression

## Objective

Move Doré from design memory to design intelligence without training a heavyweight style model.

The target is not a universal aesthetic score. The target is a compact contextual preference field learned from pairwise design evidence, with explicit uncertainty, contradiction handling, and reversible scope.

## Round 1 — Pairwise taste is a better primitive than absolute taste scores

Aesthetic judgment is usually easier and more reliable as a comparison than as an absolute score: A or B better satisfies this task, on this axis, in this context.

Bradley–Terry / Luce-style models provide a useful abstraction: repeated pairwise wins can be compressed into latent relative strengths while preserving the original comparisons as evidence.

External references:
- https://github.com/lucasmaystre/choix
- https://github.com/mohammadi-hadi/arenakit
- https://github.com/krisyotam/whichisbetter

Doré rule:
- raw comparison ledger remains canonical evidence;
- derived strengths are a cache, never authority;
- never collapse all contexts into one global taste leaderboard;
- tie/uncertain regions must remain visible.

## Round 2 — Context is part of the preference, not metadata after the fact

A design direction can win on a quiet church page and lose on Dawn Library. A dense editorial rhythm can fit Journal and be wrong for prayer or worship surfaces.

Preference key should therefore be conditional on a compact context signature:
- surface family;
- task intent;
- primary design axis;
- viewport class;
- content density/type;
- interaction mode;
- brand-pattern scope.

Doré must not learn `large serif title > small title` globally. It may learn something like `on contemplative editorial entry surfaces, larger serif hierarchy repeatedly wins when copy is short and imagery is dominant`.

## Round 3 — Uncertainty is a first-class output

A ranking without confidence is dangerous. Sparse comparisons, cyclic preferences, contradictory contexts, or near-ties must not be promoted as rules.

Doré preference field returns:
- relative strength;
- evidence count;
- win/loss/tie shape;
- confidence;
- contradiction pressure;
- scope.

Promotion rule:
- local precedent may be used immediately;
- surface-family precedent requires repeated cross-instance evidence;
- brand-pattern precedent requires repeated wins across multiple surfaces and no unresolved contradiction cluster.

## Round 4 — Surprise is more valuable than confirmation

If a new result contradicts a high-confidence precedent, do not silently average it away. Record a surprise event.

Surprise can mean:
1. old rule was overgeneralized;
2. context signature is too coarse;
3. product identity changed;
4. prior evidence was weak or biased;
5. this is a legitimate art-direction exception.

A contradiction should trigger re-segmentation before it triggers a global reversal.

## Round 5 — Taste compression must be lossy in the right direction

Doré should get lighter as it learns.

Raw history can grow, but runtime context should shrink. Repeated, non-contradictory comparisons may be compressed into a small preference summary. The summary is a retrieval hint, not a replacement for evidence.

Runtime pack target:
- at most 3 relevant preference claims;
- at most 2 rejection precedents;
- at most 1 uncertainty warning;
- original evidence refs retained by id, not copied into prompt.

## Round 6 — Active comparison: ask only when the answer matters

A useful preference system should not compare every possible pair. It should spend comparison effort where uncertainty is high and the decision is consequential.

Candidate selection priority:
- close estimated strengths;
- low evidence count;
- high contradiction pressure;
- important promotion decision;
- fresh context with weak precedent coverage.

This produces a design equivalent of active learning while keeping Doré lightweight.

## Engineering direction

New capability substrate: `ui_preference_field.py`.

Responsibilities:
- aggregate pairwise comparison evidence from `ui_taste_memory.py`;
- compute lightweight Bradley–Terry-like relative strengths with no mandatory third-party runtime dependency;
- expose uncertainty and contradiction signals;
- select high-information next comparisons;
- emit bounded runtime preference packs;
- never overwrite canonical comparison/rejection ledgers.

## Non-goals

- no universal aesthetic reward score;
- no hidden style model;
- no auto-promotion to global tokens;
- no preference inference from a single Candidate 1 fix;
- no replacing human/product identity with crowd-average taste;
- no huge context dump.

## R4 acceptance

Doré UI intelligence improves only if it can:
1. predict a likely winner from relevant precedent;
2. say when it is uncertain;
3. detect a context-breaking contradiction;
4. request the next useful comparison instead of arbitrary more data;
5. compress runtime design memory while retaining evidence provenance;
6. allow a new result to override or split an old preference when evidence justifies it.
