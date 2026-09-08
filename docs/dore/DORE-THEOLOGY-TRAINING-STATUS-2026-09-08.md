# Doré Theology Training Engineering Status — 2026-09-08

Status: ENGINEERING STARTED; TRAINING NOT YET EXECUTED.

Implemented on branch `dore-theology-training-poc`:

- isolated MLX-LM micro-POC orchestrator;
- read-only local readiness probe;
- external quarantine boundary that rejects Doré runtime/core data locations;
- separate-adapter / no-fusion POC policy;
- minimum-sufficient learning curve 0/32/64/128/256;
- unit coverage for staging/command construction/readiness helper;
- hard execution order requiring live Theology Rails acceptance before training;
- real-Mac measurement gate before any PASS claim.

Open PR: #439.

Next evidence gates:

1. CI/checks for PR #439;
2. close live Theology Rails integration and acceptance;
3. read-only Mac readiness report;
4. only then 32-example isolated micro-training.
