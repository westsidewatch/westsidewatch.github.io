# DORÉ System Relationship Map v1

Status: CANONICAL RELATIONSHIP BASELINE

## 1. One sentence

**DORÉ Core is the persistent intelligence; products are bounded consumers and real-world training environments; projects are capability-growth programs; runtimes/providers are replaceable execution substrates.**

This is the system boundary that prevents Search, Design, Image, ONE, Multiwrite or any future surface from quietly becoming a second Doré.

## 2. Four-layer model

### Layer A — DORÉ Core
Owns identity, durable memory, knowledge, research discipline, provenance, judgment, capability routing, permissions, learning, verification and cross-product semantics.

Core is not a UI and is not a model. A local LLM, search engine, renderer or cloud service is a provider. Providers can be replaced without changing Doré identity.

### Layer B — Shared faculties/capabilities
Examples: Biblical World, Search/Retrieval, Editor, Librarian, Visual Director, Image, Translation, Proofreading, Asset Steward, Publication Verification, A2A execution.

A capability graduates toward Core when two or more products need the same semantics, or when provenance/permissions/verification must be uniform.

### Layer C — Products
Products own their specific user experience, document/state schema and product acceptance. They consume Core faculties rather than duplicating them.

- **Doré Search** — conversation/retrieval/control surface. It is the main human entry into Doré, not the brain.
- **ONE** — Scripture exploration product consuming Biblical Intelligence, maps, people, chronology, original language, Search, Design/Image and Dawn Library.
- **Doré Design** — structured visual production tool. It owns editable design documents and interaction, while brand memory, visual judgment and verification remain Doré faculties.
- **Doré Image** — image-generation/asset capability. It owns renderer adaptation, image manifests and visual evidence, but it is not a separate creative identity.
- **多寫 / Multiwrite** — writing and book-production product consuming Editor, Research, Search, Dawn Library, Design and Image.
- **Journal** — editorial publication consuming Research, Theology, Editor, Visual, ONE and Dawn Library.
- **黎明書局 / Dawn Library** — governed resource/knowledge product and Doré's Librarian training domain, not a bookmark page.
- **A Day / Daily Bread** — outreach/distribution product consuming theological moment, Dawn Library, editorial judgment, Image and analytics.
- **Westside main site** — public distribution surface consuming Journal, ONE, Library, Search and A Day.
- **Church / Ministry** — human-authority domain where Doré provides bounded Scripture, translation and proofreading support.
- **Books / Publishing** — project family delivered primarily through Multiwrite + Search + Design + Image + Library.

### Layer D — Runtimes, control planes and providers
These execute capability but do not own intelligence.

- `127.0.0.1:8788` — Doré Local memory/reasoning node.
- Unix Domain Socket + launchd — local A2A nervous system.
- GitHub Issue event + self-hosted runner — authenticated external receiver for ChatGPT-to-Mac bounded execution.
- `127.0.0.1:4310` — Doré Design structured workspace runtime.
- `127.0.0.1:8790` — Doré Image Local API; local renderer sits behind it.
- Ollama / local models — replaceable inference providers.
- ComfyUI / future local image engines — replaceable renderer providers.
- GitHub — versioned institutional source of truth.
- Cloudflare — optional public runtime/media infrastructure, never Doré intelligence.

## 3. Projects are not products

A project exists to grow or validate a reusable capability. A product exists to serve a stable user task.

### Bible Intelligence Loop
Grows cross-reference, original-language, person, place, chronology, topic and historical-study intelligence. Primary consumers: Search, ONE, Multiwrite and Dawn Library.

### A2A Growing Protocol
Grows the relationship/control plane between ChatGPT and Doré: capability discovery, lifecycle, durable execution, observability, failure memory and recovery. Consumer: every bounded autonomous action.

### Storybook Learning Loop
Research/training loop that digests open resources, patterns and methods. It feeds Core or shared faculties. It must not become another product-specific brain.

### Dawn Library Genesis
A real product-development project and also Librarian/Steward apprenticeship. Its reusable stewardship methods should move upward into Core; its collection/UI remain product-owned.

### Visual / Design / Image learning
Design research, visual grammar, motion and image-engine research are one shared visual-learning stream. Design and Image are separate production surfaces but must share Doré visual memory, provenance, brand grammar and evaluation semantics.

## 4. Direction of learning

The relationship is bidirectional:

`Core capability -> Product use -> Real evidence/problem -> Learning project -> Core upgrade`

Examples:

- ONE exposes a weak place/journey relation -> Bible Intelligence learns/fixes graph semantics -> Search and Multiwrite improve too.
- Multiwrite exposes a weak editorial operation -> Editor faculty learns it -> Journal can later consume the same semantic operation.
- Design exposes interaction or visual-judgment failure -> visual learning distills the lesson -> Image, Journal, ONE and A Day benefit.
- A2A execution fails silently -> failure evidence upgrades the control plane -> all product deployment/automation becomes more reliable.

A lesson should not stay trapped inside the product where it was discovered if its semantics are general.

## 5. What must stay product-owned

To stop Core from becoming a giant monolith, these normally stay outside Core:

- page/component interaction specifics;
- product document schemas that have no cross-product semantic value;
- route/layout details;
- one-off visual compositions;
- product-specific publication templates;
- local UI state;
- temporary experiments.

Only distilled reusable semantics move upward.

## 6. Current structural problems exposed by the audit

### Runtime worktree divergence
Several local services were historically installed from `~/westsidewatch.github.io`, while production A2A now executes from the self-hosted runner checkout. This can leave Search/Image/Design using different code generations. All resident installers must resolve the canonical checkout at installation time and write that path into launchd.

### Shared capability duplication
Search, Design and Image have accumulated direct point-to-point bridges. They should converge on a small Core capability registry and bounded semantic calls instead of each product inventing its own private control semantics.

### Memory fragmentation risk
Product history, design evidence, research evidence and autonomous-learning evidence exist in different stores/files. Product-specific state is valid, but promotion/supersession/provenance semantics should be common Core rules.

### Acceptance fragmentation
A source commit, resident health, transport PASS, capability execution and human-visible product quality are different truth levels. Every product must report them separately.

### Project/product naming blur
Storybook, Bible Intelligence, A2A and visual research are learning/capability projects; ONE, Search, Design, Multiwrite, Journal and Dawn Library are products. Keeping that distinction explicit will reduce duplicate architecture.

## 7. Canonical dependency direction

```text
Human goals / Church authority
          |
          v
      DORÉ Core
 memory | knowledge | research | judgment | permissions | verification
          |
          +---------------- shared faculties ----------------+
          |        |          |         |        |           |
       Search     ONE       Editor    Visual   Librarian     A2A
          |        |          |         |        |           |
          +---- products / public surfaces / projects -------+
                     |
                     v
               runtime adapters
       local API / Design / Image / GitHub / Cloudflare
                     |
                     v
               replaceable providers
         LLM / renderer / search / storage / APIs
```

Dependency should normally point downward. A provider must not define Doré identity; a product must not redefine Core memory/judgment; a project must not fork a duplicate product runtime merely to learn.

## 8. Immediate reconciliation program

1. **Canonical runtime root** — every local resident resolves and persists the actual production checkout; eliminate stale hard-coded worktrees.
2. **Capability registry** — expose Search Local, Design, Image and later ONE/Multiwrite as bounded named capabilities through one registry.
3. **Shared acceptance vocabulary** — `source_committed`, `deployed`, `resident_healthy`, `capability_pass`, `product_pass`, `human_visual_pass`.
4. **Shared evidence envelope** — all cross-product learning records source, scope, truth state, provenance, consumer and promotion status.
5. **No second brains** — audit every product for copied prompts/memory/research logic that should be a Core faculty.
6. **Consumer declarations** — each shared capability records which products actually consume it; unused abstractions do not graduate.
7. **Learning return path** — every product project specifies what lessons can be promoted back into Core.
8. **Retire obsolete bridges** only after new paths are proven, not by documentation alone.

## 9. Acceptance for this relationship baseline

This document is architecture, not proof that every relationship is already implemented. Implementation evidence must come from runtime/code/tests.

The machine-readable companion is:

`dore-core/runtime/product-registry.v1.json`

Future product creation should update that registry instead of inventing an isolated Doré architecture.
