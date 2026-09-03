# Dawn Library `library.books` v1 — Learning Artifact

## Goal
Make the first new executable capability behind the existing Doré Capability Discovery Layer without replacing Doré Search or Conversation.

## Provider choice
Baseline provider: Open Library Search API.

Why: public-good, free, no API key required for low-volume discovery, supports multi-book search in one request, and returns work-level plus edition-related metadata useful for Dawn Library identity work.

## Provider constraints learned
Open Library is suitable for human-facing, low-volume discovery and lookup, not as Dawn Library's bulk backend. Requests should use the API rather than HTML scraping, request only needed fields, identify the application, cache when useful, and avoid bulk harvesting. Dawn Library therefore treats Open Library as a discovery provider, not source-of-truth storage.

## Engineering decision
The adapter is stdlib-only and deferred. It returns a Dawn/Doré normalized envelope while preserving provider identity, endpoint, record key, credential requirement and the explicit absence of paid fallback.

## Architectural consequence
The first real runtime data will be used to discover the next highest-value Dawn Library engineering gap. Likely candidates include Work/Edition identity, duplicate handling, provenance conflict, and local stewardship. These are hypotheses, not a fixed roadmap.

## Invariants
- free-only baseline
- no hidden paid fallback
- provenance required
- Doré Search remains native and unchanged
- Doré Conversation remains unchanged
- provider failures return evidence rather than silently switching to a paid service
- real use drives the next experiment
