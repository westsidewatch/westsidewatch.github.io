# Doré / Jev Context Economy v0

Status: implementation baseline

## Purpose

Reduce Codex engineering context consumption without lowering design quality or engineering correctness.

This is not a second memory or authority system. Canonical Doré authority, Context, Skill Growth, Reflex, System Atlas and project records remain authoritative.

## Local / free boundary

v0 uses no Jev hosted API and introduces no paid inference dependency. "Jev" names the cheap decision/routing role in this pipeline; deterministic local rules are the first implementation.

## Contract

1. Resolve the target before broad repository reads.
2. Admit a bounded working set.
3. Preserve path + SHA-256 provenance for admitted evidence.
4. Reuse verified evidence while its fingerprint is unchanged.
5. Expand context only after an explicit insufficient-evidence decision.
6. Fail closed when no evidence is admitted.
7. Never trade visual quality, canonical authority, correctness, or required verification for context savings.

## Initial API

- bounded_working_set(target, task, candidates, budget)
- fingerprint(path)
- needs_invalidation(cached, path)

This deliberately extends the existing dore_core/context boundary instead of creating a parallel memory/retrieval subsystem.

## Next gate

Instrument real Codex UI tasks and record baseline vs gated:
- files/bytes admitted
- searches/tool calls
- context payload
- repeated reads avoided
- verification outcome
- human visual acceptance

Only measured savings count as success.
