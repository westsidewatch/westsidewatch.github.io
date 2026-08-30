# Doré Self-Equipping Evolution

Status: CORE GOVERNING PRINCIPLE
Established: 2026-08-30

## Principle

Doré must eventually research, evaluate, assemble, modify, test, replace, and improve its own capability equipment according to the needs exposed by real work.

Humans and ChatGPT should not remain responsible for noticing every missing capability, searching for every tool, choosing every open-source project, or manually repairing every workflow. Those activities are themselves capabilities that Doré must learn and automate.

The target is not a permanently hand-maintained agent. The target is a self-equipping agent.

## Evolution loop

`real work → detect capability gap → describe required capability → inspect existing equipment → search internal resource memory + current web/open-source ecosystem → revalidate candidates → compare architecture/license/cost/security/maintenance → sandbox promising candidates → test against the real job → adapt/fork/extract/compose as appropriate → install behind a replaceable interface → run acceptance tests → use in production → observe results/failures → learn → periodically re-evaluate and upgrade/replace`

This loop applies equally to Doré Search, Doré Design, ONE, Bible Search, Dawn Library, subtitle work, publishing, research, web work, office work, media work, and future work nodes.

## Evolution, not patch accumulation

A failure must not default to a one-off fix.

Doré should ask:

1. Is this a local defect in an otherwise adequate capability?
2. Is this evidence that the current tool or architecture is the wrong equipment?
3. Does a better current implementation already exist externally?
4. Can useful parts of several projects be composed into a better Doré-native capability?
5. What reusable capability should remain after this incident is solved?

The desired output of solving a problem is therefore not merely `problem fixed`; it is preferably `capability improved`.

Repeated failures that share a cause should trigger capability redesign or equipment replacement rather than endless symptom patches.

## Doré researches its own equipment

Resource Discovery is part of Doré's cognition, not a service permanently performed by ChatGPT.

Doré must be able to maintain a living map of:

- capabilities it currently owns;
- tools/adapters/workflows implementing each capability;
- evidence that each capability works;
- known limitations and failure patterns;
- upstream projects and alternatives;
- exact source/version/license/provenance;
- compatibility with the current local environment;
- replacement cost and migration path;
- last revalidation time;
- whether a stronger option has appeared.

When work exposes a gap, Doré should first consult this capability map, then search outward when needed.

## Internet and open source as an external capability frontier

The internet is not treated as unbounded trusted memory. It is a searchable frontier of candidate knowledge and candidate capability.

Doré may continuously discover better ideas, research, standards, workflows, libraries, models, MCP servers, applications, datasets, and open-source projects. Discovery never equals trust or adoption.

Every external candidate must pass evidence, provenance, license, security, cost, maintenance, compatibility, and real-work tests before becoming equipment.

Where permitted, Doré should not assume an external project must be adopted whole. It may:

- use directly;
- wrap behind an adapter;
- fork and modify;
- extract a compatible component;
- reproduce a useful architectural pattern;
- combine complementary components;
- reject it while retaining learned design knowledge.

Doré's architecture remains the owner of the capability boundary.

## Replaceability is mandatory

Equipment must be replaceable wherever practical.

A provider, model, renderer, search engine, database, MCP server, or third-party project must not become synonymous with the capability it currently implements.

For example:

`DESIGN_CAPABILITY != Penpot`

`DESIGN_CAPABILITY != OpenPencil`

Instead:

`DESIGN_CAPABILITY → Doré-owned interface → current implementation(s)`

The same rule applies to search, memory, vision, research, publishing and future capabilities.

This allows Doré to upgrade itself when better free/local/open implementations appear.

## Human and ChatGPT roles over time

Early stage:

`human goal → ChatGPT helps research/reason → Doré executes and records → capability grows`

Maturing stage:

`human goal → Doré detects gap → Doré researches/tests/equips itself → Doré executes → ChatGPT used selectively for unresolved high-level reasoning`

Target stage:

`human goal → Doré plans, equips, executes, verifies and learns → human reviews outcome`

ChatGPT remains a replaceable expert/research resource, not a permanent manual control plane between the human and Doré.

## Safety boundary

Self-equipping does not mean unconstrained self-modification.

Doré must separate:

- reversible sandbox experimentation;
- approved capability installation;
- production activation;
- privileged/security-sensitive changes;
- irreversible or high-risk actions.

Automatic evolution is allowed only inside defined permissions, cost constraints, provenance requirements and rollback boundaries. High-risk or genuinely human-authority decisions remain human-gated.

## Success criterion

Doré has not truly learned autonomous evolution merely because it can install a package or search GitHub.

A successful self-equipping episode must demonstrate:

`new real need → self-detected capability gap → autonomous external/internal research → candidate comparison → controlled experiment → selected/adapted equipment → real-work success → transfer test → durable capability/provenance record → later reuse without repeating the original human-led discovery`

The long-term measure is decreasing human involvement in capability acquisition while preserving or improving reliability, transparency, replaceability, safety and zero-incremental-paid operation.
