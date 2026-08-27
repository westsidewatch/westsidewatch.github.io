# Doré Design Working Memory

Status: ACTIVE TARGET

## Product goal

Doré must be able to receive a design conversation through Doré Search and use the resulting design knowledge to create and iterate a new Westside Watch website template in Penpot.

This is the acceptance target for the current memory upgrade. General memory work that does not materially advance this target is secondary.

## Required path

```text
Doré Search conversation
        ↓
Design scope + project context
        ↓
Truth-state extraction
        ↓
Design-memory consolidation
        ↓
Current Design Brief
        ↓
Penpot execution
        ↓
Visual readback / verification
        ↓
correction loop
        ↓
verified design state
```

## Gate D1 — Design Scope

PASS when Doré can:
- recognize Scripture/church/theology and Westside Watch global learning scope;
- identify a known Westside Watch project;
- classify a new project as confirmed/candidate/rejected;
- inherit project scope for subsequent coding, UI/UX, layout, typography, image, screenshot, animation, deployment and design discussion;
- avoid requiring every isolated technical/design message to prove brand membership again.

## Gate D2 — Truth State

Every design memory must be capable of carrying one of:
- observation
- reference
- proposal
- attempt
- evidence
- decision
- rejected
- corrected
- final
- verified

Rules:
- discussion is not truth;
- tool/API success is not visual success;
- object/layer creation is not design completion;
- a rejected design must remain historically traceable but must not be presented as the current rule;
- only final/verified state may override a current design rule without explicit contrary evidence.

## Gate D3 — Consolidation

PASS when Doré can build a current design brief from conflicting historical messages without erasing provenance.

The consolidated view must separate:
- current confirmed design grammar;
- active exploration;
- references;
- rejected/corrected ideas;
- unresolved questions;
- source evidence.

Historical raw messages remain immutable evidence.

## Gate D4 — Penpot Visual Verification

PASS requires a closed loop:
1. generate/modify Penpot design;
2. read back the actual Penpot result;
3. inspect visible composition, not merely object metadata;
4. compare against the current design brief and task intent;
5. diagnose mismatch;
6. correct;
7. repeat until verified or explicitly report failure.

A run that creates many layers but renders only blocks/incorrect composition is FAIL.

## Initial Westside visual source status

Existing Figma work is `reference / unfinished`, not a gold-standard target and not automatically `final`.

Existing Penpot Figma-transfer attempt is recorded conceptually as:
- Penpot connectivity: PASS
- object/layer creation: PASS
- faithful/usable visual result: FAIL
- visual verification: FAIL

It must not be used as evidence that Penpot design capability has passed.

## First operational acceptance exam

User converses with Doré through Doré Search and asks Doré to design a new Westside Watch website template.

PASS only if Doré can:
- recall the current Westside visual thinking without the user reteaching it;
- ask only genuinely unresolved design questions;
- form a traceable current design brief;
- execute the design in Penpot through the existing Penpot path;
- visually read back the result;
- revise failed visual output;
- distinguish unfinished/reference material from approved rules;
- preserve the resulting verified decisions as design memory.

## Scope of this upgrade

Priority order:
1. Design Scope / Context Inheritance
2. Truth State
3. Design Consolidation
4. Penpot Visual Verification
5. Search-to-Penpot acceptance

Knowledge Graph and automatic GitHub Journal remain valuable, but they do not block the Penpot design gate unless a dependency is discovered during implementation.
