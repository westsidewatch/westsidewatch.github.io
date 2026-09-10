# DORÉ MULTIWRITE NATIVE-STRUCTURE IMPORT — EVIDENCE LEDGER

Date: 2026-09-10
Status: ACTIVE / BOUNDED IMPLEMENTATION EVIDENCE
Sweep parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register classification: `STEWARDSHIP` / existing-product enrichment
P01 impact: NONE

## Evidence reviewed

1. Commit `aefa5fb60ff53186165db42c041acf21fdd188cb` — `feat(multiwrite): read EPUB nav and NCX chapter titles`.
2. Commit `58ba07a2f2eca372f6a45b6687837645b3ecd580` — `feat(multiwrite): preserve native chapter structure across imports`.
3. Commit `783ee3efa1e05f8c3d090f60abeacdbe5acef4ee` — `chore(multiwrite): ship native structure import update`.
4. Current implementation paths evidenced by those commits: `static/multiwrite/publication-adapter.mjs`, `static/multiwrite/import.js`, `static/multiwrite/index.html`.

## Reconciled capability state

### EPUB
The adapter now prefers publication-native navigation instead of flattening and re-inferring chapter labels. It reads EPUB3 nav when present, falls back to NCX, preserves spine reading order, and records provenance such as `titleSource` and `structureSource`.

Classification: `ACTIVE / IMPLEMENTED_FOUNDATION`.

### DOCX / HTML / FB2 / PDF
The import path now has format-aware structure extraction rather than routing every non-EPUB format through one flattened-text inference path:

- DOCX: Mammoth conversion plus Title / Heading 1–3 mapping;
- HTML/XHTML: h1–h6 structure;
- FB2: section/title hierarchy;
- PDF: Outline-derived anchors when available;
- Markdown/TXT and formats lacking reliable native structure: retained inference fallback.

Classification: `ACTIVE / IMPLEMENTED_FOUNDATION`.

### Product shipping state
`static/multiwrite/index.html` was updated to describe the native-structure-first behavior and version the import module as `20260910-native-structure1`.

Classification: `IMPLEMENTED / SHIPPED_SOURCE`, not `VERIFIED_COMPLETE`.

## Superseded interpretation

The earlier generic rule “non-EPUB formats are flattened and then inferred” is now `SUPERSEDED_CURRENT_TRUTH` for DOCX, HTML/XHTML, FB2 and PDFs with usable outlines. It remains a deliberate fallback only where native structure is absent or unreadable.

The earlier EPUB behavior that depended primarily on document headings is likewise superseded when nav/NCX labels exist; document headings remain the fallback.

## Missing evidence / revisit candidates

1. No bounded acceptance evidence in this batch proves representative real-file imports for every advertised format.
2. Repository implementation and cache-busted shipping do not prove browser/runtime success, title/order fidelity, malformed-file handling, large-book behavior, mobile behavior or IndexedDB persistence across representative fixtures.
3. PDF outline-to-page anchoring is implementation evidence only; difficult outlines, duplicate destinations, nested hierarchy and scanned/image PDFs remain unverified.
4. HTML heading extraction currently walks sibling content until the next heading; nested containers and structurally complex documents require fixture coverage before fidelity claims.
5. DOCX behavior depends on Mammoth/CDN loading; offline/dependency-failure behavior is not closed by these commits.

Classification: `UNKNOWN_NEEDS_EVIDENCE / COMPLETED_REVISIT_CANDIDATE`, not a blocker.

## Smallest next proof

Persist one deterministic fixture matrix covering at least EPUB3 nav, EPUB2 NCX, DOCX headings, HTML headings, FB2 nested sections, PDF outline, Markdown fallback and plain-text fallback. For each fixture verify chapter titles, order, source provenance, fallback semantics, validation and saved/read-back book structure. Add at least one malformed/dependency-failure negative fixture. Only then consider a bounded native-import acceptance token.

## Governing conclusion

The 2026-09-10 sequence is a real product-capability milestone: 多寫 now has a native-structure-first import architecture across several formats. It is not yet a cross-format verified-complete milestone. Existing `STEWARDSHIP` status in the canonical Master Work Register remains sufficient; no roadmap priority or P01 state changes are justified by this evidence.
