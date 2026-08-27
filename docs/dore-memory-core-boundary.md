# Doré Memory Core Provider Boundary

Status: LOCKED

## Memory Core — must work with no Workers AI binding

- D1 conversation/message persistence
- R2 canonical archive
- Raw historical import with original timestamps and provenance
- Recent recall
- Lexical/text recall
- Cross-conversation same-project recall
- Date/time structured recall and coverage audit

These capabilities MUST NOT require `env.AI` and MUST continue to operate if Workers AI is unavailable or its free allowance is exhausted.

## Optional semantic adapter

Embeddings/vector semantic retrieval are optional enrichment. Failure or absence of an embedding provider must never prevent canonical memory persistence or base recall. A future provider may replace Workers AI without changing Doré Memory Core.

## Workers AI scope

Workers AI is permitted for the public Doré Search AI conversation surface after the user explicitly enters AI mode. It is a response engine for that surface, not Doré's memory system.

## Acceptance rule

A change fails the architecture contract if D1/R2 memory write, structured/lexical recall, cross-session recall, or historical backfill requires an AI model binding.
