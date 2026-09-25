# Fond Canonical Writing Rule

## Hard rule

All writing projects in this repository MUST have exactly one current manuscript authority.

That authority MUST be the Markdown file directly connected to the Fond reader (`/fond`).

### Required behaviour

1. New writing, continuation, correction, deletion, and full-text revision MUST update the Fond-connected canonical MD in place.
2. NEVER create a new `v2`, `v3`, `working-save`, `recovered`, `edited-manuscript`, `continuation`, dated manuscript, or parallel正文 file to represent a newer current version.
3. Historical files may remain only as archive/evidence. They MUST NOT become a current writing target and MUST NOT be read by Fond.
4. Fond MUST read the canonical MD directly. No copied正文, generated intermediate正文, fallback manuscript, or alternate current source is allowed.
5. Canonical MD contains publication正文 only. Do not put AI notes, recovery notes, save status, source notes, editorial instructions, authority notes, workflow notes, or engineering metadata inside it.
6. If a project does not yet have a Fond-connected canonical MD, establish that canonical MD and connect it to Fond BEFORE further writing is saved.
7. When asked to “save”, “continue”, “revise”, “全文修正”, or otherwise modify a writing project, resolve its Fond-connected canonical MD first and write to that same file.
8. A successful save means the canonical MD itself changed. Creating another manuscript file does NOT count as saving the current work.

## Current principle

**One work → one current canonical manuscript path → Fond reads that path → all future writing updates that path.**

Archives preserve history. Canonical MD preserves the current text. Fond publishes the canonical MD.
