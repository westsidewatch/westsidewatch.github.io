# ONE — Doré Native Binary Publisher

Status: **REQUIRED PRODUCTION TOOL / NON-RUNTIME / BATCH-CAPABLE**

This tool exists to solve one specific production problem permanently: an approved Doré Studio image must become a real binary file in the repository without passing through chat text, base64 fragments, browser reconstruction, temporary runtime fetches, or a special Pages workaround.

Tool:

`/scripts/dore/publish-studio-asset.mjs`

## Contract

The publisher operates on a checked-out repository working tree and reads the approved image directly from the filesystem as binary bytes.

Flow:

`approved local/generated image → byte validation → SHA-256 → atomic copy into static/one/studio/ → registry assignment → receipt → normal git commit/PR/deploy → live verification`

The public ONE reader must consume only the final binary asset path. The reader must never know about staging chunks, base64, local file paths, publisher internals or the temporary production ledger.

## Why this is the canonical Doré publishing path

The previous connector experiments exposed a structural problem: moving image bytes through chat/tool text can truncate or double-encode them, and build/runtime reconstruction makes publication dependent on unrelated workflows. That approach does not scale to the remaining production backlog.

This publisher removes that entire class of failure. It uses Node filesystem APIs, so copying a 50 KB image and a 5 MB image is the same operation: binary bytes are copied directly, then re-read and compared by exact byte count and SHA-256 before registry mutation is accepted.

## Single-plate command

Example:

```bash
node scripts/dore/publish-studio-asset.mjs \
  --input /absolute/path/lamentations-03.png \
  --book 25 \
  --chapter 3 \
  --asset-id LAM-03-DORE-STUDIO-001 \
  --title "Lamentations III" \
  --scripture "Lamentations 3" \
  --filename lamentations-03-dore-studio-v2.png \
  --replace
```

`--replace` is required when editorial review has explicitly approved replacement of an existing Studio assignment. Without it, an existing asset ID or chapter assignment is a hard failure.

## Batch mode

For normal production, do not publish one PR per image. Create a JSON manifest containing 10–30 approved jobs and run:

```bash
node scripts/dore/publish-studio-asset.mjs --manifest /absolute/path/dore-wave.json
```

Example manifest:

```json
{
  "jobs": [
    {
      "input": "/work/plates/025-003.png",
      "book": 25,
      "chapter": 3,
      "assetId": "LAM-03-DORE-STUDIO-001",
      "title": "Lamentations III",
      "scripture": "Lamentations 3",
      "filename": "lamentations-03-dore-studio-v2.png",
      "replace": true
    }
  ]
}
```

After the whole wave succeeds, create one git commit and one PR containing all binary files, registry edits and receipts.

## Validation gates

The publisher fails closed when any of these conditions is true:

- input file does not exist;
- file is not PNG, JPEG, WebP or AVIF by binary signature;
- file is suspiciously tiny for a Studio master (currently under 25 KB);
- copied bytes differ from source byte count or SHA-256;
- destination escapes `static/one/studio/`;
- registry marker is missing;
- chapter/asset already exists without explicit `--replace`.

For each successful asset it writes a receipt under:

`static/one/dore-publisher-receipts/`

The receipt records chapter key, asset ID, final repo path, public URL with content-hash cache key, format, byte count, SHA-256, dimensions when cheaply detectable, and state `PERSISTED_ASSIGNED_PENDING_DEPLOYMENT`.

A receipt is not `DONE`. The production ledger may move to `LIVE_VERIFIED/DONE` only after the deployed ONE chapter visibly renders that exact revision.

## Separation from ONE runtime

This tool is a production-side utility only.

It must never be loaded by:

- `static/one/index.html`;
- `one-app.js`;
- `one-cover-policy.js`;
- service workers;
- reader-side loaders;
- the temporary production ledger.

No publisher code, receipt, manifest or staging path may become a runtime dependency.

## Replacement of experimental workarounds

Once a plate has been successfully published through this native path and live-verified, any plate-specific base64 staging package, runtime reconstruction bridge, temporary trigger file or workaround created solely for that plate should be removed in the same or immediately following cleanup PR.

The durable architecture is:

`Doré AI / editor → Native Publisher → ONE Studio Asset Registry → ONE Cover Policy → public chapter`

not:

`Doré AI → chat/base64 → staging chunks → runtime reconstruction → cover`.

## Production speed target

The publisher is designed for the remaining large backlog. Generation and approval may remain plate-by-plate, but persistence and Git publication should normally run as waves. A wave should require one binary publishing pass, one registry update set, one commit, one PR, one deployment and one verification sweep—not a full repository workflow for every plate.
