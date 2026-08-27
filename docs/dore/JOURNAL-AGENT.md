# Doré Journal Agent

Status: Phase 1 — event layer implemented

## Principle

**Local + Cloud record; Local-first learning and journal judgment; GitHub is the single official engineering journal.**

GitHub Journal is evidence/audit history, not Doré's primary memory store.

## Flow

```text
ChatGPT / Doré Search / project work / GitHub evidence
                    |
          scope + context inheritance
                    |
              Learning Event
             /              \
       Cloud collector     Local collector
             \              /
               Memory Sync
                    |
          Local Journal Agent
        classify / verify / dedupe
                    |
          journal candidate
                    |
             GitHub evidence
                    |
          Official GitHub Journal
```

## Global learning scope

Always in scope:
- Scripture / biblical study
- Church
- Theology

Westside Watch scope:
- confirmed Westside Watch projects
- new projects classified as confirmed or candidate
- once a work context belongs to Westside Watch, its technical and design work inherits that scope

Context inheritance includes:
- coding and debugging
- website engineering
- GitHub / CI / deployment
- Cloudflare / API / database / AI infrastructure
- UI/UX
- visual design, typography, layout and animation
- screenshots and image-based design evidence
- architecture and product decisions

A single technical sentence or screenshot does not need to independently prove brand membership when its parent work context is already confirmed.

## Knowledge status

Learning events must distinguish:
- observation
- proposal
- evidence
- decision
- rejected
- corrected
- final
- verified

Discussion is never automatically treated as truth.

## Journal admission

Strong candidates:
- verified capability or milestone PASS
- architecture change
- important root-cause bug fix
- formal product/design decision
- rejected/replaced approach with reusable lesson
- cross-project knowledge
- significant failure worth preventing

Normally memory-only:
- tiny layout adjustments
- routine refresh/retry
- transient command output
- intermediate debugging noise
- unverified speculation

## Evidence chain

A journal entry should preserve, when available:
1. problem / question
2. cause
3. attempts
4. failed/rejected approaches and why
5. final solution/decision
6. verification result
7. evidence references (commit, test, conversation/message, file, screenshot)

## Cloud role

Cloud is an event collector and durable queue. It must not become a second independent official journal.

Endpoint: `POST /api/dore/learning-events`

The collector is deterministic and does not require Workers AI.

## Local role

Local Doré performs heavier classification, relation-building, deduplication and journal drafting using local inference where useful. If Local is offline, Cloud events remain pending until synchronization/resumption.

## GitHub role

GitHub is the sole official journal/evidence history. Journal writing must be idempotent and evidence-linked. Memory remains the primary cognitive/recall system.

## Event contract v1

Core fields:
- `id`
- `project_id`
- `conversation_id`
- `source_node`
- `event_type`
- `scope`: scripture | church | theology | westside_brand | candidate | out_of_scope
- `brand_project_status`: confirmed | candidate | not_applicable | rejected
- `modality`: text | code | design | image | screenshot | deployment | test | mixed
- `knowledge_status`
- `importance`
- `summary`
- `evidence`
- `source_ref`
- `journal_status`: pending | accepted | rejected | written
- timestamps

## Next phases

1. Local learning-event store + cloud sync.
2. Scope classifier and Project Context Inheritance.
3. Journal candidate scoring/deduplication.
4. GitHub evidence verification.
5. Automatic daily/milestone/decision journal writer.
6. Acceptance tests: offline Local, Cloud-only capture, resync, duplicate event, rejected proposal, verified milestone, cross-project decision.
