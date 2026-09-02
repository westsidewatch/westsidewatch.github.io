# DORÉ JOIN PORTAL EVIDENCE LEDGER — 2026-09-02

Status: SWEEP-01 BOUNDED RECONCILIATION
Product: `/join/`
Canonical linkage: `DORÉ-MASTER-WORK-REGISTER.md` → `MEM-SWEEP-01` (Join / Priority-B site-media already accounted for)
P01 impact: none

## Evidence reviewed

- current production source: `join/index.html`;
- current canonical Master Work Register interpretation for Join/Priority-B media placement and Church information surfaces;
- existing Sweep-01 rule that product-shell existence, storage migration, and operational-information verification are separate evidence layers.

## Current implementation facts

`join/index.html` is not a placeholder shell. It is a live, reader-facing ministry portal with:

- primary links to Doré Bible Search, ONE and Westside Watch;
- an inline Doré search entry;
- Westside Watch identity and Romans 13:12 watch/dawn framing;
- a hard-coded gathering schedule;
- WeChat join QR delivered through the Doré site-asset endpoint using `SITE-WECHAT-QR`;
- a background delivered through the same asset endpoint using `SITE-BACKGROUND`;
- Zoom meeting information;
- named ministry contacts, telephone links and the Westside Watch email address;
- a church-name image and link to `/church/`.

The current source therefore proves two different things that must not be conflated:

1. **Portal implementation exists** — the Join surface is materially implemented and integrated with Search/ONE/Main.
2. **Operational ministry data are embedded in code** — schedules, Zoom credentials and contact details are direct page content rather than a separately verified operational-data source.

## Classification

### Join portal implementation

Current classification: `MAINTENANCE` as a live product surface.

The existence of the implemented portal is not itself a new milestone requiring a new active workstream. The canonical Master Register already accounts for Join under the product-history sweep and Priority-B site-media history.

### Priority-B Join site-media placement

Current classification: retain historical bounded completion already represented by the canonical Cloudflare migration interpretation.

The current source uses asset-code endpoints for `SITE-BACKGROUND` and `SITE-WECHAT-QR`, consistent with the already-closed site-media migration/cutover history. No newer contrary evidence was found in this bounded batch.

### Operational-information governance

Current classification: `MAINTENANCE / REVISIT CANDIDATE`, not `BLOCKED`.

Reason: the Join portal currently carries time-sensitive ministry information directly in HTML. The separate Church information-surface reconciliation found that Church route shells should not be treated as verified operational truth merely because routes exist. Join is stronger than those shells because it contains actual values, but source presence still does not prove that the values are current, authorized or synchronized with the church's governing information source.

This is a governance/synchronization risk rather than evidence that the live Join page is broken.

## Retrospective evaluation

### Original objective

Provide a direct, low-friction public joining/meeting/contact portal connecting Westside Watch readers to Search, ONE, the local church and real community participation.

### Completion evidence

A materially implemented `join/index.html` exists with working structural links, search entry, meeting/contact sections and asset-code-backed background/QR references.

### Current quality

Strong as a compact ministry doorway and cross-product portal. The page is structurally simple and clear. Its main present weakness is not layout but data governance: time-sensitive operational details are hard-coded into the presentation layer.

### Durable learning

A ministry portal should distinguish:

`stable brand/editorial content` from `time-sensitive operational truth`.

Storage/cutover completion for media assets does not prove operational-information freshness.

### Weakness / debt

Schedule, Zoom and contact data can drift independently from `/church/`, future calendar sources or ministry-authorized updates. Duplicate operational truth across pages increases stale-information risk.

### Revisit trigger

Reopen when any of the following occurs:

- church schedule/contact/Zoom information changes;
- a canonical church information source/API/data file is introduced;
- Join is redesigned under Brand V1;
- a stale-value discrepancy is observed between Join and another official surface.

### Desired future outcome

Keep the Join presentation lightweight, but source time-sensitive ministry information from one canonical, explicitly verified operational-data source shared with Church surfaces where practical. Preserve the existing asset-code delivery pattern for the migrated media unless newer integrity/runtime evidence contradicts it.

## Sweep decision

No Master Register status change is warranted in this batch: its existing `MEM-SWEEP-01` statement that Join/Priority-B media history has been reconciled remains correct, and the broader Church-information evidence boundary already prevents route/source existence from being mistaken for verified freshness.

The useful new durable finding is the narrower **operational-data synchronization revisit trigger** for Join. This should be carried into future Brand V1 or Church-information work, not opened as a competing active project and not allowed to interrupt P01.
