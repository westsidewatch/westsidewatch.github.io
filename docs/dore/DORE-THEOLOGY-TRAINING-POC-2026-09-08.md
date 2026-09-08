# Doré Theology Alignment Training POC — 2026-09-08

## Goal

Reduce theological/devotional cross-domain contamination without turning foreign devotional material into Doré Core knowledge.

## Fixed principles

- Base local model remains replaceable; current configured bootstrap default is `gemma4:e4b`.
- No full-model fine-tuning for POC.
- No paid API, cloud training service, or mandatory network call.
- Training/eval adversarial material lives only in an external quarantine workspace.
- Quarantined material MUST NOT be ingested into Doré Knowledge, Memory, Search corpus, Bible World, Study documents, or canonical databases.
- Doré Core stores only abstract authority/policy classes and evaluation outcomes.
- Adapter weights remain separate from the base model; no fusion for POC.
- Theology Rails remain mandatory before and after inference. The adapter improves behavior probability; it does not own theological authority.

## Minimum Sufficient Learning

POC curve:

`0 -> 32 -> 64 -> 128 -> 256`

At every stage, run the same held-out bilingual evaluation. Continue only when the next stage produces a material improvement. Stop at the smallest stage that meets the acceptance threshold.

## Training target

The adapter learns abstract behavior only:

- Christian task/domain recognition
- authority separation
- devotional voice stability
- knowledge is not authority
- comparative-religion research is not devotional adoption
- Chinese/English behavioral consistency

Bible facts, verses, morphology, geography, Strong's relationships, and other canonical evidence stay in Biblical World / evidence substrates rather than being memorized into adapter weights.

## Quarantine boundary

The training wrapper rejects quarantine paths under:

- `~/.dore`
- `~/Library/Application Support/Dore`

The POC copies only the selected split into an ephemeral `/tmp` work directory, trains/evaluates there, and writes only adapter artifacts/reports there unless an explicit later admission step is approved.

## First real-Mac gate

Before any claim of training success, the self-hosted Mac must report:

1. exact runtime model identity;
2. whether `mlx-lm` is installed and its version;
3. peak unified-memory use during the 32-example run;
4. wall-clock training time;
5. adapter size;
6. base-vs-adapter blind bilingual delta;
7. no canonical ingest;
8. no paid API/network dependency;
9. adapter behavioral fingerprint proves the adapter was actually loaded.

No local PASS may be claimed until these values are returned by the Mac.
