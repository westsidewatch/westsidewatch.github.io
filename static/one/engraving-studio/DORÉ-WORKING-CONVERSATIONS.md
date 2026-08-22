# Doré Working Conversations

Status: **MASTER WORKFLOW INDEX FOR PRODUCT-DEFINITION CONVERSATIONS**

This file is part of the Doré memo system. It records how dated product conversations are preserved and later synthesized before implementation. The main `DORÉ-SCRIPTURE-INTELLIGENCE-MEMO.md` remains the long-term architectural memory; dated conversation records preserve the movement of thought that leads to the final product definition.

## Why conversations are preserved separately

Doré is still being defined through continuing working conversations. A conversation is not assumed to begin with the final specification. Its purpose is to let ideas advance, collide, be corrected, connect to existing Westside Watch products and eventually clarify what should actually be built.

Therefore the record must preserve two different kinds of memory:

1. **Master memory** — durable principles, architecture, theology, product boundaries and decisions that remain valid across days.
2. **Dated working-conversation memory** — the development of an idea on a particular day, including proposals that may later be refined, rejected or absorbed into a stronger design.

The dated records must not be prematurely collapsed into one final specification, because the sequence of reasoning can matter when later decisions need to be understood or reconsidered.

## Working-conversation workflow

The intended workflow is:

`dated conversation -> preserve that day's developing ideas -> next dated conversation -> continue/refine/challenge -> repeat as needed -> pre-build synthesis -> implementation specification -> build`

Rules:

- Each substantial Doré product-definition conversation may receive its own date-stamped record, for example `2026-08-22`, `2026-08-23`, and later dates.
- A new day's discussion should normally create a new dated record rather than overwrite the previous day's reasoning.
- Dated records are working memory, not automatically runtime requirements.
- Later conversations may supersede earlier proposals. Supersession should be explicit during synthesis rather than silently rewriting historical records.
- Important durable conclusions may also be promoted into the master memo when they become stable enough.
- Before actual Doré product construction begins, read the master memo **and all relevant dated conversation records together**.
- The pre-build step must produce a final synthesis that identifies: what is definitely being built; what remains exploratory; what has been rejected or superseded; product boundaries; shared knowledge architecture; API/contracts; safety/editorial rules; implementation order; and unresolved decisions requiring human choice.
- Implementation should begin from that synthesis, not from whichever conversation happened most recently.

## Conversation index

### 2026-08-22

File: `DORÉ-SCRIPTURE-INTELLIGENCE-MEMO-2026-08-22-ADDENDUM.md`

Focus: Doré's emergence as the next Westside Watch product/project; Doré as a shared Scripture intelligence layer; Westside Stories as the first external consumer through subtitle proofreading; the ONE -> Doré -> Westside Stories -> human correction -> Doré feedback loop; Doré Core / Knowledge / Product Adapters; provenance; future API boundaries; preserving timestamps and safe fallback to raw Whisper output.

This record is the first explicitly date-separated Doré product-definition conversation. It should be read as a stage in the developing product idea, not as the final build specification.

### 2026-08-23 and later

Create separate dated records when the conversation materially advances Doré. Add each record to this index with a short statement of its focus and relationship to earlier decisions.

## Final synthesis gate before building

Doré should not move from exploratory conversation directly into implementation merely because enough ideas have accumulated. There is a deliberate synthesis gate.

Before the first full Doré product build:

1. read the complete master Doré memo;
2. read every indexed dated working-conversation record in chronological order;
3. trace which ideas persisted, changed, conflicted or were superseded;
4. consolidate stable decisions without erasing the history that produced them;
5. produce one current product-definition / implementation memo;
6. obtain human confirmation of any material unresolved choices;
7. only then begin implementation.

The purpose is to allow conversation to remain genuinely exploratory while ensuring that construction begins from the whole accumulated design intelligence rather than a partial snapshot.