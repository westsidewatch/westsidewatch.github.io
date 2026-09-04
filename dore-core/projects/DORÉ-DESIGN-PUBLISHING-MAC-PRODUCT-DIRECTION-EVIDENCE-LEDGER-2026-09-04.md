# DORÉ DESIGN / PUBLISHING / MAC PRODUCT DIRECTION — EVIDENCE LEDGER

Date: 2026-09-04
Status: BOUNDED_RECONCILIATION_COMPLETE
Scope: newly established Doré Design publishing-studio and Dore / 多寫 commercial-product direction
P01 impact: NONE

## Evidence reviewed

- current `dore-design/publishing/EDITORIAL-STUDIO-ARCHITECTURE.md` (`CANONICAL IMPLEMENTATION SPEC`);
- current `dore-design/product/DORE-MAC-COMMERCIAL-PROGRAM.md` (`CANONICAL PRODUCT DIRECTION`);
- commits `5f6966b5cd7d411b337b0e2a3765d3b6dc6e6367`, `5051b12afa2fbf38b42ad1addc5355bcf815dbce`, and `a36f70b2bb1b1534d25c80916981390d0502d3a9`;
- current canonical Master Work Register, especially `VIS-GRAMMAR` and stewardship/product-history boundaries.

## Findings

### 1. Doré Design Publishing Studio is a real canonical direction, not a completed product

The architecture now defines one shared local-first publishing studio with first-class `WEB`, `BOOK`, and `JOURNAL` modes. Its governing interaction model is direct-on-publication: the visible publication surface is part of the source of truth, and the same canonical project state should drive editing, preview, revision and export.

Classification: `ACTIVE_PARALLEL / CANONICAL_IMPLEMENTATION_DIRECTION`.

This is materially stronger than a loose design-editor idea, but the architecture itself explicitly lists completion gates. No evidence in this bounded batch proves those gates as a whole. Therefore it must not be promoted to `VERIFIED_COMPLETE`.

### 2. Protected authorship is a governing invariant

The product direction separates `content`, `provenance`, `presentation`, and `output`; AI collaboration is explicit and may suggest/proofread/research/translate/design, but protected human text may not be silently overwritten. Revision safety, Author Lock, deterministic same-source output and recoverability are product requirements, not optional polish.

Classification: `CORE_PRODUCT_GUARDRAIL / ACTIVE_IMPLEMENTATION_REQUIREMENT`.

### 3. Dore / 多寫 Mac program is a commercial destination, not release readiness

The newly added Mac program establishes a real intended destination: a local-first macOS publishing application, provisionally named `Dore / 多寫`, with eventual Mac App Store distribution. It also establishes commerce/product-learning as a resident Doré capability family.

Classification: `DISCOVERY / CANONICAL_PRODUCT_DIRECTION`.

The document itself says naming remains provisional and requires trademark/App Store/market validation; business model remains deliberately unresolved; productization, security/privacy, sandboxing, signing/notarization, payments, market validation and release evidence remain future gates. Therefore current prototype/editor work must not be described as commercially ready.

### 4. The two directions are linked but should remain separately evidence-gated

`Doré Design Publishing Studio` is the product/engineering surface. `Dore / 多寫` is the commercial packaging/distribution program. The latter depends on product truth from the former and must not destabilize current editor engineering.

Current sequence retained from the program:

`finish current editor engineering → canonicalize/verify → real Book 02 use → productization architecture → market discovery → brand/logo/manual → beta/business validation → App Store submission → launch/learning loop`

Commercial research may run read-only/in parallel, but it is not authority to skip product-truth gates.

### 5. Relationship to Westside visual learning

The publishing editor is a legitimate application surface for Doré's accumulated design-system knowledge, Storybook learning, Brand/VI/CI research, typography, publication templates, art direction and future purpose-built visual assets. This does not by itself complete `VIS-GRAMMAR`; the visual grammar still requires its own purpose-drawn asset library and verification gates.

### 6. No blocker or completion token

No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition is established by this batch. No P01 source/runtime/deployment/binding/audio/transcription state was changed.

## Canonical disposition

- `DORE-DESIGN-PUBLISHING`: `ACTIVE_PARALLEL / CANONICAL_IMPLEMENTATION_DIRECTION`.
- `DORE-MAC`: `DISCOVERY / CANONICAL_PRODUCT_DIRECTION`.
- `Author Lock / provenance / recoverability / same-source output`: `CORE_PRODUCT_GUARDRAILS`.
- Commercial-ready / App-Store-ready claim: `NOT_PROVEN`.
- Product name `Dore / 多寫`: `PROVISIONAL`.
- Sweep 01: remains `ACTIVE_PARALLEL`.

## Next evidence gates

For Doré Design Publishing Studio, persist a bounded real-product acceptance proving at minimum direct-on-book writing, protected-author behavior, revision/recovery, deterministic same-source preview/export, and one actual sustained Book 02 use path without production-site mutation.

For Dore / 多寫, keep market/commercial research evidence-gated and do not promote beyond discovery until product truth and productization architecture are demonstrated.