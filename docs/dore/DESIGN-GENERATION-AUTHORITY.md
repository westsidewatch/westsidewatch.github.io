# Doré Design Generation Authority

Status: ACTIVE CANONICAL CONTRACT

## Purpose

Close the execution gap between Doré design research and actual image generation.

Research, visual evidence, editorial grammar and prior approved prompt work must not remain passive reference material. Any Doré-controlled formal visual generation path must resolve the applicable canonical design authority before a generator is invoked.

This contract extends `docs/dore/DESIGN-WORKING-MEMORY.md`; it does not create a parallel design system.

## Core rule

```text
consumer / task
      ↓
resolve design scope
      ↓
resolve canonical grammar
      ↓
resolve canonical generation prompt
      ↓
compose subject-specific prompt
      ↓
GENERATOR
      ↓
visual readback
      ↓
compare against resolved grammar + evidence
      ↓
correct / regenerate
      ↓
verified result
```

Formal generation MUST NOT silently bypass the authority-resolution steps.

## Gate G1 — Scope resolution

Before generation, resolve:
- consumer/project;
- artifact type;
- design family/tradition when applicable;
- requested or inherited grammar;
- source-image preservation requirements;
- current final/verified design decisions.

Conversation wording is input, not automatically canonical authority.

## Gate G2 — Grammar resolution

A selected editorial/design grammar must resolve to a traceable canonical record.

The record may include:
- layout;
- image treatment;
- typography;
- material/surface;
- density;
- sequence;
- irony;
- motion/emergence;
- visual evidence references;
- explicit exclusions.

If multiple historical records conflict, use Doré truth-state rules: `final/verified` outranks proposal, attempt and reference. Rejected/corrected material must never silently return as current grammar.

## Gate G3 — Prompt resolution

`resolve_generation_prompt()` is a required conceptual interface for formal Doré visual generation.

It must return a prompt assembled from canonical authority, not an improvised stylistic summary from chat memory.

Minimum resolved payload:

```text
consumer
artifact_type
grammar_id
grammar_version
canonical_prompt
visual_evidence[]
source_preservation_rules[]
exclusions[]
authority_sources[]
truth_state
```

The subject, copy, dimensions and immediate composition request may be injected at runtime. They must not overwrite canonical grammar unless the user explicitly changes the design direction.

## Fail-closed rule

For formal/canonical output:

**If the requested grammar or canonical generation prompt cannot be resolved, generation is BLOCKED.**

The system must report the missing authority rather than inventing a substitute prompt and presenting it as Doré-derived output.

Exploratory generation is allowed only when explicitly marked `exploration / evaluation-only`. It cannot become historical or design authority without later verification and promotion.

## Gate G4 — Visual Evidence Layer

Where a grammar has visual evidence, generation must carry the evidence identifiers/references into the resolved generation context.

Evidence is used to constrain interpretation; generated images are never themselves historical authority.

Example authority pattern already established in design experiments:

```text
Selected grammar:
- layout: ...
- image: ...
- typography: ...
- material: ...
- density: ...
- sequence: ...
- emergence: ...

Visual evidence authority: <evidence ids>
Generated images remain evaluation-only and are never historical authority.
```

## Gate G5 — Visual verification loop

A successful generator call is not PASS.

After generation Doré must, where the execution environment supports visual readback:
1. inspect the visible result;
2. compare it with resolved canonical grammar;
3. compare it with visual evidence constraints;
4. identify material mismatches;
5. patch the generation instructions without mutating canonical authority;
6. regenerate when needed;
7. mark the result `verified` only after visual acceptance.

This inherits Gate D4 from `DESIGN-WORKING-MEMORY.md` and applies the same principle to image generation.

## Italian Magazine / editorial research

Italian editorial research is a seed tradition and design-learning authority, not a generic suffix such as “Italian magazine style”.

Domus, Casabella, Ottagono, Abitare, IL and other studied traditions must remain distinguishable grammars with traceable evidence. A consumer may combine or mutate grammars only through an explicit exploration step; the resolver must not flatten them into one aesthetic preset.

Existing known experiment identifiers such as `domus-ponti-*`, `domus-lupi-*`, `casabella-*` and related visual-evidence IDs must be recovered into canonical records before they can be relied upon by formal generation. Their appearance in historical conversation alone is insufficient runtime authority.

## Consumer inheritance

This gate is shared Doré Core capability. Consumers such as Westside Watch, Living Water, ONE, Cinema, Chidi, Neser and game/publication work should consume the same resolver rather than maintaining independent prompt folklore.

Consumer-specific art direction remains local; authority resolution remains shared.

## Non-goals

Do not:
- create a second Doré design system;
- duplicate every research note into prompts;
- treat generated images as historical evidence;
- let chat memory outrank canonical records;
- require every consumer to implement its own resolver;
- silently fall back to vague style labels.

## Immediate recovery work

The next implementation pass must locate and classify existing Italian Magazine / editorial grammar and prompt assets across repository history, Doré runtime/local assets and research records, then normalize them into canonical resolvable records.

Until recovery is complete, missing grammars must fail closed for formal generation.

## Acceptance test

PASS requires this scenario:

1. A consumer requests an image using a known studied editorial grammar.
2. Doré resolves the exact canonical grammar and prompt without the user re-pasting it.
3. The generation payload records its authority sources and evidence IDs.
4. The generator receives the resolved prompt plus only task-specific variables.
5. The result is visually checked against the grammar.
6. A mismatch triggers correction rather than silent acceptance.
7. A new conversation can repeat the process from canonical authority rather than remembered chat wording.
