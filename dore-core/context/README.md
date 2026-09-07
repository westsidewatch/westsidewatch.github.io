# Westside Context — minimal projection

This is an internal Doré engineering layer. It does **not** change the public main-site architecture.

## Principle

`docs/MASTER_SITE_ARCHITECTURE.md` remains the canonical structural source of truth. The compiler reads it and produces a disposable, versioned projection for retrieval. It never writes back to the source.

## First implementation

The first slice deliberately uses only Python standard library + SQLite FTS5:

```text
Canonical Markdown
      ↓
heading hierarchy compiler
      ↓
compact context_nodes
      ↓
SQLite FTS5
      ↓
relevant context
      ↓
Doré Core
```

No vector database, embedding API, cloud memory service, GraphRAG framework, or third-party runtime is required.

## Why this is the first slice

The current objective is **能力越大、負擔越小**. We therefore establish a deterministic lexical baseline before adding semantic/vector retrieval. If this baseline satisfies the real Doré context benchmark, additional machinery is not justified.

The projection preserves:

- source path
- source SHA-256
- heading level
- parent relationship
- source-order ordinal
- complete section content

This makes the result traceable back to the canonical Markdown while keeping retrieval separate from the source of truth.

## Explicit non-goals

- no modification of `MASTER_SITE_ARCHITECTURE.md`
- no new public main-site block
- no replacement of Doré Knowledge or Memory
- no third-party memory framework
- no external API
- no automatic structural decisions

The next step is benchmark-driven integration: compare this minimal FTS5 projection against the selected open-source retrieval candidates before introducing any larger dependency.
