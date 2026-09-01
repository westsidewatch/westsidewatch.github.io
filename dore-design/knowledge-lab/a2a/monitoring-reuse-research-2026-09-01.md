# A2A Monitoring — Reuse Before Rebuild Research (2026-09-01)

## Problem

The Doré↔ChatGPT A2A relationship must supervise lower-order project continuation loops. Repeated no-progress or peer non-response must become observable A2A state. A bespoke supervisor was started too early; this research resets the implementation order to: discover mature monitoring stacks -> compare -> run a local experiment -> adopt only what fits -> write the thinnest Doré-specific adapter.

## Mature candidates checked

### 1. Prometheus + official Python client + Alertmanager — primary adoption candidate

- Official Python client: `prometheus/client_python`.
- License: Apache-2.0 AND BSD-2-Clause.
- Current package metadata requires Python >=3.9.
- Native primitives map directly to Doré state: Gauge for current state/queue depth/age, Counter for transitions/failures/escalations, Histogram for cycle/experiment durations.
- Prometheus alerting rules natively express sustained conditions with `for:` and can avoid flapping with `keep_firing_for:`.
- Alertmanager already implements grouping, deduplication, routing, silencing and inhibition. These are exactly the mature mechanisms we should not re-create.
- Prefer Prometheus pull/scrape. Do not default to Pushgateway; upstream explicitly warns it removes normal `up` health semantics and retains stale series.

Decision: **ADOPT FIRST, smallest local experiment.** The Doré-specific code should only translate A2A/project-loop state into stable metrics and labels. Stall timing, repeat detection and notification policy should move into Prometheus rules/Alertmanager rather than remain custom Python logic.

### 2. OpenTelemetry Python — tracing foundation, second adoption candidate

- CNCF/OpenTelemetry official Python SDK.
- Apache-2.0.
- Traces and metrics are stable; logs are still development.
- Current official Python support is >=3.10.
- Semantic conventions give us a standard way to name spans/events/attributes and correlate A2A task -> research -> experiment -> Storybook work.

Decision: **ADOPT AFTER local Python-version compatibility is verified.** Use for distributed trace/context, not as the sole alert engine.

### 3. Arize Phoenix — AI/agent observability UI, later candidate

- Open-source AI observability/evaluation platform.
- Built on OpenTelemetry/OpenInference.
- Provides tracing, evaluations, datasets and experiments; can run locally or self-hosted.

Decision: **Candidate for a later visual/debugging layer**, not required to restore supervision now. Verify exact repository license and local resource cost before adoption.

### 4. Langfuse — heavier LLM engineering observability platform

- Open source, self-hostable, strong tracing/evaluation/metrics platform.
- Main repository is MIT except `ee` folders.
- Self-hosting normally uses Docker and additional infrastructure.

Decision: **Defer.** Strong tool, but heavier than needed for this local A2A supervision gap.

## Initial architecture after reuse research

`Doré Agent Core / A2A adapter -> Prometheus metrics endpoint -> Prometheus rules -> Alertmanager -> A2A intervention signal`

Later:

`A2A task/research/experiment spans -> OpenTelemetry -> Phoenix or another OTLP-compatible viewer`

The project continuation loop remains below A2A. Prometheus observes both and evaluates health. ChatGPT remains an active A2A peer; monitoring does not replace the peer role.

## First falsifiable experiment

1. On the Mac, determine Python version and whether `prometheus_client` is already available.
2. If compatible and absent, install only the official `prometheus-client` package into Doré's local Python environment; do not install a new AI framework.
3. Export a tiny metrics surface containing at minimum:
   - `dore_a2a_up`
   - `dore_project_loop_progress_timestamp_seconds`
   - `dore_project_loop_unchanged_cycles`
   - `dore_a2a_peer_required`
   - `dore_a2a_interventions_total`
4. Validate exposition using the official client library.
5. Check whether a local Prometheus binary/package already exists. If absent, discover the lightest maintained macOS installation route and record provenance before installing.
6. Define a rule where sustained no-progress becomes an alert via Prometheus `for:` rather than bespoke Python repeat-count policy.
7. Only after this passes, remove/replace duplicate custom stall logic in `a2a_supervisor.py`.

## Promotion rule

No monitoring capability becomes a Doré Skill until the local experiment proves: repeated no-progress is detected by the mature stack; alert state survives ordinary agent cycles; project parent identity remains intact; no human relay is required.
