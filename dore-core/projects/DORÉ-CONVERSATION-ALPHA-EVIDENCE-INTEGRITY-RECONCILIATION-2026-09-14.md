# DORÉ CONVERSATION ALPHA — EVIDENCE INTEGRITY RECONCILIATION

Date: 2026-09-14
Status: SWEEP-01 DURABLE EVIDENCE
Related work: `CONVERSATION`, `CONV-MEM-V1`, `CORE`
P01 impact: NONE

## Bounded evidence reviewed

- `dore-core/tests/memory-layer-contract.mjs`;
- `dore-core/tests/test_conversation_context.py`;
- `dore-core/tests/test_conversation_contribution.py`;
- `dore-core/tests/test_conversation_meeting_close.py`;
- `dore-core/runtime/build_conversation_context.py`;
- `dore-core/runtime/conversation_contribution.py`;
- canonical Master Register interpretation of Conversation Runtime Internal Alpha.

## Finding

Conversation Runtime Internal Alpha remains a legitimate bounded historical `VERIFIED_COMPLETE / COMPONENT / INTERNAL_ONLY` milestone for its original structural contract: it loads a bounded active-project context, exposes explicit authority boundaries, requires evidence references for fact-like contribution classes, rejects unknown evidence references, prevents speculative contributions from becoming persistence-eligible facts, closes meetings with project-scope checks, and can replay durable meeting memory.

However, the current implementation does **not** prove semantic grounding of contribution content to the cited evidence. `conversation_contribution.py` verifies that each cited reference names an available source, but it does not verify that the contribution text is actually entailed by that source. The current test fixtures expose this boundary directly: `test_conversation_contribution.py` and `test_conversation_meeting_close.py` can construct persistence-eligible evidence statements saying P01 is `RUNNABLE` merely by citing `persistent_runtime_state`, even though the canonical runtime has since advanced to `BLOCKED / ENVIRONMENT_BLOCKED`.

This is not evidence that the original Internal Alpha milestone was fraudulent; it shows that the word **grounded** must be interpreted narrowly as **source-referenced / structurally grounded**, not semantically verified against current source content.

## Current quality judgment

- bounded context loading: strong for the original internal-only milestone;
- source-reference existence validation: real and useful;
- uncertainty/type/authority envelope: real and useful;
- persistence filtering for speculative items: real and useful;
- semantic claim-to-evidence entailment: `UNKNOWN_NEEDS_EVIDENCE` / not implemented by the reviewed boundary;
- stale-source contradiction protection: not demonstrated;
- public/consequential decision authority: still explicitly not authorized.

## Classification

- Conversation Runtime Internal Alpha original milestone: retain `VERIFIED_COMPLETE / COMPONENT / INTERNAL_ONLY`;
- semantic evidence integrity of persisted contributions: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`;
- completed Internal Alpha quality disposition: `COMPLETED_REVISIT_CANDIDATE / MAINTENANCE HARDENING`, only if the contribution envelope is reused for consequential memory, planning, or future Conversation expansion.

## Smallest useful future proof

Add a bounded evidence-claim verification layer or equivalent typed assertion contract so a persistence-eligible `evidence` contribution cannot pass merely because it cites an existing source. At minimum:

1. include a machine-readable claim/assertion form for state facts such as project status/blocker;
2. verify that assertion against the loaded current source packet;
3. add a negative regression where a stale claim (`P01 is RUNNABLE`) cites the current blocked runtime source and is rejected or explicitly downgraded to contradiction/unverified;
4. preserve the existing authority, scope, speculation and persistence gates;
5. only then describe persisted fact-like contributions as semantically evidence-grounded.

A general natural-language entailment engine is not required for this first repair; typed high-value project-state assertions are sufficient to close the concrete gap without overbuilding.

## Priority

MEDIUM. This should not interrupt P01. Raise priority before Conversation Alpha is used to persist consequential project facts automatically, before public Conversation authorization is reconsidered, or when `CONV-MEM-V1` begins consuming Alpha contributions as trusted durable memory.

## P01 boundary

No subtitle runtime state, blocker, ordering, deployment, binding, credential, or resume condition was modified in this reconciliation.