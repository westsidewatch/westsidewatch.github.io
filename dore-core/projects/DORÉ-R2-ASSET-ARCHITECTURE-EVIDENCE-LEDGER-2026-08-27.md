# DORÉ R2 ASSET ARCHITECTURE EVIDENCE LEDGER — 2026-08-27

Status: ACTIVE_EVIDENCE_LEDGER
Sweep: `MEMORY-CONSOLIDATION-SWEEP-01`
Source family: top-level Doré architecture / R2 asset placement

## Bounded evidence reviewed

- `dore-core/CLOUDFLARE-R2-ASSET-ARCHITECTURE-v0.1.md`;
- canonical `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`;
- already-reconciled production evidence for ONE Priority-A private-R2 delivery and Join/Priority-B site-media cutover;
- `dore-core/projects/DORÉ-CLOUDFLARE-STRUCTURED-RUNTIME-EVIDENCE-LEDGER-2026-08-26.md` for the adjacent structured-data placement boundary.

## Current evidence judgment

### 1. The R2 document is current architecture doctrine, not one monolithic completion milestone

The document defines a durable hybrid placement model:

- GitHub for institution memory, source, policy, schemas and code-coupled/version-sensitive assets;
- R2 for growing editorial/media binaries and reusable masters;
- D1 for structured registries/relationships/operational state;
- Workers/Pages Functions as bounded capability gateways;
- one authoritative binary backend per asset, with stable IDs, hashes, provenance/rights and explicit migration mapping.

Classification: `CORE/CONTINUOUS` architecture doctrine with partially verified implementation history.

The architecture should not be marked `VERIFIED_COMPLETE` as a whole. Its strongest claims are principles that continue to govern new work and must be re-proved in each migration/consumer path.

### 2. Several implementation slices are already genuinely verified

The canonical Master Register records two bounded production milestones consistent with this architecture:

- ONE Priority-A media: 7/7 migrated assets delivered through asset-code/D1/R2 with hash verification and active-reference cutover before rollback binaries were removed;
- Join/Priority-B site media: the background and WeChat QR are actively delivered through the verified five-asset private-R2 cutover.

These are evidence that the hybrid architecture is not merely aspirational. They verify particular consumer/migration slices, not universal asset-registry coverage, global lifecycle enforcement or all future media placement.

### 3. Adjacent structured-data placement confirms the lifecycle-over-file-size rule

The separate Cloudflare structured-runtime evidence ledger records a `VERIFIED_COMPLETE` placement audit that deliberately kept deterministic browser indexes on Pages instead of moving them to R2/D1 simply because they were large. This materially supports the R2 architecture's governing decision rule: storage follows lifecycle, mutability and access semantics rather than file extension or size alone.

### 4. Documentation provenance drift exists but is low-risk

The repository filename is `CLOUDFLARE-R2-ASSET-ARCHITECTURE-v0.1.md`, while the document title says `Cloudflare R2 / Doré Asset Architecture v0.2`.

Classification: documentation/provenance maintenance, not a runtime blocker and not evidence that the architecture itself is invalid. Future editing should reconcile filename/version identity or explicitly record why the v0.1 path contains the v0.2 text so later sweeps do not infer two separate architectures.

### 5. Historical free-tier figures are planning evidence, not timeless policy

The document records Cloudflare allowance figures as the premise at design time. Those numbers should be treated as dated planning evidence. Any future financial/capacity decision must revalidate current provider pricing/allowances rather than treating the 2026-08-24 snapshot as permanent architecture truth.

This does not change the free-first principle or the storage-pressure doctrine.

## Missing-evidence / future proof boundary

No new top-level missing-evidence identifier is necessary from this batch because the open work is distributed across existing active product/runtime lines rather than one declared global completion token.

The smallest useful future architecture-level proof, if a global asset milestone is ever proposed, would be a cross-product fixture showing:

1. stable `asset_id` resolution across at least two consumers;
2. authoritative-backend + content-hash verification;
3. rights/provenance fields preserved;
4. dedupe/reuse rather than duplicate production masters;
5. migration/rollback mapping;
6. one regenerable/temporary cleanup case that cannot delete a permanent/unique original;
7. current cost/capacity assumptions explicitly revalidated.

Until such a milestone is named and tested, retain the architecture as governing doctrine plus bounded verified migrations, not as a single completed project.

## Completed-work / revisit / supersession judgment

- R2 asset architecture doctrine: `CORE/CONTINUOUS`.
- ONE Priority-A and Join/Priority-B R2 cutovers: retain their existing bounded `VERIFIED_COMPLETE` historical interpretations; do not duplicate them as a new completion entry.
- filename/title version mismatch: low-priority documentation maintenance.
- no new `COMPLETED_REVISIT_CANDIDATE`, `SUPERSEDED`, or `RETIRED` item is justified.
- no Master Register row/status change is warranted; the existing ONE/JOIN/RUNTIME/CORE interpretations already carry the strongest justified operational state.

## P01 protection

This reconciliation changed no P01 code, runtime state, deployment, binding, credential, subtitle ordering or blocker state. The existing subtitle critical-path environment dependency is unchanged.
