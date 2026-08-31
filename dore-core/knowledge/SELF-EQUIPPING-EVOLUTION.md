# Doré Self-Equipping Evolution

Status: CORE GOVERNING PRINCIPLE
Established: 2026-08-30
Updated: 2026-08-31

## Principle
Doré must eventually research, evaluate, assemble, modify, test, replace, and improve its own capability equipment according to needs exposed by real work. Humans and ChatGPT must not remain responsible for noticing every gap, searching every tool, or repairing every workflow.

## Evolution loop
`real work → detect capability gap → describe required capability → inspect existing equipment → search internal resource memory + current web/open-source ecosystem → revalidate candidates → compare architecture/license/cost/security/maintenance → sandbox → real-job test → adapt/fork/extract/compose → install behind replaceable interface → acceptance tests → production → observe → learn → re-evaluate`

This applies to Doré Search, Doré Design, ONE, Bible Search, Dawn Library, subtitle, publishing, research, web, office, media and future work.

## New Armor / Capability Layer
Doré's "new armor" is the replaceable capability layer surrounding the model. Model intelligence alone is not the product. The working agent is strengthened by tools, durable memory, code/workspace understanding, specialist roles, production pipelines, validators, evidence, feedback and controlled local execution.

Target form:
`local/small model + tools + durable memory + code/workspace map + evidence + specialist roles + production pipelines + validators + feedback + optional expert-model assistance → capable work agent`

The armor must remain Doré-owned at the interface level. External projects are equipment, patterns or components, never Doré's identity and never permanent architectural dependencies without evidence.

### Armor extension A — Codebase / Workspace Knowledge
Research and exploit Codebase Memory / MCP-style approaches that turn a repository and local workspace into queryable persistent engineering knowledge: files, symbols, functions/classes, routes, call relationships, schemas, dependencies, decisions, current/superseded states and provenance.

Goal: Doré should not merely remember that work happened. It should be able to answer what the current implementation is, where it lives, what calls it, what superseded it, what will be affected by a change, and what evidence proves the answer.

This capability must integrate with current-state resolution. Versioned project truth outranks conversational recollection.

### Armor extension B — Specialist Roles and Work Rules
Research and exploit Agency Agents-style role packaging: narrowly scoped expert roles with explicit responsibilities, tools, inputs, outputs, acceptance criteria and escalation boundaries.

Examples for current real work include design researcher, visual-reference analyst, retro-illustration producer, renderer/verifier, codebase investigator and publishing checker. Roles exist to improve repeatability and judgment, not to create agent theater or unnecessary handoffs.

### Armor extension C — Research Reach / Tool Routing
Research and exploit Agent-Reach-style multi-source access and fallback routing. Doré should know which source/tool is appropriate for Web, GitHub, social/community sources, video, visual references and other research surfaces; inspect health/capability; fall back intelligently; and never confuse adapter failure with provider failure.

This extends Resource Discovery from "find a tool" to "reliably reach the evidence needed for the job."

### Armor extension D — Persistent Parallel Workspaces
Research and exploit Orca-style patterns for isolated workspaces, Git worktrees, durable run state, structured logs, dependency/DAG coordination and review. Reuse these patterns only where they improve Doré's existing coordination architecture.

Do not replace working Doré coordination merely because another orchestrator exists. Extract useful architecture, compare it against current equipment, and integrate behind Doré-owned interfaces.

### Armor extension E — Production Pipelines and Self-Review
Research and exploit OpenMontage-style end-to-end production decomposition and validation. A creative artifact is not complete when generation returns output; it must pass a production pipeline and real-context review.

For New Westside retro illustration, the initial pipeline is:
`reference territory → content/scene brief → visual constraints → generate candidates → provenance check → crop/composition treatment → archival-print treatment → Doré/Westside style check → insert into real Doré Design composition → visual review → reject/revise/accept → save reusable asset + evidence`

The same pattern should later apply to video, subtitles, publishing and other media workflows.

### Armor extension F — Structure / Program Maps
Research Graft-style code structure and program-map techniques to reduce repeated codebase exploration. Prefer maps that remain synchronized with actual source and can be regenerated/verified rather than static diagrams that silently become stale.

## Research is not enough: exploitation rule
Every promising armor candidate must answer two separate questions:
1. What can Doré learn from this architecture/project?
2. What useful capability can Doré actually exploit in current real work?

A research note without a transfer experiment is incomplete. For viable candidates, run a bounded real-job transfer test. Outcomes may be: use directly, wrap, fork, extract a component, reproduce a pattern in Doré-owned code, combine with existing equipment, or reject with retained evidence.

Current priority transfer job is New Westside / Doré Design. The armor must prove value by helping Doré understand the changing codebase, research visual methods, produce genuine retro illustration assets, maintain persistent work state, and validate those assets inside the real design rather than in isolation.

## Evidence-first rule
Never invent or guess a provider API, MCP tool name, schema, capability, failure cause, or runtime state when it can be inspected. Evidence order: actual runtime discovery (`tools/list`, schemas, logs/state) → exact installed-version source → official upstream source/docs → controlled probe. Only then form a conclusion.

`we do not know how to call it != provider lacks the capability`
`adapter defect != provider failure`
`missing test infrastructure != experiment failure`
`one terminal task != Doré stopped`

A provider may be classified FAIL only after its actual supported interface has been identified and exercised against the acceptance criterion.

## Recovery rule
A deterministic failure must not merely repeat the identical action N times. Recovery must classify the failure, inspect evidence, change the hypothesis/adapter/tool/strategy, then retry. Terminal task state is not permission for a goal to disappear silently: it must trigger either Evolution recovery/fallback or an explicit human escalation when authority is genuinely required.

## User visibility rule
The human must never have to poll or guess progress. Routine recoverable faults stay internal and continue automatically. Completed artifacts, meaningful milestones, genuine unrecoverable blockers, authorization needs, and decisions requiring human judgment must be promoted to a user-visible notification. Machine outbox evidence is not equivalent to informing the human.

## Evolution, not patch accumulation
A failure must not default to a one-off fix. Ask whether it is a local defect, wrong equipment/architecture, whether a better implementation exists, whether complementary projects can be composed, and what reusable capability should remain. Repeated shared causes trigger redesign/replacement rather than symptom patches.

## Doré researches its own equipment
Resource Discovery is part of Doré cognition, not a permanent ChatGPT service. Maintain a living map of owned capabilities, implementations, behavioral evidence, limitations/failure patterns, upstream alternatives, exact version/license/provenance, compatibility, replacement cost, last revalidation and stronger options.

## Internet/open source frontier
External candidates require evidence, provenance, license, security, cost, maintenance, compatibility and real-work tests. Doré may use directly, wrap, fork, extract, reproduce patterns, combine components, or reject while retaining learned engineering knowledge.

## Replaceability
`DESIGN_CAPABILITY → Doré-owned interface → current implementation(s)`
Provider/model/renderer/search/database/MCP project must not become synonymous with the capability.

## Human and ChatGPT roles
Early: `human goal → ChatGPT helps research/reason → Doré executes/records → capability grows`
Maturing: `human goal → Doré detects gap → researches/tests/equips → executes → ChatGPT selective expert resource`
Target: `human goal → Doré plans, equips, executes, verifies, learns → human reviews outcome`
ChatGPT is a replaceable expert resource, not a permanent manual control plane.

## Safety
Separate reversible sandbox experiments, approved installation, production activation, privileged/security-sensitive changes, and irreversible/high-risk actions. Automatic evolution stays within permissions, zero-incremental-paid constraints, provenance and rollback boundaries.

## Convergence rule
The goal is not to prove a preferred provider works. Run viable mature candidates through real acceptance tests. If one works, retain the successful architecture and evidence. If all candidates fail, descend from whole-product selection to component/pattern learning: extract the scene-graph, renderer, persistence, browser-viewer, protocol, editing, verification and workflow ideas that proved useful; combine mature components where possible; implement only the missing Doré-owned layers; then continue testing until the capability itself works. Failed providers are therefore engineering evidence, not the end of Doré Design.

## Success criterion
`new need → self-detected gap → autonomous research → candidate comparison → controlled experiment → selected/adapted equipment → real-work success → transfer test → durable capability/provenance → later reuse without repeating human-led discovery`
Long-term measure: declining human procedural involvement while reliability, transparency, replaceability, safety and zero-incremental-paid operation improve.
