# ONE — 1,189 Chapter Visual Master Inventory

Status: ACTIVE · DORÉ BASELINE LOCKED · NO IMAGE GENERATION DURING AUDIT

ONE's visual production unit is the **chapter**, not the book. The Protestant 66-book canon contains 1,189 chapters (OT 929 + NT 260). Every chapter must ultimately have one canonical artwork identity, one portrait cover composition, one horizontal illustrated-Scripture spread, and one theme verse from that chapter.

## Locked Doré baseline — 184 chapters

The first Doré allocation pass is now frozen as a protected baseline:

- `181` unique Protestant-canon chapters have a direct Doré chapter/verse assignment in the adopted Doré catalog audit.
- `3` additional chapters are covered by explicit alternate/cross-reference assignments in the adopted catalog rather than by subjective thematic reuse.
- Locked baseline: `184 / 1189` chapters.
- Remaining chapters before semantic reuse audit: `1005`.

These 184 chapter allocations are **protected historical mappings**. Later reuse analysis must not remove, overwrite, regenerate, or silently replace their canonical Doré assignment.

For a locked chapter with multiple Doré plates:

1. one representative plate is selected for the portrait cover;
2. all other directly assigned plates remain attached to that same chapter for its illustrated section;
3. each plate receives its own title/caption and Scripture reference;
4. surplus plates may be evaluated later for reuse elsewhere, but their original chapter association is never deleted.

The three catalog-supported alternate mappings are treated as `DORÉ-CROSSREF`, distinct from later editorial `DORÉ-REUSE`, so provenance remains auditable.

## Required chapter record

Each of the 1,189 records must eventually contain:

- book number / code / Chinese + English book name
- chapter number
- `artStatus`: `HISTORICAL` | `DORÉ-CROSSREF` | `DORÉ-REUSE` | `GENERATE-ONCE` | `FIXED-GENERATED` | `REVISION-REQUESTED`
- verified Doré / historical artwork title, if applicable
- exact Scripture reference depicted by the historical artwork
- mapping type: `direct` | `catalog-crossref` | `semantic-reuse`
- source URL / provenance
- source/native aspect ratio (`portrait` | `landscape`)
- canonical ONE asset path (for fixed local assets)
- chapter theme verse reference + approved text
- portrait-cover focal/crop metadata
- horizontal spread layout (`landscape-with-verse` | `portrait-with-verse`)
- Morning Star eligibility (only when compositionally appropriate)
- audit notes

## Doré reuse sequence

Only after the locked 184-chapter baseline is preserved:

1. evaluate Doré plates that have **not** been selected as a cover first, including additional plates from multi-plate chapters and deuterocanonical/apocryphal plates;
2. map them to still-uncovered chapters only when the image meaning genuinely fits that chapter;
3. after that pool is exhausted, evaluate Doré plates already used as covers for defensible semantic reuse;
4. every reuse must preserve the original plate provenance and record a concrete `reuseReason`;
5. visual mood alone is not sufficient evidence;
6. only after this reuse audit is complete may the remaining uncovered chapter count become the ONE Studio generation count.

## Canon structure / chapter totals

Old Testament — 929 chapters.
New Testament — 260 chapters.
Total — 1,189 chapters.

The canonical book/chapter totals remain those of the Protestant 66-book canon already established for ONE.

## Historical source baseline

Primary mapping baseline: chapter/verse-indexed catalogs of Gustave Doré's Bible illustrations, cross-checked where assignments are ambiguous. The complete Doré corpus is commonly cataloged as 241 Bible plates and includes deuterocanonical/apocryphal material. Those non-Protestant-canon plates remain available to the semantic reuse pool even though they do not create a direct canonical chapter mapping.

## Production gate

No bulk ONE Studio generation starts until the reuse audit yields exact counts for:

- locked direct/cross-reference Doré chapters;
- additional chapters covered by unused-plate semantic reuse;
- additional chapters covered by already-used-plate semantic reuse;
- final uncovered chapters requiring ONE Studio artwork.

Generation then proceeds chapter-by-chapter from `GENERATE-ONCE`, never as an uncontrolled batch.