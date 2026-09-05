# DORÉ CAPABILITY EMBODIMENT ARCHITECTURE

Status: ACTIVE ARCHITECTURE / RESEARCH-BASED CORRECTION
Established: 2026-09-05

## Core correction

Doré must not become a federation of mini-products or mini-agents that communicate with each other through expensive conversational handoffs.

Doré is one persistent intelligence. Design, image generation, research, translation, search, publishing and future capabilities are faculties of the same Doré. Repositories and projects may remain separate for engineering ownership, testing and release discipline, but runtime identity must remain unified.

Project boundary != intelligence boundary.

`Doré Image` and `Doré Design` therefore do not "talk to each other" as two agents. They are two capability surfaces behind one Doré routing/reflex layer and one shared state/evidence model.

## Alignment with existing Doré architecture

This architecture formalizes principles already present in Doré Core:

- Doré is one persistent intelligence with bounded faculties and adapters.
- Current faculties are not independent agents.
- Providers are replaceable and are not Doré.
- The reflex layer performs `STIMULUS -> INTENT -> ROUTE -> EVIDENCE -> OUTCOME -> REFLEX UPDATE`.
- The reflex layer should stay small; many raw interactions should collapse into one transferable route.

The new implication is that new capabilities should be embodied through the reflex/capability-routing system rather than stacked as permanent active agents.

## Biological analogy

Use the following analogy only as an engineering map:

- **Doré Core primitives / judgment / memory** = brain + long-term nervous integration.
- **Reflex layer / capability router** = spinal cord + fast routing/reflex arc.
- **Faculties** (Scholar, Editor, Visual Director, Developer, Interpreter, etc.) = learned functional circuits, not separate persons.
- **Capabilities / skills** = learned motor patterns and specialized neural circuits.
- **Tools / providers / model runtimes** = muscles, sensors, instruments and replaceable external hardware.
- **Doré Design** = a manipulable visual workspace / hand-eye workbench.
- **Image renderer (ComfyUI, diffusers, SVG engine, etc.)** = visual motor machinery.
- **Projects** = training programs / engineering work packages, not extra brains.

A capability should feel like "Doré can do X" rather than "Doré asks agent X to do X" unless physical isolation, security, concurrency or a genuinely separate reasoning context justifies a sub-agent.

## Governing principle: sparse embodiment

Doré should grow in *capacity* while keeping per-task *activation* small.

At runtime:

`stimulus -> cheap intent gate -> activate minimal capability set -> execute -> verify -> consolidate`

The default target is Top-1 or very small Top-k capability activation. No task should load every skill, every prompt, every provider schema or every project memory.

A larger Doré should therefore be able to know and do more while loading less per action.

This follows the same broad systems principle demonstrated by sparse Mixture-of-Experts research: total capacity can increase while only a small subset is activated for a given input. It also follows modern skill registries and trigger-based microagent systems that keep capabilities dormant until relevant.

## Three-speed nervous system

### L0 — deterministic reflex

No LLM when unnecessary.

Examples:
- known file/type routing;
- asset metadata lookup;
- SVG export;
- deterministic transforms;
- test/verify commands;
- exact tool invocation from already-resolved intent;
- cache and artifact retrieval.

Target: milliseconds, near-zero inference cost.

### L1 — semantic reflex

Small/local embedding, classifier or compact model resolves ambiguous intent and chooses capabilities.

Outputs only a compact route manifest:

```yaml
intent: visual.hero.create
faculties: [visual]
capabilities: [image.generate, image.critic, design.insert]
providers: [local-image-renderer]
state_refs: [westside.visual.current]
verification: [asset-fit, responsive]
```

The route manifest is the communication medium between capabilities. It replaces conversational "agent A tells agent B" handoffs.

### L2 — deliberative cognition

Use a stronger reasoning model only when judgment, planning, synthesis, uncertainty or creative direction genuinely requires it.

Once L2 resolves the plan, execution should fall back to L0/L1 wherever possible.

## Capability registry

Every Doré capability should expose a compact manifest rather than permanent prompt/context residency.

Minimum fields:

```yaml
id: image.generate
faculty: visual
inputs: [visual_brief, style_recipe]
outputs: [asset_candidate]
triggers: [image request, missing hero asset]
requires: [renderer]
cost_class: local_free
latency_class: slow
state_reads: [visual_grammar, asset_registry]
state_writes: [candidate_asset]
verification: [render_exists, provenance, visual_review]
authority: A1
```

The registry is searchable; full instructions are lazy-loaded only after routing.

## Visual capability unification

Doré Visual becomes one faculty with several capabilities:

- `visual.direct` — interpret product need and establish visual intent;
- `visual.grammar` — retrieve/build Doré style grammar;
- `image.generate` — create raster/illustrative material;
- `image.control` — pose/reference/depth/line/inpaint control;
- `image.critic` — inspect and diagnose generated imagery;
- `design.compose` — manipulate structured Doré Design workspace;
- `design.typography` — hierarchy/type decisions;
- `design.svg` — native vector/ornament/geometry generation;
- `design.verify` — render/structure/responsive verification;
- `asset.publish` — register accepted asset and provenance.

These capabilities share the same task state. No textual A2A handoff is required for normal flows.

Example:

`ONE needs Matthew 3 hero`

becomes:

`Visual Director intent -> grammar -> image.generate -> image.critic -> design.compose -> design.verify`

This is one Doré run with sparse capability transitions, not a committee meeting.

## Shared state instead of conversational handoff

Capabilities communicate by durable typed artifacts:

- `VisualBrief`
- `StyleRecipe`
- `AssetCandidate`
- `CritiqueResult`
- `DesignPatch`
- `VerificationResult`

Each artifact has ID, schema version, provenance and content hash.

A capability receives only the artifact fields it needs. It does not receive the entire conversation history or another component's hidden reasoning.

This reduces token use, routing latency, accidental context contamination and debugging complexity.

## When separate agents are justified

Separate agents are an exception, not the default. Use only when one or more apply:

1. security/permission isolation;
2. parallel independent search that actually benefits wall-clock time;
3. incompatible model/runtime requirements;
4. adversarial review where independence is part of the evaluation method;
5. external service boundary or A2A interoperability;
6. long-running job that must outlive the initiating cognition loop.

Even then, agents communicate through typed artifacts/events and a shared job/state model where possible, not free-form recursive chat.

## External research principles absorbed

### Sparse activation / MoE

Modern MoE research reinforces the target architecture: increase total specialization while routing each input to only a small expert subset. Recent work further explores adaptive expert counts, routing stability, memory-aware specialization and even expert-autonomous routing. Doré should borrow the *systems principle*, not attempt to reproduce model-training algorithms at application level.

### Adaptive computation

Recent token-selective/adaptive-depth work shows that not every input deserves the same compute depth. Doré should apply the same idea at system level: deterministic/simple tasks halt early; difficult tasks escalate.

### Trigger/lazy skill loading

OpenHands skills/microagents use triggers so specialized knowledge is loaded only when relevant. Other capability-registry projects explicitly recommend routing first, reading matched entries only, and avoiding broad registry loading. Doré should adopt this as a first-class invariant.

### Plugin/function filtering

Semantic Kernel supports limiting available plugins/functions to a filtered subset. This supports the principle that the model should see only the relevant action surface, not the whole armoury.

### Long-term memory separation

Titans research distinguishes short-term attention from a persistent long-term memory mechanism. Doré already has explicit memory layers; runtime capability execution should retrieve only relevant durable memory rather than expanding the active prompt as Doré grows.

## Resource rule

Adding a capability must not permanently add its full runtime cost.

Every new capability must specify:
- dormant footprint;
- activation condition;
- cold-start cost;
- warm-cache cost;
- model/provider requirement;
- unload/eviction behavior;
- fallback path.

Target invariant:

> capability count may grow approximately linearly while average activated capability count remains bounded.

A useful first target is median active capabilities <= 3 for ordinary tasks and <= 6 for complex product tasks, excluding deterministic verification functions.

## Capability compilation

Repeated successful workflows should progressively compile downward:

`deliberative plan -> reusable workflow -> semantic reflex -> deterministic reflex where safe`

Example:

First Doré Original hero may require heavy L2 visual reasoning.
After enough validated examples, palette selection, safe-area computation, asset packaging and Doré Design insertion become L0/L1 behaviors. L2 remains for creative direction and exceptional cases.

This is the main mechanism by which Doré becomes stronger without becoming slower.

## Learning rule

A project is temporary; a capability is retained.

When a project creates a verified transferable ability:

`PROJECT EVIDENCE -> CAPABILITY CANDIDATE -> REGRESSION -> REGISTRY -> REFLEX ROUTE`

The project may then close while the capability remains available to all Doré surfaces.

This prevents "armour stacking": the engineering package disappears from the active cognitive path once its lessons have become native capability.

## Immediate correction to Doré Image / Doré Design

Engineering projects remain distinct for now because they have different code, test and runtime responsibilities. Runtime architecture changes immediately:

- no Image-agent <-> Design-agent conversation layer;
- no duplicate visual memory;
- no separate identity/state;
- one `visual` faculty;
- one shared visual task state;
- one capability router;
- typed artifacts between stages;
- lazy activation of image/design capabilities;
- providers loaded only on demand.

## Acceptance gates

This architecture is not complete until measured.

Required tests:

1. A visual task routes through Image + Design without free-form inter-agent chat.
2. A non-visual task does not load image/design skill bodies or renderer schemas.
3. Adding a new dormant capability causes negligible ordinary-run latency/context increase.
4. The same artifact state can be inspected by Doré Design and visual generation capabilities without duplication.
5. A repeated visual workflow demonstrates downward compilation (fewer reasoning/model calls on later validated cases).
6. Capability routing failures feed the existing reflex loop and regression set.
7. Resource telemetry reports active capabilities, model calls, latency, memory/context footprint and cache hits.

## Architectural direction

Do not build a larger suit of armour.

Build a nervous system that can selectively recruit more muscles.

Doré's growth metric is not number of agents, projects, prompts or services. It is the number of verified transferable capabilities available to one intelligence at bounded marginal runtime cost.