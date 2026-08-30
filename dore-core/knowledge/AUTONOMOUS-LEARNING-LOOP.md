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

### Free-only hard constraint

Doré resource discovery, evaluation, testing and adoption must follow the project's **zero incremental paid-dependency principle**.

A candidate may be discovered for awareness even when its cost model is not yet known, but it must not advance to approved, integrated, core dependency or production use until Doré has verified that the intended usage path can operate without introducing a paid API, paid model call, paid SaaS dependency, mandatory subscription, metered commercial service, or other incremental charge.

Open-source code is not automatically free-to-run. If an open-source tool depends on a paid provider for the capability Doré intends to use, that usage path is ineligible unless a genuinely free/local/open replacement path is verified.

Preferred execution order is:

`local/open-source → existing already-free infrastructure → free public standards/protocols/data → free-tier service only when it is non-billing-safe and replaceable`

A free tier that can silently convert into paid usage, requires a payment method for metered overage, or creates an uncontrolled billing risk must not be treated as "free-only" by default.

For every candidate considered for adoption, Doré must record a cost verdict such as `FREE_VERIFIED`, `FREE_PATH_AVAILABLE`, `COST_UNKNOWN`, or `PAID_DEPENDENCY`. Only the first two may pass the cost gate, and `FREE_PATH_AVAILABLE` requires the actual selected integration path itself to remain free.

Doré must prefer a somewhat less capable free solution over a stronger paid-dependent solution unless the user explicitly changes this governing constraint.

### Project-aligned preparation: tools belong at the workbench

A verified resource is not collected merely to possess or use it unchanged. Doré discovers external resources in order to **understand, adapt, reshape and align them to the needs of its own projects** where license and architecture permit.

The mental model is a prepared workshop: a blacksmith prepares the right hammer at the forge; a cook prepares the right spatula at the stove. Tools must not be accumulated in an undifferentiated pile.

Therefore every candidate that passes source, rights/license, security, maintenance and free-only checks must immediately receive a project/capability alignment record before it can become an approved resource. The record must answer:
- Which Doré/ONE/Westside Watch/Bible Search/Dawn Library/work-node problem is this resource for?
- Which existing capability or planned capability does it strengthen, replace or make unnecessary to build?
- Is the intended treatment `DIRECT_USE`, `ADAPT`, `FORK_AND_MODIFY`, `EXTRACT_PATTERN`, `DATA_INGEST`, or `REFERENCE_ONLY`?
- What parts are useful, what parts are unnecessary, and what must be changed to fit our architecture and product rules?
- Where does the resulting capability belong in our own architecture, registry, project or work node?
- What adapter/boundary keeps the external implementation replaceable rather than letting it dictate Doré's architecture?
- What tests prove that the adapted result serves our actual project need?

A resource that has no identified project/capability destination remains `UNASSIGNED_CANDIDATE`; it must not be integrated simply because it is interesting or popular.

The normal preparation path is:

`discover → verify → free-only gate → map to our project/capability → understand internals → choose adaptation mode → sandbox modification/test → register at its proper architectural destination → use in real work → observe → revalidate/replace`

Doré should prefer owning the integration logic, adapters, schemas, prompts/rules and project-specific modifications around an external tool. When license permits and modification is beneficial, Doré may fork or extract only the useful parts rather than inheriting an entire upstream architecture.

External projects are therefore **raw capability material**, not product architecture. Doré's own project map determines where the tool belongs and what shape it must take.

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
