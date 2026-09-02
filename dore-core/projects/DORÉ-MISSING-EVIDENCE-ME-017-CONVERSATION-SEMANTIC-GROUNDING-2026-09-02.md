# ME-017 — Conversation fact-like contribution semantic grounding

Date identified: 2026-09-02
Sweep: `MEMORY-CONSOLIDATION-SWEEP-01`
Related work: `CONVERSATION`, `NERVOUS-SYSTEM`, Conversation Internal Alpha, Conversation Memory Layer
Classification: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`
Priority: MEDIUM, subordinate to P01

## What is already evidenced

The internal Conversation Alpha and its tests enforce several real safety/evidence boundaries:

- current active-project scoping;
- internal-only/non-public authority;
- human church authority remains final;
- fact-like contributions require one or more known evidence references;
- unknown evidence references are rejected;
- speculative decision candidates are not persistence-eligible;
- project-mismatched meeting contributions are rejected;
- persistence/replay round trips are implemented and tested.

The bounded Conversation Internal Alpha continuity milestone remains legitimately `VERIFIED_COMPLETE / INTERNAL_ONLY / NOT_PUBLIC` for those claims.

## What is not yet evidenced strongly enough

The current contribution contract/tests do not prove semantic entailment between a fact-like contribution and the source it cites.

Concrete bounded evidence:

- current `dore-core/runtime/project-execution-state.json` says P01 is `ENVIRONMENT_BLOCKED` at attempt 39;
- `dore-core/tests/test_conversation_contribution.py` constructs `P01 remains runnable but production verification is incomplete.` as a grounded judgment while citing `persistent_runtime_state`;
- `dore-core/tests/test_conversation_meeting_close.py` constructs `P01 remains RUNNABLE in persistent runtime state.` as persistable evidence while citing the same source;
- the builder verifies that the source id exists, but the reviewed test contract does not demonstrate that the factual sentence is actually supported by the current source content.

The older persisted meeting record itself is not proof of a bug: it correctly labels `project_state_at_close: RUNNABLE` as historical meeting state. The hardening gap is allowing a newly-created fact-like statement to inherit credibility solely from a valid source identifier even when the current source contradicts the sentence.

## Why this matters

Citation presence is not the same as grounded evidence. Without an entailment/currentness check, a stale or fabricated factual sentence can become persistence-eligible while carrying a real evidence reference. This is especially important for mutable runtime claims, authority state, project status, blockers and production verification.

## Smallest useful future evidence

Add one bounded semantic-grounding acceptance gate for fact-like contributions:

1. create a current or synthetic `persistent_runtime_state` fixture with a known project state;
2. submit one entailing factual contribution and prove it is accepted;
3. submit one contradictory factual contribution using the same valid evidence reference and prove it is rejected, downgraded to non-fact/speculation, or marked unresolved;
4. update mutable tests to derive expected state from the packet or use explicitly frozen historical/synthetic fixtures rather than hard-coded live-state prose;
5. persist the test result and only then consider this evidence gap resolved.

## Current disposition

- do not demote the bounded Conversation Internal Alpha continuity milestone;
- treat the stale `RUNNABLE` test wording as `MAINTENANCE` debt;
- treat semantic evidence entailment as `UNKNOWN_NEEDS_EVIDENCE` until the bounded negative/positive gate passes;
- do not interrupt or modify P01 for this work.

Aggregate linkage: this adjunct should be folded into `DORÉ-MISSING-EVIDENCE-REGISTER.md` as `ME-017` during the next dependency-safe aggregate reconciliation.