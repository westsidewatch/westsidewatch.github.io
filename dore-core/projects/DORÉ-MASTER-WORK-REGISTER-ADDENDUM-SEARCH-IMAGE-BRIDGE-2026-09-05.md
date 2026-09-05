# DORÉ MASTER WORK REGISTER — ADDENDUM: SEARCH → RESIDENT IMAGE BRIDGE

Date: 2026-09-05
Status: CANONICAL_ADDENDUM / SWEEP_RECONCILED
Parent register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence: `DORÉ-SEARCH-IMAGE-BRIDGE-EVIDENCE-LEDGER-2026-09-05.md`
P01 impact: NONE

## Canonical interpretation

### SEARCH-IMAGE — Search AI image-command integration

**Status:** `ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

Search AI now has a concrete bounded image-command integration: natural-language image intent can be recognized in Search AI mode, forwarded to a loopback resident Image bridge, executed through the resident Image autorun seam, and returned as a generated artifact reference in the Search conversation UI. The follow-on hardening commit constrains request size/shape, narrows served image types, prevents path leakage/traversal and exposes browser-safe artifact metadata.

This is a legitimate product-integration milestone. It is not evidence that Doré Image has completed real-media acceptance or that the whole visual runtime is production-ready.

### Architecture disposition

The direct `Search browser → 127.0.0.1:8790 → resident Image` path is classified `MAINTENANCE / COMPATIBILITY` as a control-service boundary.

The governing runtime direction remains one persistent intelligence with sparse capabilities routed through the shared typed control plane. Therefore the 8790 endpoint must not silently become a second long-term product-specific orchestration plane. Preserve it while useful for bounded local integration, but nominate it for consolidation once the shared Companion/A2A/capability path has live acceptance.

The reader-facing behavior—asking Doré in Search to generate a purpose-built visual asset—remains valid and should survive that consolidation.

### Authority boundary

Loopback binding, origin checks and `X-Dore-Origin` routing guards improve containment but do not prove cryptographic authorization. Existing Nervous-System authority debt remains open. No capability or local bridge may expand Doré's permission envelope merely because it is technically reachable.

### Revisit candidate

The direct 8790 service boundary is `COMPLETED_REVISIT_CANDIDATE`.

Revisit when:

- the shared typed control plane has live Companion/A2A acceptance;
- Search can route the same image intent through that plane;
- latency/failure/privacy behavior can be compared;
- no concrete isolation need justifies a separate product-specific localhost endpoint.

If parity is proven, retire the 8790 orchestration boundary while preserving the Search image feature.

### Open acceptance evidence

Do not promote beyond this submilestone until there is persisted evidence for:

- one real purpose-built Westside asset generated through a configured resident renderer;
- real visual observations and critic/correction where needed;
- durable checksum/provenance;
- equivalent typed-control-plane execution;
- unauthorized-request refusal at the authority boundary;
- latest-head CI/runtime receipts.

### Relation to VISUAL work

The preferred real acceptance object remains a purpose-built Westside Doré-derived website asset—e.g. engraved light texture, Bethlehem-star grammar, water/sky/stone motif—not an original Doré artwork. Original Doré works remain curated content.

### Relation to P01

No change. P01 remains independently blocked on its approved production audio-acquisition/transcription dependency; this addendum does not alter that critical path.