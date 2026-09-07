# Westside Context — minimal projection

This is an internal Doré engineering layer. It does **not** change the public main-site architecture.

## Boundary

`docs/MASTER_SITE_ARCHITECTURE.md` remains the canonical structural source of truth. The compiler reads it and produces a disposable local projection. It never writes back to the source.

The adapter boundary is:

```text
canonical Markdown
      ↓
context compiler
      ↓
SQLite / FTS5
      ↓
Context Packet (match + canonical ancestors + provenance)
      ↓
Doré Core faculties / existing Knowledge / Memory / Graph
```

`Context Packet` is data, not an instruction and not a write capability.

## First implementation

The first slice uses only Python standard library + SQLite FTS5. CJK substring retrieval has a local `LIKE` fallback because SQLite's default `unicode61` tokenizer does not perform Chinese word segmentation.

The projection preserves:

- source path
- source SHA-256
- heading level
- parent relationship
- source-order ordinal
- complete section content

## Non-goals

- no modification of `MASTER_SITE_ARCHITECTURE.md`
- no new public main-site block
- no replacement of Doré Knowledge or Memory
- no third-party memory framework
- no external API
- no automatic structural decisions
- no new graph database
- no vector database before benchmark evidence requires one

## Engineering rule

The target is **能力越大、負擔越小**. Start with the smallest local mechanism that can recover the context Doré actually needs. Expand only when a measured retrieval gap cannot be solved by the existing layer.
