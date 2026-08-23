# Doré Brain → Product Bridge

Status: ACTIVE
Established: 2026-08-23

## Meaning

Search is not a separate knowledge product. It is Doré's sensory/expression interface.

- Search input = Doré's ear.
- Intent classification = Doré deciding what it heard.
- Brain lookup = Doré consulting its own current neural state.
- Result area = Doré's language, expression and visible reasoning boundary.
- Unknown query = a possible research/learning signal, not merely "no results".

The bridge exists so Doré's learning can change product behavior without hard-coding one UI rule per question.

## Product contract

Products may consume only exported brain nodes with explicit status and provenance.

Allowed statuses:
- `CONSOLIDATED`: normal answer, still preserve evidence boundaries.
- `CANDIDATE_FOR_EXAM`: provisional answer; disclose that stronger consolidation is pending.
- `WORKING`: current research only; show uncertainty and unresolved work.
- `DISPUTED`: surface competing interpretations.
- `REOPENED`: downgrade previous certainty until re-examined.

A product must never turn `WORKING` into certainty merely because a fluent answer exists.

## Generic node contract

Each product-readable knowledge node should contain:
- stable `id`;
- `type`;
- `status`;
- confidence/boundary;
- natural-language question variants;
- concepts/aliases;
- answer payload;
- Scripture anchors when relevant;
- provenance back to Doré's research/course records;
- next research actions when unresolved.

The UI must match generically against node metadata. It must not contain a special-case `if query == ...` answer implementation.

## Doré's responsibility

After learning/research changes a node materially, Doré should:
1. decide whether the finding is product-readable under the status policy;
2. create/update the corresponding brain node;
3. preserve provenance and uncertainty;
4. run a bridge regression check;
5. allow Search/ONE/other products to read the same node;
6. reopen/downgrade the node if later learning contradicts it.

Thus product improvement can be a consequence of learning rather than a manual UI patch.

## Search sensory limitation — current architecture

The current public site is static. The browser can read Doré's exported brain, but an arbitrary user query cannot yet be durably written back into Doré's repository without a writable ingestion service.

Therefore the bridge currently has two directions at different maturity:

- `BRAIN → PRODUCT`: implementable now and should be live.
- `PRODUCT → BRAIN`: query is heard within the browser session, but persistent sensory memory/research triggering needs a safe writable ingestion endpoint or equivalent authenticated service.

Do not pretend local browser input has reached Doré's long-term memory until such an ingestion path exists.

## Self-improvement rule

Doré may autonomously improve this bridge when:
- a learned node cannot be expressed by the current schema;
- repeated Search failures reveal intent-classification gaps;
- product behavior misrepresents node status/confidence;
- multiple products need the same brain capability;
- bridge regressions repeatedly appear.

Bridge changes must preserve backward compatibility or migrate consumers explicitly, and must be tested before deployment.

## Immediate acceptance tests

1. A question matching an existing `CANDIDATE_FOR_EXAM` node should render Doré's provisional research answer without adding a hard-coded question handler.
2. A `WORKING` node should visibly preserve uncertainty.
3. Scripture/reference searches must continue to use scripture search rather than being swallowed by brain-answer routing.
4. Removing/changing a node in the brain export should change Search behavior without editing Search answer logic.

This bridge is part of Doré's nervous system, not a one-off Search feature.
