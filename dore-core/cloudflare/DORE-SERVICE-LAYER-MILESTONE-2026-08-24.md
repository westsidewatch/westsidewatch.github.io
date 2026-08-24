# Doré Service Layer — 2026-08-24

Status: **COMPLETE / PASS**

Doré now exposes a product-neutral service contract at `/api/dore/query` (`dore.query.v1`). It accepts GET `?q=` and POST `{query,type?}` and classifies auto queries into scripture, brain, asset, or status lanes.

The response envelope standardizes: `ok`, `schema`, `query`, `type`, `confidence`, `provenance`, `boundary`, plus lane-specific results/delegation metadata.

## Compatibility policy
The service layer deliberately does not replace the proven browser scripture engine in this milestone. Scripture requests are routed by contract to the existing browser search dataset and declare the protected capabilities: reference, chapter, range, multi-reference, exact text, fuzzy, original-language, and entity. This prevents a premature server rewrite from regressing Bible Search.

Brain questions are matched server-side against the canonical Doré knowledge index. A sufficiently confident node is returned with provenance and epistemic boundary; unmatched questions fall back to scripture/search rather than inventing an answer.

Asset queries are routed to the existing D1 Asset Registry service. Status queries are routed to the canonical Doré status snapshot. Thus ONE, Westside Stories, Westside Watch, Journal/Liming and future clients now have one stable Doré entry contract without duplicating routing rules.

## Architecture
Products -> `/api/dore/query` -> Doré service contract -> Scripture / Brain / Asset Registry / Status.

Existing `/dore/search/` remains backward compatible and is a first client, not the definition of Doré itself.

## Gate
PASS criteria for this milestone are architectural and non-destructive: unified endpoint exists; stable schema exists; server-side intent routing exists; Brain has server-side evidence matching; Asset and Status have explicit service delegation; scripture regression surface is preserved rather than rewritten; no R2/D1 placement policy is disturbed.

Next major milestone: **First External Worker — Westside Stories subtitle proofreader**, using the Doré service contract as the cross-product boundary.
