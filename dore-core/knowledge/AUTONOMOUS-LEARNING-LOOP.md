# Doré Autonomous Learning Loop

Status: PRIMARY DEVELOPMENT OBJECTIVE
Established: 2026-08-22

## Governing objective

From this point forward, Doré development is judged primarily by whether Doré can **think about unfamiliar work, detect what it does not know, learn from that gap, test the new capability for transfer, and decide whether the resulting answer is fit to surface**.

A larger database is not sufficient. A successful product answer to one known query is not sufficient. A patch that improves only the triggering query is a failure of the learning objective.

## Core loop

`unseen work stimulus → understand/route → attempt → self-evaluate → detect gap → Learning Signal → capability diagnosis → learning plan → evidence-bearing study → candidate Knowledge + Reflex → self-generated transfer tests → consolidation gate → re-attempt → Answer Admission Gate → surface / abstain → retain outcome as future learning evidence`

This loop must be shared by Doré Bible Search, ONE, future subtitle proofreading, Dawn Library and later Doré work nodes.

## Resource Discovery and Reuse Principle

Doré must treat discovery of already-built external capabilities as a permanent part of learning and work, not as an occasional manual search.

Default rule:

`discover continuously → preserve candidates with provenance and evaluation evidence → when a capability is actually needed, retrieve prior candidates → search again for newer/better alternatives → revalidate current candidates → compare → controlled test → reuse/integrate the best fit → build only when necessary → observe → learn`

The governing maxim is:

**Discover continuously. Revalidate before use. Reuse when better. Build only when necessary.**

This applies to open-source tools, libraries, frameworks, MCP servers, agents, datasets, research resources, workflows, media/design tooling, Bible/theology resources and other mature external capabilities relevant to Doré, ONE, Westside Watch, Bible Search, Dawn Library and later work nodes.

Discovery is not adoption. A discovered resource remains a candidate. Doré must preserve enough information to understand why it was considered useful, where it came from, and what evidence supported the evaluation.

Before actual use, Doré must perform just-in-time revalidation even if the candidate was previously judged strong. Revalidation should consider, as applicable:
- whether a newer or better alternative now exists;
- current maintenance/activity and project health;
- architecture and compatibility with Doré's current system;
- license, provenance, rights and security implications;
- cost and dependency burden;
- measured performance/reliability where evidence exists;
- whether direct reuse, partial reuse, learning from the design, or building internally is the best choice.

Doré must not accumulate third-party packages merely because they are popular. External resources should strengthen Doré's coherent architecture rather than replace architectural judgment.

A previously saved candidate is therefore a starting point for a fresh decision, never a permanent answer.

## Self-evaluation signals

Doré must be able to emit at least:
- `NO_RESULT`
- `LOW_CONFIDENCE`
- `INTENT_UNRESOLVED`
- `CAPABILITY_MISSING`
- `LEXICAL_COLLISION`
- `ENTITY_FRAGMENT`
- `EVIDENCE_INSUFFICIENT`
- `CONTRADICTION`
- `OUT_OF_SCOPE`

A user report may confirm a signal, but human reporting must not be required for the loop to exist.

## Learning rule

The triggering query is a stimulus, never the lesson specification.

Doré must diagnose a reusable missing capability. Example:

`舊約有聖靈嗎？` may expose `PRESENCE_BY_SCOPE + CONCEPT_RESOLUTION + CANONICAL_AGGREGATION`; it must not create a special `old_testament_holy_spirit` answer rule.

The same principle applies to `聖經有幾位馬利亞？`, `十字架的影子`, subtitle errors, ONE questions and future library-management tasks.

## Evidence-bearing study

Autonomous learning does not mean unconstrained ingestion. Doré may study only through admitted source routes and must preserve provenance/evidence class. Search results, ONE editorial prose, user wording and brand content are stimuli unless independently admitted as evidence.

New knowledge and reflexes remain provisional until transfer tests pass.

## Transfer requirement

A learning episode cannot graduate on its triggering query. It must pass:
1. paraphrase transfer;
2. different-entity/content transfer;
3. at least one unseen question/task in the same inferred capability family;
4. regression against previously graduated capabilities;
5. evidence-boundary checks.

If the trigger improves but transfer fails, classify the episode as `MEMORIZED_PATCH` and reject consolidation.

## Answer Admission Gate

After learning, Doré re-attempts the original work. An answer is surfaced only if:
- intent/scope are sufficiently understood;
- required capability is available;
- evidence is sufficient for the wording used;
- uncertainty/controversy is represented where required;
- no lower-level failure signal remains unresolved.

Otherwise Doré abstains or surfaces a bounded partial result while retaining the learning task.

## First reserved autonomous-learning experiment

Stimulus: `舊約有聖靈嗎？`

This is a reserved stimulus, not training data. Do not hard-code its answer, aliases, verse list or dedicated intent rule.

Success requires Doré to discover the missing reusable capability, study through admitted Scripture/language/world resources, generate transfer tests that do not merely repeat this question, consolidate only after transfer, and then independently decide whether it can answer.

A successful answer to this stimulus alone is **not** graduation. Blind transfer tasks are mandatory.

## Relationship to Biblical World

Autonomous Learning Loop is below and across BW-1 through BW-6. Biblical World education continues, but each section must increasingly be teachable through this loop. BW stages supply knowledge domains; the loop supplies Doré's ability to grow from work.

Do not proceed by manually patching every geography, chronology, entity or concept query. A repeated failure family should become a capability-learning episode.

## Work-node principle

- **Doré Search** supplies unpredictable public stimuli.
- **ONE** supplies passage-bounded Scripture, structured study entry points and recurring real study questions.
- **Subtitle proofreader** will supply lexical/contextual correction failures.
- **Dawn Library** will eventually supply new books, metadata, concepts and collection-management tasks.

Work must feed education. Education must improve work. Product-specific presentation must not become Core truth.

## Graduation target

Reserved milestone: `AUTONOMOUS_LEARNING_LOOP_1_0`

It may be issued only after an end-to-end run demonstrates, without a trigger-specific patch:

`unknown → self-detected gap → self-directed study → transferable new capability → regression-safe consolidation → evidence-gated answer`

on the reserved stimulus plus blind transfer tasks.
