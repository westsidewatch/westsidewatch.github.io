# Doré Structured Data Runtime Audit — 2026-08-24

Status: **COMPLETE / PASS**

## Scope
Audit the structured runtime data used by Doré Bible Search / Doré Brain after the GitHub + Cloudflare infrastructure reorganization. This milestone is placement/governance only: no destructive cutover is permitted unless it improves runtime without breaking the already-working search product.

## Production browser indexes

| Dataset | Current size | Current consumer | Placement decision |
|---|---:|---|---|
| `static/dore/search-index.json` | 10,235,111 B | `static/dore/dore-search.js` | **KEEP on Pages for current search runtime** |
| `static/dore/original-index.json` | 10,184,152 B | lazy-loaded by `static/dore/dore-search.js` | **KEEP on Pages for current search runtime** |
| `static/dore/entity-index.json` | 2,860,537 B | lazy-loaded by `static/dore/dore-entity-search.js` | **KEEP on Pages for current search runtime** |
| `static/dore/brain/knowledge-index.json` | 19,822 B | Doré Brain bridge | **KEEP on GitHub/Pages** |
| `static/dore/status/current.json` | 5,196 B | Doré self-status route | **KEEP on GitHub/Pages** |
| `data/resources.json` | 49,489 B | Liming Library master | **KEEP on GitHub** |
| `data/volumes/vol-00.yaml` | 7,045 B | Journal editorial structure | **KEEP on GitHub** |

### Reason
The three large `/dore/*.json` files are not media assets. They are deterministic, versioned browser indexes generated from the corpus and are directly fetched by the currently-working search UI. Moving them to R2 merely because they are large would add an API/delivery dependency without reducing application complexity. D1 is also the wrong first destination for whole 10 MB browser snapshots: it is better reserved for queryable mutable metadata/state, not as a blob substitute.

Therefore this milestone makes **no destructive move of the active browser indexes**. The current browser contract remains stable while the next milestone consolidates the search service.

## Research / generated datasets

The repository also contains large generated research artifacts and inventories, including:

- `reports/DORÉ-CROSS-WITNESS-CORRESPONDENCE-MAP.json` — 888,938 B
- `reports/DORÉ-CROSS-WITNESS-DIFFERENCE-CAUSES.json` — 2,676,476 B
- `reports/DORÉ-CROSS-WITNESS-EXCEPTION-TRIAGE.json` — 900,222 B
- `reports/inventories/*.json` — roughly 0.2–0.82 MB each

Decision: **keep these in GitHub as reproducible research evidence for now**. They are not public browser hot-path data. If their history becomes a repository-size burden, a later archival policy may place immutable generated snapshots in private R2 while retaining compact manifests/checksums in GitHub. That is an archival optimization, not a production runtime requirement.

## D1 role after audit

D1 remains the home for data that benefits from structured queries or mutation:

- Asset Registry metadata
- Doré sensory / persistent operational state
- future service-layer mutable indexes, caches, job state, and relational metadata when justified

D1 is **not** designated as a wholesale replacement for versioned browser JSON snapshots.

## R2 role after audit

R2 remains the home for independently addressable large binary/content objects:

- canonical ONE media
- site media already cut over
- future Journal media
- future Liming Library media
- optional future cold archives of generated research snapshots, only if repository pressure justifies it

R2 is **not** designated as the default home for every large JSON file.

## Architecture boundary

The audited boundary is now:

`GitHub source + deterministic generators -> Pages browser indexes -> Doré browser search`

`D1 -> mutable/queryable registry + operational state`

`R2 -> large independently-addressable media/content objects`

This preserves the existing working Bible Search while keeping the Cloudflare services in roles they are actually good at.

## Regression protection

The next milestone MUST preserve:

1. direct verse reference lookup;
2. chapter and verse-range lookup;
3. multi-reference input;
4. exact and fuzzy Chinese/English scripture search;
5. original-language lookup and translated-to-original behavior;
6. entity context lookup;
7. Doré Brain/self-status routing;
8. graceful degradation if an optional lazy index is unavailable.

## Result

**PASS.** Placement decisions are complete. No active search dataset is moved merely for storage aesthetics. The next milestone is **Search Runtime Consolidation**, where browser/service boundaries and regression gates can be improved deliberately without conflating that work with storage migration.
