# ONE Visual Manifest — Hard Gates

The visual manifest is the single source of truth for chapter cover and illustration assets.

## State model

`CANDIDATE → VERIFIED_SOURCE → ASSIGNED → CALLABLE → LOCKED_CALLABLE`

A chapter is not counted as locked merely because an audit or conversation says it is covered.

## LOCKED_CALLABLE requirements

A chapter may enter `LOCKED_CALLABLE` only when all of the following exist:

1. Unique `chapterId`.
2. Real cover `assetId` and repository asset path.
3. At least one real illustration asset and repository asset path.
4. Asset orientation.
5. Doré title and original biblical provenance for every Doré asset.
6. Reuse class identifying whether the allocation is original, event reuse, textual reuse, or image-meaning reuse.
7. A fixed chapter theme verse.
8. Cover layout fixed to `portrait-book-cover-template`.
9. Illustration layout derived from the original image orientation:
   - landscape → `landscape-image-with-verse`
   - portrait → `portrait-image-with-side-verse`
   - multiple plates → `multi-image-editorial-spread`
10. Every referenced asset actually exists.

## Failure behavior

If any required field or asset is missing, the chapter is `UNRESOLVED` and MUST NOT:

- count toward the callable locked total;
- silently select another image;
- generate a replacement image;
- reuse a nearby chapter's asset;
- fall back to a generic cover.

The renderer must expose the unresolved state during development.

## Counting

The authoritative locked/callable count is computed from valid manifest chapter records. A manually typed checkpoint such as 447 is historical audit metadata only and is never authoritative for rendering.

## Mutation

Locked assets are immutable by default. Changing a locked allocation requires an explicit unlock, modification, validation, and relock cycle.

ONE Studio generated artwork follows the same rule: generate once, accept, assign a stable asset ID/path, then lock. It is never regenerated automatically.

## Rendering contract

Chapter pages read visual choices only from `visual-manifest.json`. Rendering code may choose responsive presentation but may not choose or substitute visual content.

## Current migration gate

Historical audit checkpoint: 447 chapters.
Callable manifest checkpoint: derived only from validated manifest records.

Do not begin the Psalms full-production test until the historical locked set has been migrated and validation reports no missing required fields, unresolved assets, or duplicate chapter IDs.
