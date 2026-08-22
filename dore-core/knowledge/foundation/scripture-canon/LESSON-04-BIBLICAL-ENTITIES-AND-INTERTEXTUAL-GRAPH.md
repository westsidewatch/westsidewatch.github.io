# DORÉ Foundation — Scripture Canon
## Lesson 04: Biblical Entities and Intertextual Graph

Status: **IN PROGRESS**

Student: **Doré / 多雷**

## Lesson principle

> **Connect what Scripture connects; distinguish what Scripture distinguishes; mark what scholarship infers.**

Doré has learned to preserve textual identity, language, witness, morphology and provenance. It now begins learning the internal world of Scripture as a graph of persons, places, peoples, offices, events, genealogies and textual relationships.

## 1. Entity identity is not name identity

A surface name is not yet an entity.

Examples of required discipline:

- two people may share the same name;
- one person may appear under multiple names or spellings;
- a place may change name across periods;
- a title or office is not automatically a personal name;
- a people-group, kingdom and geographic territory must not be collapsed into one object merely because translations use similar wording.

Doré therefore assigns stable entity IDs independently of display names.

## 2. Foundation entity classes

Initial classes:

- `person`
- `place`
- `people_group`
- `kingdom_or_polity`
- `office_or_role`
- `event`
- `artifact_or_object`
- `institution`
- `genealogical_line`

Each entity must be supported by one or more claims with provenance.

## 3. Claims, not blobs

Doré must not store an entity as one paragraph of supposedly certain facts. Each durable fact is a claim.

```yaml
claim:
  subject_id: person.abraham
  predicate: father_of
  object_id: person.isaac
  claim_class: TEXT_EXPLICIT
  references:
    - bible.ref.GEN.21.3
  provenance:
    - witness-or-translation-source
  confidence: 1.0
```

This allows explicit Scripture, inferred chronology, traditional identification and scholarly reconstruction to remain distinguishable.

## 4. Relationship classes

Foundation relationships include:

- parent / child
- ancestor / descendant
- spouse
- sibling
- ruler_of
- priest_of / prophet_to / apostle_of
- born_at / lived_at / traveled_to / died_at
- participant_in_event
- event_at_place
- succeeded / preceded
- contemporary_with
- member_of_people_group
- associated_with_kingdom
- named_as / renamed_as

A relationship may be directional, symmetric, time-bounded or disputed.

## 5. Genealogy discipline

Genealogies are not simple family trees.

Doré must support:

- omitted generations;
- legal versus biological lineage distinctions where evidence supports such analysis;
- repeated names;
- different genealogical presentations in different texts;
- explicit uncertainty where harmonization exceeds evidence.

Matthew 1 and Luke 3 must never be mechanically merged into a single genealogy without preserving their distinct textual presentations.

## 6. Place identity and historical geography

Place records must preserve:

- textual names and aliases;
- approximate or disputed coordinates separately from canonical claims;
- historical period;
- polity/region relationships;
- source of geographic identification;
- uncertainty when ancient location is debated.

Modern map coordinates are scholarly/geographic metadata, not biblical wording.

## 7. Event identity

An event record is not merely a chapter heading. It may connect:

- participants;
- place(s);
- time/chronology claims;
- causes/consequences stated in text;
- parallel accounts;
- later biblical references to the event.

Events must preserve multiple textual witnesses/accounts without erasing differences.

## 8. Intertextual relationship classes

Doré begins distinguishing:

- `explicit_quote`
- `explicit_citation_formula`
- `strong_allusion`
- `probable_allusion`
- `lexical_echo`
- `thematic_parallel`
- `typological_reading`
- `traditional_connection`

Only explicit relationships should be promoted automatically. Other classes require evidence and confidence.

## 9. New Testament use of the Old Testament

When a New Testament text cites or echoes an Old Testament passage, Doré must retain at least:

- NT reference;
- OT reference candidate(s);
- quotation/allusion class;
- wording relationship;
- source-language relationship when available;
- Septuagint/Masoretic or other witness relevance where necessary;
- citation formula if explicit;
- scholarly dispute status.

A verbal similarity alone is not enough to claim quotation.

## 10. Identity safety rules

Doré must fail closed when:

- same-name persons cannot be safely disambiguated;
- a place identification is disputed but presented as certain;
- genealogy links are inferred without classification;
- chronology is reconstructed beyond evidence;
- an allusion is labeled quotation without explicit support;
- traditional harmonization is presented as textual fact.

## Foundation exercises

Doré will be required to demonstrate at least:

1. distinguish multiple biblical persons with the same surface name;
2. model Abraham → Isaac → Jacob as explicit genealogical relations with references;
3. preserve Matthew 1 and Luke 3 as distinct genealogical presentations;
4. represent Jerusalem as an entity with textual aliases without forcing every possible historical/geographic identification into canonical fact;
5. connect Exodus events to later biblical references without claiming that every thematic similarity is an explicit citation;
6. distinguish an explicit quotation from a probable allusion;
7. preserve disputed identity as disputed rather than merging entities.

## Lesson completion gate

Lesson 04 requires:

- machine-readable entity schema;
- claim/relationship schema;
- provenance-bearing identity model;
- first person/place/event registries;
- same-name disambiguation tests;
- genealogy tests;
- intertextual classification tests;
- a small verified graph built from real biblical references before full-corpus graph extraction begins.

## Maxim

> **A connection is useful only when Doré can explain why the connection exists.**
