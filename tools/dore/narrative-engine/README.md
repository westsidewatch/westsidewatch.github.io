# Doré Narrative Engine · Golden Gate Pilot

A reusable, evidence-aware editorial workflow for scene-driven historical nonfiction. First corpus: `docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md`, section `## 金門`.

## Run

```sh
python3 tools/dore/narrative-engine/narrative.py extract docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md
python3 tools/dore/narrative-engine/narrative.py audit docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md
python3 tools/dore/narrative-engine/narrative.py test
```

Extraction prints a JSON scene inventory and source span. Audit prints measurable scene/action/chronology indicators and possible exposition-only paragraphs. Tests check the extraction and guardrail behavior. This is a deterministic editorial harness, not a model or an automatic manuscript rewrite. It does not modify canonical manuscript.

## Editorial pipeline

1. Extract one named section without altering the manuscript.
2. Construct a scene ledger with evidence, time/place, actors, goal, obstacle, choice, consequence and narrative function.
3. Separate documented fact, defensible contextual reconstruction and unsupported invention.
4. Write scene-first prose, with historical scale interleaved at transitions.
5. Audit: scene specificity, chronology, narrative causality, character decisions, unsupported dialogue or thoughts, and paragraph-level redundancy.
6. Review the revised manuscript manually before publishing. Never automatically overwrite canonical text.

## Golden Gate acceptance

- Retain the east wall, Kidron, Mount of Olives, Jewish/Christian/Muslim traditions and biblical references.
- Establish the Latin Kingdom as consequence, then rewind to the crusading expedition.
- Make the three-year expedition and the 38-day siege structurally visible; do not confuse elapsed-day and inclusive-day counts.
- Include the June 13 failed assault, water crisis, timber supply, siege towers, July 14–15 assault and civilian aftermath.
- Keep the city defenders and civilians present; do not fabricate eyewitness dialogue, private thoughts or false precision.
- Do not turn evidence caveats into repeated narrator lectures.
- A paragraph should show an action, constraint, decision, consequence, or a necessary transition. Empty interpretive summaries fail editorial review.

Methodological references (framework only; do not reproduce copyrighted chapters): Jack Hart, *Storycraft*; Jon Franklin, *Writing for Story*; Kramer & Call, *Telling True Stories*; Roy Peter Clark, *Writing Tools*; Nieman Storyboard.
