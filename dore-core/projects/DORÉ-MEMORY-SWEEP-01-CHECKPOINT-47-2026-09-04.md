# DORÉ MEMORY CONSOLIDATION SWEEP 01 — CHECKPOINT 47

Date: 2026-09-04
Status: BOUNDED_RECONCILIATION_COMPLETE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md` + `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-DORE-DESIGN-MAC-2026-09-04.md`
P01 impact: NONE

## Bounded evidence reviewed

- current `static/multiwrite/index.html`;
- current `static/multiwrite/styles.css` lineage through `a498c88d2a26ac542168032a90e9c93dca6c02d3`;
- product-identity correction commit `d31859523ed4c1219e8655ca46a0cd88a0c088af`;
- product-home/library implementation lineage `bab14566a2e197bbcfffa300971523c6c6741243`, `4d21df0a597f6d6d3aaa613294fa9e56094441c3`, `49e755cef52ae81af8c8f40019600d66e3834d3b`, `190acf7223437d81aa49997f1011464d97672e61`, `acda406e7dec536c8b28dc8e98d096d631f23082`, and `a498c88d2a26ac542168032a90e9c93dca6c02d3`;
- Checkpoints 44–46 and the current Doré Design / Mac / Books canonical addendum.

## Reconciliation findings

1. **Multiwrite has now materialized a distinct product-home/library surface, not only an editor/import/export workbench.** The current homepage establishes a product thesis around writing, reading and book-making in one place; provides a separate `我的書` library; and preserves the import-old-draft path as a secondary entry rather than making import itself the product identity. This is legitimate `IMPLEMENTED_ALPHA` product-surface evidence under `DORE-DESIGN-PUBLISHING`.
2. **The current browser-alpha identity is now explicitly `DORÉ · 多寫`.** The current document title, brand lockup, footer and product copy all use `多寫`; the current slogan is `讓所寫的，成為書。 / Write on. Make it a book.`. Earlier intermediate variants such as `DORÉ · WRITING`, `多寫 · WRITE`, and the temporary slogan `使用這個編輯器，就是在你的書上直接寫。 / Write on the book itself.` are historical design iterations and are `SUPERSEDED` for the present browser product surface.
3. **This does not settle the commercial Mac naming question.** The canonical addendum correctly keeps `Dore / 多寫` commercial naming as provisional for trademark/market validation. The evidence supports a current alpha product identity, not a market-validated final commercial brand.
4. **The homepage now has a clearer publication-first information architecture.** Current sections distinguish product thesis, three core actions (`帶回來 / 繼續寫 / 成書`), library, import, Doré family links and product signature. This reduces the earlier risk that the browser alpha would read as a file importer with book features added later.
5. **Visual convergence with the DORÉ family is implementation evidence, not visual-quality completion.** The current surface deliberately reuses Cormorant Garamond + Noto Serif TC, gold/ink/paper vocabulary, DORÉ signature and Westside/DORÉ navigation. No persisted rendered inspection, accessibility/performance acceptance, responsive artifact review or user-approved aesthetic acceptance was found in this bounded batch. It therefore does not satisfy the separately gated `VIS-GRAMMAR` or D4 visual-readback contract.
6. **The current product homepage does not supersede Multiwrite's source-preservation/export evidence boundaries.** Import/source protection, working drafts, deterministic semantic exports, DOCX/PDF artifact fidelity, Author Lock/revision/recovery and packaged-Mac/offline behavior remain governed by Checkpoints 44–46 and their evidence ledgers.
7. **No canonical status change is warranted.** `DORE-DESIGN-PUBLISHING` remains `ACTIVE_PARALLEL / CANONICAL_IMPLEMENTATION_DIRECTION; MULTIWRITE IMPLEMENTED_ALPHA`; `DORE-MAC` remains `DISCOVERY / CANONICAL_PRODUCT_DIRECTION`. This checkpoint adds product-history and supersession provenance without promoting either workstream.
8. No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition was found. P01 runtime/deployment/bindings/credentials/audio-transcription dependency/source order were not modified.

## Durable supersession note

For current browser-product identity, treat these as historical-only unless later deliberately restored:

- `DORÉ · WRITING` product overline;
- `多寫 · WRITE` hybrid name;
- `使用這個編輯器，就是在你的書上直接寫。 / Write on the book itself.` as the primary homepage slogan.

Current alpha identity evidence is:

- product: `DORÉ · 多寫`;
- slogan: `讓所寫的，成為書。 / Write on. Make it a book.`;
- core product thesis: writing, reading and book-making occur on the same book surface;
- primary collection surface: `我的書`;
- import-old-draft: retained as a first-class workflow, but no longer the whole product's visual identity.

## Smallest next evidence

Persist one rendered product-home acceptance packet across desktop + mobile that verifies:

1. current `DORÉ · 多寫` identity and slogan are consistently rendered;
2. `我的書` is visibly the primary collection surface and import remains discoverable without dominating the product;
3. real book-card → editor → save/reload → export flow preserves source/draft identity;
4. typography, contrast, focus/navigation and mobile layout remain usable;
5. any visual corrections are evidence-driven and persisted before claiming product-home visual acceptance.

Do not infer commercial-name validation, full Visual Grammar completion, Mac productization or publication-quality export from this homepage milestone.

## Sweep disposition

Sweep 01 remains `ACTIVE_PARALLEL`. This bounded batch records a newly materialized product-surface milestone and retires several transient identity variants from current-state interpretation. It does not justify `VERIFIED_COMPLETE` and establishes no new blocker.