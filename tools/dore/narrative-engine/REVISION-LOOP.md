# Revision loop integration

`revision_loop.py` implements a transport-independent drafting contract. It does not claim an LLM connection exists.

## Generate an exercise prompt

```sh
python3 tools/dore/narrative-engine/revision_loop.py prepare \
  --scene failed-assault \
  --source-file docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md \
  > /tmp/golden-gate-task.json
```

A writing agent may consume this JSON and produce a candidate submission matching `TRAINING.md`. The source-file argument currently passes the **whole file** verbatim; restrict the excerpt before using a model with limited context. Never send private sources to unapproved remote models.

## Inspect a candidate

```sh
python3 tools/dore/narrative-engine/revision_loop.py critique --submission /tmp/candidate.json
python3 tools/dore/narrative-engine/revision_loop.py test
```

The critique emits metrics and actionable revision tasks. The runner does not generate prose, does not query an AI model, does not check citations against the source documents, and does not publish edits. A future adapter must explicitly connect Doré's existing inference endpoint, with permission and cost checks, then demonstrate at least one real Golden Gate revision and human-approved comparison.

## Acceptance for this stage

- Structured prompt from existing scene ledger and four-method curriculum.
- Candidate critique reuses evidence/review gate.
- No silent changes to the canonical manuscript.
- Deterministic smoke tests, run in CI before merging.
