# Doré Exploration — Design Mastery Baseline

Date: 2026-09-09
Status: EXPLORATION RECORD — NOT YET ARCHITECTURE

## Why this record exists

Preserve the current Doré Exploration findings before the next research round. These are candidate conclusions to test, not frozen architecture. Exploration decides when conclusions are mature enough for engineering; conclusions must not predetermine exploration.

Core Doré principle: capability should grow while burden shrinks. Mature human work should be absorbed where possible; immature areas remain open to continued exploration.

## Context

The current problem is not merely producing more templates. Doré should eventually become capable of autonomous, high-quality, non-homogeneous design. This field is comparatively immature, so mature products, mature open-source systems, large design corpora, and professional design knowledge deserve especially deep exploration.

A useful analogy emerged: asking a thinly educated AI to improve through a loop resembles asking a primary-school student to teach itself. A design director who begins with deep professional knowledge and then continues learning has a radically stronger starting point. Doré's learning loop therefore needs a thick human-design foundation beneath it.

Large-scale signals repeatedly observed in mature products/resources include: decades of accumulated human design expertise, 1000+ component/block libraries, and multi-million-scale design/product corpora. These signals motivate two parallel exploration tracks.

## Exploration Track A — Human design mastery as Doré's foundation

Question: what mature open-source knowledge, design systems, component libraries, corpora, rules, examples, and professional corrections can give Doré the equivalent of deep human design education before autonomous looping?

Candidate sources/patterns identified so far include:

- mature design systems and machine-readable design-system knowledge;
- component/block libraries at 1000+ scale;
- large real-world UI corpora;
- responsive screenshots paired with HTML/CSS/JS/DOM structure;
- design tokens, typography, spacing, motion, accessibility and review rules;
- professional designer correction/revision datasets;
- agent-native access patterns such as registries, structured docs, MCP-style tools, retrieval and compliance checks.

Important distinction: `1000 components exist` does not mean `Doré understands 1000 components`.

The likely missing middle layer is machine-usable design knowledge:

`design corpus -> structured representation -> selective retrieval -> usage rules -> component/pattern selection -> constraints -> validation -> artifact`

Licensing/provenance must remain explicit. Resources may fall into at least three classes: directly reusable code/assets, pattern/knowledge extraction only, and evaluation/reference only. Large external corpora must not silently become copied Doré templates.

## Exploration Track B — How large design experience becomes autonomous generation ability

Question: after Doré has access to large-scale high-quality design knowledge, how does that experience become design judgment and original generative ability rather than imitation?

Promising mature/near-mature patterns found so far:

- selective retrieval rather than loading a huge corpus into active context;
- global and local example retrieval;
- composition/remix of mature structures;
- controlled generative escape when the existing vocabulary cannot express the design intent;
- human selection and direct editing;
- preservation of high-information correction evidence;
- learning from the difference between AI artifact and professional human revision.

A key warning remains: exposure to many examples is necessary but not sufficient. More examples can still cause fixation, convergence, overwhelm or design drift. The unresolved target is `judgment`, not merely `memory` or `imitation`.

## Three candidate conclusions from the current exploration

These conclusions MUST be challenged in subsequent Doré Exploration. They are not accepted architecture merely because they currently look plausible.

### Candidate 1 — Design Foundation

High-confidence direction: Doré needs a thick human-design foundation before expecting a self-improving design loop to produce design-director-level work.

Current refinement: the best implementation may NOT be a huge knowledge base loaded into the model. Mature agent-native design systems increasingly suggest:

`huge available knowledge surface + tiny active working context`

Possible foundation shape:

`Corpus + Registry + Retrieval + Tools + Constraints + Validator`

This fits Doré's lightweight principle better than permanently carrying all design knowledge in model context or runtime dependencies.

This conclusion must still be tested against alternatives: training/fine-tuning, learned representations, compact distilled knowledge, multimodal models with native design competence, or hybrid approaches may outperform retrieval-heavy architecture.

### Candidate 2 — Design Intelligence

Current candidate:

`understand problem -> selectively retrieve -> compare -> reason/judge -> compose/remix -> generate/escape -> validate`

The critical addition is **selective** retrieval. Retrieval itself is not design intelligence.

Open question: how does large experience become design judgment rather than sophisticated imitation? This is one of the two darkest boxes in the current exploration.

This conclusion must be compared with mature alternatives, not assumed optimal.

### Candidate 3 — Human Correction Learning Loop

High-confidence observation: direct human revision carries much more learning information than simple accept/reject feedback.

Useful evidence can include:

`original artifact -> human annotation -> human edit/revision -> resulting artifact -> preserved/replaced structures`

However, the mechanism by which correction becomes durable Doré capability remains unresolved. Candidate mechanisms include retrieval memory, derived design rules, preference learning, fine-tuning, reward models, or hybrid/distilled learning.

Therefore only `preserve rich correction evidence` is currently strong. `How to learn from it` remains open and must be explored.

## Important mature-product observations

### Mature products often use a two-layer creativity model

1. constrained composition using mature components/tokens/layouts/design systems;
2. generative escape when mature vocabulary cannot express the intent.

This challenges the assumption that every design must be generated from scratch to count as creative.

### Templates/components are not necessarily the cause of homogeneity

Mature structures can be reliability foundations rather than creative ceilings. The deeper question is whether the system can choose, recombine, vary, and escape them intelligently.

### Existing Doré templates should not become ancestral style authorities

Dawn Atlas, Living Current and Signal Nocturne should be treated as completed design specimens / occupied examples, not as the three templates from which all future Doré design descends.

### Design Map is currently downgraded

Earlier ideas such as Grammar Pool, novelty gates and fixed Design Map axes remain research candidates. Mature-product exploration currently suggests they should not be engineered prematurely. A Design Map may still prove useful, but it has not earned architectural status.

## Mature/open-source leads already identified

These should be verified and deepened rather than merely name-dropped:

- State of AI in Design Systems: cross-system survey of machine-readable/agent-native design-system techniques;
- ReUI: large production-ready component/example source with lightweight copy-and-own characteristics;
- large WebUI corpora and related screenshot + structure datasets;
- WebSight and similar large synthetic/real UI corpora, with caution about size and training burden;
- UI Remix: retrieval/remix research and implementation for navigating example corpora without relying on a single example;
- Apple `ml-rldf`: professional designer feedback/revision data for generated UIs;
- mature product patterns observed in Relume, Wix Harmony, Squarespace Design Intelligence, Builder/Fusion, Framer/Webflow-class AI design tooling.

Product claims and exact dataset/library counts must be reverified from primary sources before engineering decisions.

## Next exploration mandate

Continue two parallel lines:

A. Find the strongest mature/open-source ways to give Doré deep human design knowledge: not just more assets, but machine-usable professional design expertise.

B. Find the strongest mature methods by which an AI standing on that large knowledge base develops autonomous generation and judgment.

At the same time, explicitly test whether the three current candidate conclusions are actually the most effective solutions:

1. Is `huge knowledge surface + tiny active context` really superior to stronger training/distillation/hybrid approaches for Doré?
2. Is `selective retrieval + reasoning + composition + generative escape` the strongest path from knowledge to original design judgment?
3. Is `rich human correction evidence -> continuous learning` the strongest learning loop, and what is the lightest durable mechanism for converting corrections into capability?

Do not force closure. If mature solutions are abundant, shift rapidly from invention to adaptation. If the field remains fragmented or immature, continue exploration and preserve uncertainty.

## Engineering boundary

This file records exploration. It does NOT authorize implementation of a new parallel Template Loop, Design Map, training system, or permanent dependency.

Existing responsibility boundary remains:

`Doré Exploration -> external learning`

`Storybook Loop -> design experimentation/candidate production`

`Template Registry -> mature reusable outputs`

`Doré Design -> structured use/edit/render/validation`

`Human feedback / Knowledge Lab -> learning evidence`

Future exploration may revise how these pieces learn, but should avoid adding overlapping systems unless evidence demonstrates a real missing responsibility.
