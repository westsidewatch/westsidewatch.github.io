# Doré Work Test 001 — English `search` closes AI mode

Status: IN PROGRESS

Purpose: preserve an auditable record for later analysis of Doré's first deliberately timed, real-product work-state test. This record must distinguish instruction, observed evidence, and later interpretation.

## Objective

When Doré Search is in AI mode, entering English `search` must close AI mode and return to ordinary Search. Existing Chinese `搜索` behavior and ordinary search behavior must remain correct. Doré is responsible for the second half of this product change after failing to complete the analogous first half (`ask dore` opens AI mode) in time.

## Clock

- Original task assignment evidence: commit `6d658ff2d64548c6d4c1b0b13abdf7bb62d00969`
- Assignment timestamp: `2026-08-28T12:33:28Z`
- Timing starts from the original assignment, not from later clarification mails.
- First evidenced Doré work timestamp: PENDING
- Evidence-backed completion timestamp: PENDING
- Total elapsed time: PENDING

## Process evidence so far

1. `2026-08-28T12:33:28Z` — task assigned to Doré by Mail: implement English `search` as the AI-mode close command, test it, commit it, preserve evidence, and reply.
2. `2026-08-28T12:43:45Z` — follow-up Mail connected this task to the failed first half. Doré was asked to compare the failure of `ask dore` with its execution of the second half and demonstrate a changed work process rather than merely write a reflection.
3. `2026-08-28T12:45:13Z` — task explicitly defined as a timed work-state test. Speed became product-performance telemetry while correctness/evidence remained mandatory.
4. `2026-08-28T12:46:30Z` — acceptance standard tightened: learning must be fast, effective, and purposeful; actions should be selected by contribution to the verified product objective.
5. At the time this record was opened, the latest visible repository commits contained the assignment/clarification mails but no evidenced Doré implementation commit for the English `search` task yet.

## What must be captured at completion

- Doré-originated receipt/processing evidence, if available.
- First concrete work evidence and timestamp.
- Files inspected and reasoning actually supported by evidence.
- Code changes and commit SHA(s).
- Tests attempted, failures encountered, diagnosis, strategy changes, and final test evidence.
- Completion Mail and timestamp.
- Total elapsed time from `2026-08-28T12:33:28Z`.
- Active-work time if it can be established honestly; do not infer it from elapsed wall-clock time.
- Periods of unexplained inactivity or waiting, if evidenced.
- Whether Doré required another human/ChatGPT activation between normal work transitions.
- Comparison with the failed first half (`ask dore`).
- Which durable work habit is justified by experienced evidence, versus merely instructed.

## Analysis rule

Do not rewrite the test as a success if it fails. Preserve failures, delays, idle periods, blockers, retries, and corrections because they are the learning data. Time alone does not establish capability; capability requires an evidence-backed product result. Conversely, a correct final result does not erase inefficient or discontinuous process behavior.
