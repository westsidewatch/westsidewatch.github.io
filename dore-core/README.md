# DORÉ Core

**Status:** `DORÉ / Foundation + active brand apprenticeship`

Doré Core is Westside Watch's persistent Scripture/church intelligence, learning, resource and governed brand-operating layer.

Doré is not a chat UI, autonomous preacher, giant prompt, single model or product-specific tool. It is one persistent intelligence with bounded faculties and adapters. Its foundation remains rigorous Scripture/theology/history/language research, evidence discipline and provenance-aware memory; its apprenticeship now also occurs through real Westside Watch work.

## Formation sequence

`Architecture -> Core Skeleton -> Foundation Education -> Research Benchmark -> Researcher -> Brand Apprenticeship -> Companion Learning -> Bounded Automation`

These stages may overlap where safeguards are explicit. Doré must never claim graduation merely because it has begun useful product work.

## Repository map and architecture namespaces

The current repository is not a literal one-folder-per-architecture-layer implementation. The durable source families currently include `architecture/`, `benchmarks/`, `cloudflare/`, `constitution/`, `evidence/`, `knowledge/`, `memory/`, `projects/`, `readers/`, `reflex/`, `runtime/` and `tests/`, while additional executable Doré code also exists outside this hyphenated `dore-core/` tree (for example the Python package under `dore_core/`).

The following names are **architectural responsibilities**, not a claim that matching `dore-core/<name>/` directories already exist:

- **Core primitives** — context, observation, evidence, judgment and routing.
- **Knowledge** — provenance-aware durable knowledge and curriculum/corpus manifests.
- **Memory** — working memory, candidate knowledge, promotion and supersession.
- **Research** — source evaluation, retrieval, citation and research workflows.
- **Providers** — replaceable model/search/embedding/ASR/translation/image providers. Provider != Doré.
- **Roles / faculties** — Scholar, Researcher, Librarian, Steward, Editor, Visual Director, Proofreader and Interpreter.
- **Product adapters** — contracts for ONE, Westside Stories, 黎明書局, Journal, Search, Visual, church and later products.
- **Tools / permissions** — managed tool/API/MCP gateways and authority policies.
- **Benchmarks / tests** — formation, transfer and regression evidence.

Architecture documents describe intended boundaries; only repository/runtime/test evidence proves that a particular boundary is implemented. Missing literal directories must not be interpreted as either proof of absence of the capability or proof that the architecture is complete.

## First principle

Doré must learn correctly before it is allowed to automate broadly.

Knowledge breadth is not the definition of intelligence. Doré must preserve sources, distinguish Scripture from interpretation, represent uncertainty, compare competing evidence, understand brand/product context, verify external actions, and know when it does not know.

## Current and future brand faculties

Doré is being formed as one intelligence capable of serving across the brand as:

1. Researcher / biblical-historical-theological scholar.
2. Librarian and primary online resource steward for 黎明書局, the brand resource station.
3. Journal editor able to understand columns, interludes, Daily Devotional Sharing and cross-surface reuse.
4. Visual production center and visual-asset librarian.
5. Scripture/church-aware subtitle proofreader.
6. Simultaneous interpretation and translation faculty where authorized.
7. Search / conversation interface whose retrieval tools remain downstream of understanding.
8. ONE maintainer and progressively more capable bounded developer.
9. Archivist / memory steward connecting decisions, resources, assets and provenance.
10. Content automation editor for well-specified recurring online workflows, beginning with staged Daily Devotional automation.

These are faculties of one Doré, not independent agents. Learning from one surface may inform others only when provenance and scope permit.

Human authority remains decisive for doctrine, sensitive pastoral matters, rights-uncertain publication, high-impact public statements and irreversible actions.

## Brand operating relationship

Doré should learn through and connect real brand work:

`Journal <-> ONE <-> 黎明書局 <-> Church <-> Search <-> Social <-> DORÉ`

黎明書局 is not a bookstore. It is the brand's resource station and a major Doré-led learning/management domain: resources should be inventoried, classified, provenance-aware, related to Scripture/topics/people/places, and connected to actual use in Journal, ONE, Search, teaching and ministry.

## Infrastructure responsibility

GitHub remains the versioned institutional source of truth for code, architecture, schemas, policies, tests, approved content/knowledge and decision history.

Cloudflare is the preferred runtime media/service substrate:

- **R2** — shared brand binary media / visual asset library.
- **D1 or another replaceable structured runtime store** — live asset/resource registry and operational relationships where appropriate.
- **Workers / Pages Functions** — bounded runtime capability adapters.
- **Cloudflare CDN/custom domain** — public asset delivery and caching.
- **Cloudflare Images Free transformations** — optional derivative/optimization layer; R2 remains the binary source of truth.

Doré owns meaning, provenance-aware relationships, routing, permission and verification. Cloudflare provides infrastructure; it does not become Doré's intelligence.

## Architecture sources

Historical baseline:

`static/one/engraving-studio/DORÉ-CORE-ARCHITECTURE-v0.1.md`

Current brand-operating direction (supersedes v0.1 where identity, brand roles, 黎明書局 and Cloudflare/media integration differ):

`dore-core/DORÉ-BRAND-OPERATING-ARCHITECTURE-v0.2.md`

Dated working conversations remain historical working memory and must not silently override the current architecture baseline.