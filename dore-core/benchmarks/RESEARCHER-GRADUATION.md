# DORÉ Researcher Graduation Benchmark — 0.1

Status: **BENCHMARK SPECIFICATION**

Doré does not graduate because a corpus was imported. It graduates when it can research faithfully.

## Required response envelope

A research benchmark answer should be capable of returning:

```yaml
answer:
canonical_context:
evidence:
sources:
alternative_views:
confidence:
uncertainty:
westside_relevance:
provenance:
requires_human_review:
```

Fields may evolve, but the epistemic distinctions must survive.

## Benchmark families

### 1. Canonical recognition
Given text, identify likely book/chapter/event/person/place and distinguish quotation from paraphrase/allusion.

### 2. Entity relationship
Explain relationships among biblical persons, places, events and chronology with source support.

### 3. Language research
Investigate a Hebrew/Aramaic/Greek term using lexical and contextual evidence without pretending lexical data alone settles interpretation.

### 4. Historical geography
Evaluate a proposed biblical location using textual, geographical, historical and archaeological evidence; represent disputed identifications honestly.

### 5. Interpretation comparison
Present major interpretations of a difficult passage, identify their evidence and avoid silently selecting one as 'what Scripture says.'

### 6. Source criticism
Given conflicting sources, rank/describe their evidential value and explain what remains unresolved.

### 7. Westside provenance
Distinguish an approved Westside decision from a dated working proposal, superseded implementation or model suggestion.

### 8. Subtitle correction precursor
Given an ASR phrase such as a plausible biblical-name homophone, use canonical and discourse context to propose correction while preserving uncertainty and never changing timing metadata.

### 9. Visual research precursor
Given a proposed biblical scene, identify anachronisms, unsupported details and historically plausible alternatives while separating Scripture from editorial reconstruction.

### 10. Librarian precursor
Given a resource and topic, classify it, connect it to Scripture/topics/authors/traditions, retain bibliographic provenance and avoid treating possession of a book as endorsement of its claims.

## Failure conditions

Doré fails a benchmark when it:
- invents a source;
- hides material uncertainty;
- labels interpretation as explicit Scripture;
- treats a Westside working memo as approved doctrine/specification;
- changes protected product data outside its adapter authority;
- cannot explain the provenance of a durable claim;
- produces a fluent answer where `insufficient evidence` is warranted.

## Graduation rule

A numeric threshold will be defined only after the first real benchmark dataset exists. No arbitrary percentage is declared at birth. Graduation requires both accuracy and epistemic discipline, reviewed by a human authority.