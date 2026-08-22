# DORÉ Foundation — Scripture Canon
## Lesson 04: Biblical Entities and Intertextual Graph

Status: **IN PROGRESS**

Student: **Doré / 多雷**

## Purpose

After learning to preserve textual identity, original-language layers, provenance, and uncertainty, Doré now begins learning how Scripture's people, places, events, institutions, objects, quotations, genealogies, and cross-text relationships connect without collapsing distinct identities or inventing harmonizations.

## Core entity classes

- person
- people/group
- place
- polity/kingdom/empire
- event
- institution/office
- object
- divine-title/name reference
- genealogy relation
- quotation/allusion candidate
- covenant/law/ritual concept

## Identity rule

A shared surface name does not prove shared identity.

Doré must separate:

```text
mention → candidate entity → resolved entity → relationship claim
```

Every resolution must retain evidence and confidence.

Examples of forbidden shortcuts:

- merging every `Mary/Mariam` into one person;
- merging every `Herod` into one ruler;
- assuming every `Bethany` mention names the same location without context;
- converting a traditional identification into textual fact;
- declaring an allusion certain merely because vocabulary overlaps.

## Relationship classes

Initial graph edges include:

- parent_of / child_of
- ancestor_of / descendant_of
- spouse_of / sibling_of
- ruler_of / subject_of
- located_at / traveled_to / came_from
- participant_in
- contemporary_with
- predecessor_of / successor_of
- quotation_of
- likely_allusion_to
- thematic_parallel_to
- fulfills_claim_about
- disputed_identification_with

Edges themselves are claims and therefore require provenance, evidence class, and confidence.

## Intertextual discipline

Doré must distinguish:

1. explicit quotation identified by the text;
2. strong verbal reuse;
3. probable allusion;
4. thematic parallel;
5. later interpretive association.

These must never be flattened into a generic `cross-reference` relation.

## Foundation exercises

Doré will be required to:

1. distinguish multiple persons with the same or similar names;
2. trace one genealogy without skipping textual gaps or turning literary genealogy into modern biological certainty;
3. represent a place with alternate names while preserving historical/geographic uncertainty;
4. connect an explicit New Testament quotation to its Old Testament source while preserving source text/version questions;
5. distinguish explicit quotation from probable allusion;
6. preserve disputed identifications as parallel candidate claims;
7. return `insufficient evidence` when identity resolution cannot be made safely.

## Required machine-readable outputs

Lesson 04 will produce:

- `ENTITY-SCHEMA-v0.1.yaml`
- `RELATION-SCHEMA-v0.1.yaml`
- `ENTITY-REGISTRY-SEED-v0.1.yaml`
- `INTERTEXTUAL-RELATION-CONTRACT-v0.1.yaml`
- entity-resolution tests
- quotation/allusion provenance tests

## Principle

> **Connect what Scripture connects; distinguish what Scripture distinguishes; mark what scholarship infers.**
