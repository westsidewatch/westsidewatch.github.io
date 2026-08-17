# ONE — Doré Illustration × Bible Chapter Master Table

Status: CANONICAL LEDGER · BUILDING FROM LOCKED EVIDENCE

Locked coverage baseline: **447 / 1,189 chapters**.

This file is the single authoritative chapter-level ledger for Gustave Doré allocations in ONE. A chapter does not count merely because a book-level total says it is covered: the row must record the exact Bible chapter and exact Doré plate identity/provenance. Reuse must never be represented as Doré's original chapter assignment.

## Columns

| # | ONE chapter | Doré plate / exact title | Doré original provenance | ONE relation | Evidence / note |
|---:|---|---|---|---|---|
| 1 | Psalm 109 | The Death of Ahab | 1 Kings 22 | DORÉ-REUSE / IMAGE-MEANING | Locked precision allocation; judgment/downfall reuse |

## Locked coverage control

| Scope | Locked covered chapters | Row-level reconstruction status |
|---|---:|---|
| Psalms | 150 / 150 | Reconstruct exact plate rows from current mappings + locked history |
| Proverbs | 31 / 31 | Reconstruct exact plate rows from locked history |
| Ecclesiastes | 12 / 12 | Reconstruct exact plate rows from locked history |
| Song of Songs | 8 / 8 | Reconstruct exact plate rows from locked history |
| All other locked allocations | 246 | Reconstruct exact plate rows from current mappings + locked history |
| **TOTAL** | **447 / 1,189** | **447 rows required before ledger is complete** |

## Non-negotiable ledger rules

1. Exactly one coverage row per counted Bible chapter; multiple plates for one chapter do not increase coverage.
2. Every row must name the exact Doré plate, not a generic theme label.
3. Every row must preserve Doré's original biblical provenance.
4. `DIRECT` means the Doré plate itself belongs to that chapter/event.
5. `DORÉ-REUSE / IMAGE-MEANING` means ONE editorially reuses a Doré plate for another chapter because its depicted meaning is strongly appropriate.
6. Reuse never changes or falsifies Doré provenance.
7. Weak mood-only matches are excluded.
8. The locked total **447** is preserved while row-level evidence is reconstructed; no invented row may be used merely to make the row count reach 447.
9. New allocations after this checkpoint append rows and update the locked total only after duplicate removal.
10. This ledger supersedes scattered prose totals as the audit source of truth once all 447 locked rows have been reconstructed.

## Reconstruction queue

The repository currently contains chapter illustration mappings and audit material for Genesis, 1 Samuel, 2 Samuel, Psalms, Isaiah, Matthew, Mark, Luke, John, 1 Thessalonians and 2 Thessalonians, plus the locked master checkpoint. Historical commits must also be consulted because some earlier precision/reuse passes are summarized in the checkpoint but are not retained as 447 explicit rows in the current master document.

No missing plate/chapter pair is to be guessed. Rows are added only when recoverable from repository evidence or an explicitly verified Doré source.