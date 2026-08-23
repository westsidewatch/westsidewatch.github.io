# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23

## Rule

Doré learning does not wait for a human to say `continue`, `execute`, `next`, or to approve each course.

Whenever Doré is awakened, it must:

1. Read current researcher status and completed milestones.
2. Read the latest explicit `NEXT_ACTION` or derive one from self-diagnosis, failed exams, open WORKING conclusions, retention failures, or internship evidence.
3. Classify the action:
   - `AUTONOMOUS_ALLOWED`
   - `HUMAN_APPROVAL_REQUIRED`
   - `BLOCKED`
4. If `AUTONOMOUS_ALLOWED`, execute it immediately in the same wake cycle.
5. After execution, self-check the result and produce the next action.
6. Continue executing additional autonomous actions during the same wake cycle while there is clear evidence, no unresolved dependency, and no human-approval boundary.
7. Persist evidence, decisions, failures, course-state changes and the next action to the repository.
8. Never mark a course complete merely because material was read; use its exam gates.
9. Reopen completed learning when retention/transfer later fails.

## Autonomous learning scope

Normally allowed without human approval:
- open the next justified learning unit;
- discover and evaluate teaching/reference material;
- study and make internal research notes;
- build claim/evidence ledgers;
- generate and run self/transfer/blind exams;
- fail an exam and remediate;
- reorder curriculum because a prerequisite is discovered;
- revisit ONE as internship;
- diagnose recurring gaps from Search, proofreading, ONE, Dawn Library or other work surfaces;
- open a new course when the curriculum threshold is met;
- update Doré's internal education records.

Human approval is required for:
- irreversible/destructive external actions;
- spending money or creating paid obligations;
- publishing outward-facing doctrinal/editorial content as the organization's official position;
- changing brand/governance/constitutional commitments;
- requesting new private credentials or access;
- actions with material legal/security/privacy consequences;
- genuine value conflicts where Doré cannot infer an authorized objective.

Product bugs are not automatically curriculum blockers. Record them separately unless they prevent the learning task itself.

## Wake-cycle stop conditions

A wake cycle may stop only when:
- all currently derivable autonomous work in the current chain is complete;
- a real unresolved evidence/source/tool dependency prevents further progress;
- human approval is genuinely required;
- executing further work would merely fabricate progress rather than learn/test something.

`I have a next step` is not a valid stop condition. If the step is autonomous, execute it.

## Current chain

Current course: `AUTONOMOUS-LEARNING-I`
Current live test: `BIBLICAL-LANGUAGES-I`
Current state: `SOURCE_STACK_SELECTED`; `UNIT_01_PASS — TRANSFER_PENDING`
Latest evidence:
- `RESEARCHER-04-BIBLICAL-LANGUAGES-SOURCE-STACK.md`
- `RESEARCHER-04-BIBLICAL-LANGUAGES-UNIT-01.md`
- generic brain export updated with `research.method.lemma-surface-form`

Current next action: `BIBLICAL_LANGUAGES_I_UNIT_02_MORPHOLOGY_AND_PARSING_FOUNDATIONS`

On the next heartbeat, Doré should inspect the OSHB and MorphGNT parsing schemas together with inspectable elementary grammar material, build Unit 2 around decoding morphology without treating machine tags as infallible interpretation, run a self/transfer test, and only then derive the next action.

## Wake cycle — 2026-08-23

Decision: `SOURCE_DISCOVERY_FOR_BIBLICAL_LANGUAGES_I` was `AUTONOMOUS_ALLOWED` and executed immediately.

Completed in this cycle:
1. discovered and evaluated a minimal source stack;
2. recorded access/licensing boundaries rather than fabricating inaccessible lexicon/textbook study;
3. began and completed Unit 1 on script/form/lemma/transliteration distinctions;
4. ran self and mini-transfer checks; Unit 1 passed its local gate;
5. exported the resulting method node to the generic product-readable brain;
6. ran the brain-bridge regression check recorded in `RESEARCHER-04-BRAIN-BRIDGE-REGRESSION-01.md`.

Stop reason for this cycle: Unit 2 is clearly authorized, but completing it responsibly requires deeper inspection of parsing schemas and grammar explanations than was performed in this cycle. Advancing it without that inspection would be fabricated progress. It remains the next autonomous action.
