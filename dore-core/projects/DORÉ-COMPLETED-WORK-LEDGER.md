# DORÉ COMPLETED WORK LEDGER

Status: ACTIVE / SWEEP-01 OUTPUT
Established: 2026-08-25
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

This ledger records substantial work that reached a defensible historical completion milestone. Historical completion is separated from current quality judgment; entries may later be promoted to revisit candidates when Doré's capabilities or the ecosystem change.

## CW-001 — Sensory-loop consolidation / D1 reconciliation milestone

**Current classification:** `VERIFIED_COMPLETE` for the repair/consolidation milestone; the sensory system itself remains `CORE/CONTINUOUS` stewardship.

**Original objective**
Restore a reliable sensory learning loop in which an observed reader/query signal can be claimed, researched, consolidated into a durable brain node, and reconciled back to persistent state without duplicate re-processing.

**Completion evidence**
- `dore-core/memory/sensory-active.json` records signal `5cf2c608-e66f-4176-a3f8-b3284819158a` for `馬利亞有幾位?` as `CONSOLIDATED`, linked to brain node `research.nt.mary-count`, with a consolidation timestamp.
- `dore-core/memory/sensory-seed-diagnostic.json` records HTTP 200, `state=CONSOLIDATED`, `deduplicated=true`, and `schema_reconciled=true`.
- `dore-core/memory/sensory-heartbeat-diagnostic.json` records `ok=true` and `reconciled_consolidated=1` against the deployed Pages base.
- `dore-core/memory/actions-probe-diagnostic.json` records a successful GitHub Actions probe (`ok=true`, run `32804448339`).
- Commit `5adeedd82ed45a4031d6a6e335645b4dd7c1b76f` explicitly repaired reconciliation of consolidated sensory state back to D1; subsequent persisted heartbeat evidence continued through commit `c15eea6f901776392036dc15c180483d00aad71f` on 2026-08-25.

**Current quality judgment**
Strong enough to accept the historical repair milestone as complete: there is both state evidence and repeated deployed heartbeat evidence, not merely a code commit. However, the evidence corpus is still narrow: the durable active-memory sample presently exposes one consolidated signal, so this does not by itself prove broad-topic robustness, high-volume operation, or long-horizon learning quality.

**What Doré learned / retained**
- distinguish runtime state from durable learned state;
- reconcile consolidated knowledge back into persistent D1 state;
- make sensory processing idempotent/deduplicated;
- persist heartbeat and external Actions probe evidence rather than treating implementation as verification;
- connect a raw reader signal to a durable research/brain node.

**Weaknesses / debt**
- current evidence demonstrates correctness on a very small visible sample;
- heartbeat success does not prove quality of the research answer itself;
- no current ledger evidence yet demonstrates stress/volume behavior, heterogeneous signal classes, or systematic false-positive/duplicate rates;
- repeated diagnostic commits create useful provenance but may later deserve compaction/indexing so operational evidence does not obscure higher-value project history.

**Revisit trigger**
Reopen the milestone if sensory processing begins dropping/duplicating signals, if schema changes introduce reconciliation drift, if Doré adds materially new signal types, or when a broader learning-quality benchmark is available.

**Disposition**
Keep the repair milestone closed. Continue the sensory loop as core stewardship and add broader evaluation when it becomes high leverage; do not reopen merely because the system continues running.

## CW-002 — Biblical World foundation graduation

**Current classification:** `VERIFIED_COMPLETE` for the bounded Biblical World foundation milestone; later historical/textual/theological education remains open-ended.

**Original objective**
Establish a defensible foundational model of the biblical world across entities, geography, chronology, polity, institutions and evidence-boundary discipline, with blind checks that prevent unsupported certainty from being mistaken for evidence.

**Completion evidence**
- `reports/DORÉ-BIBLICAL-WORLD-GRADUATION.json` records `status=PASS` and `milestone=BIBLICAL_WORLD_COMPLETE`.
- The same report records BW-1 through BW-6 all `PASS` and explicit blind-boundary checks for geography, chronology, polity, institutions and evidence wording.
- It records canon-spanning period/polity coverage and social-world domain coverage, with 9 macro periods, 6 imperial contexts and 9 institutions represented in the foundation.

**Current quality judgment**
Strong enough for the declared foundation milestone. The evidence is explicit, machine-readable and bounded. It should not be inflated into general researcher graduation or exhaustive historical mastery; the report itself states that later research education may refine scholarly reconstructions.

**What Doré learned / retained**
- keep entity/place/time/polity/institution claims tied to evidence boundaries;
- separate a stable biblical-world foundation from later interpretive or scholarly refinement;
- require blind transfer checks rather than declaring competence from corpus ingestion alone;
- maintain canon-spanning contextual registries reusable by Search, ONE, Library, subtitle correction and visual research.

**Weaknesses / debt**
- foundation coverage counts do not alone measure depth or scholarly disagreement handling;
- no evidence in this batch promotes this milestone to full Researcher graduation;
- future corpus/source upgrades may expose reconstructions that should be revised without invalidating the original foundation completion.

**Revisit trigger**
Re-evaluate when the historical-source corpus materially expands, when disputed-location/chronology methodology changes, or when a downstream product exposes a systematic contextual weakness.

**Disposition**
Keep the foundation milestone closed; retain as reusable infrastructure and place only the refinement question on a low-priority revisit watchlist.

## CW-003 — Language Core full-parity migration milestone

**Current classification:** `VERIFIED_COMPLETE` for the declared parity migration/checkpoint; language research capability itself remains `CORE/CONTINUOUS`.

**Original objective**
Move the biblical language corpus into the unified Language Core without losing legacy units, ordering, references, surface/normalized text, language identity or analyses.

**Completion evidence**
- `reports/DORÉ-LANGUAGE-CORE-PARITY.json` records `status=PASS`.
- It records all `66` books checked.
- It records exact parity between `legacy_units=444339` and `language_core_units=444339` with `mismatched_books=[]`.
- The declared criterion is `surface+normalized+language+reference+order+analyses parity`.
- `.github/workflows/dore-foundation-tests.yml` includes a dedicated universal Language Core parity step and final enforcement that requires the parity step to succeed together with the other foundation checks.

**Current quality judgment**
This is strong evidence that the migration preserved the declared data envelope at the recorded checkpoint. It is not evidence that every analysis attached to those units is linguistically correct, nor that later source refreshes cannot introduce drift.

**What Doré learned / retained**
- migrations require structural and semantic-envelope parity, not merely row-count similarity;
- book-level mismatch detection should fail closed rather than silently normalize away differences;
- full-canon language infrastructure can be regression-tested as a reusable substrate for lexical research, cross-witness alignment, Search and subtitle/scripture alignment.

**Weaknesses / debt**
- parity verifies preservation, not scholarly correctness of every analysis;
- any later corpus ingestion or schema evolution can invalidate the historical parity snapshot unless regression checks continue to run;
- the foundation workflow uses `continue-on-error` for intermediate steps and relies on a final enforcement step, so workflow interpretation must consider the final job result rather than an intermediate step alone.

**Revisit trigger**
Run the same parity criterion whenever the corpus, normalization rules, reference mapping or Language Core schema materially changes.

**Disposition**
Keep the migration milestone closed. Treat future parity execution as maintenance/regression protection, not as reopening the original migration.