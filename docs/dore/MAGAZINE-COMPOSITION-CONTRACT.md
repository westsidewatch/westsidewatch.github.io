# Doré Magazine Composition Contract v1

Status: ACTIVE EXPERIMENTAL CONTRACT

Doré Magazine Engine extends the existing Design Generation Authority. It is not a parallel design system.

## Pipeline

content entity
→ editorial brief
→ reference retrieval
→ asset intelligence
→ canonical Italian editorial grammar
→ structured layout candidates
→ editorial reward + hard geometry gates
→ deterministic HTML/CSS/SVG composition
→ responsive/multi-surface render
→ human feedback
→ publication preflight

## Required interfaces

1. editorialBrief(entity, surface)
2. retrieveReferences(brief, grammar)
3. inspectAssets(assets): provenance, rights, resolution, focal point, crop safety
4. generateCandidates(brief, grammar, assets, references)
5. scoreCandidate(candidate): hard + editorial dimensions
6. compose(candidate): structured production output; generated raster layout is never canonical
7. renderVariants(composition): web, mobile, preview image; print/PDF may be added without changing composition authority
8. recordFeedback(candidate, verdict, edits)
9. preflight(render)

## Hard rules

- Real people are never synthesized as identity-bearing portraits.
- Source portraits remain source assets; layout generation may crop, grade and position but not invent identity.
- A successful image/model call is not a successful design.
- Formal output must resolve an existing canonical grammar through Doré Design Generation Authority.
- References are evidence, not templates to copy.
- Missing rights/provenance, unsafe crop, unreadable typography, overflow, overlap or canonical regression fail closed.
- Human selection and corrections must be recordable as preference evidence.
- Consumer-specific art direction stays local; grammar resolution and scoring stay shared.

## First vertical slice

Olive Mountain speaker covers are the first production test because they stress:
- repeated content type with different identities;
- mixed portrait availability and quality;
- Chinese/English naming;
- responsive crops;
- series metadata;
- coherent publication identity without template repetition.

Acceptance requires multiple structurally distinct candidates for the same speaker, deterministic reproduction of the selected candidate, and a clean no-portrait fallback.
