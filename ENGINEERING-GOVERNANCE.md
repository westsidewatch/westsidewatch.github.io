# Westside Watch — Repository-wide Engineering Governance

This contract applies to all engineering work in this repository and to every project conversation that operates on it: Westside Watch, Living Water, ONE, Doré, Dawn Library, Cinema, 池底, Jerusalem 3000, games, publishing systems, shared Core, and future projects.

## Execution-until-stage-complete directive

When the human gives an instruction such as `不可停留在通報層`, `完成再通報`, `中間不要停`, `繼續工程不用停`, `不要一直通報`, or another instruction with the same clear meaning, it establishes an execution boundary for the current engineering stage across the repository.

While that directive is active:

- acknowledgement is not execution and must not terminate the work turn;
- a commit, PR, CI result, merge, deployment trigger, successful deployment, intermediate diagnosis, or partial fix is not a reporting boundary;
- the agent must continue performing the next available engineering action inside the current stage instead of returning an intermediate status report;
- reporting is permitted only after the current stage Definition of Done has been satisfied and verified;
- the only permitted early return is a genuine hard blocker that cannot be resolved with the available tools or authority, such as missing human-only authorization, unavailable required source data, or a tool/permission boundary that prevents further execution;
- a hard-blocker report must identify the blocker precisely and must not describe the stage as complete.

This directive is semantic, not phrase-specific. Equivalent wording carries the same execution requirement.

## Completion semantics

A PR, commit, merge, CI pass, deployment trigger, successful deployment, runtime boot, or implementation milestone is not automatically completion. Each engineering stage must use its own explicit Definition of Done. Where a machine-readable completion contract exists, it is authoritative for release of the reporting gate.

## Scope

Project-local governance may add stricter requirements but may not weaken this repository-wide execution rule. New projects inherit it automatically; it does not need to be restated in every project folder or conversation.
