#!/usr/bin/env python3
from editorial_visual_observation_capability import (
    HistoricalImageEvidence, VisualObservationError,
    observe_historical_editorial_image, promoteable_to_prompt, DIMENSIONS,
)

E = HistoricalImageEvidence(
    evidence_id="fixture-magazine-001",
    image_uri="https://evidence.example/historical-cover.jpg",
    source_uri="https://evidence.example/issue",
    publication="Fixture Magazine",
    era="Fixture Era",
)


def grounded(req):
    assert req["authorityContract"]["mustInspectImage"] is True
    return {
        "imageInspected": True,
        "dimensions": {
            d: ({"status": "observed", "facts": [f"visible {d} fact from image"]}
                if d in {"layout", "image", "typography", "material", "density"}
                else {"status": "insufficient", "facts": []})
            for d in DIMENSIONS
        },
    }


def ungrounded(req):
    return {
        "imageInspected": False,
        "dimensions": {d: {"status": "observed", "facts": ["generic Italian concrete architecture"]} for d in DIMENSIONS},
    }

obs = observe_historical_editorial_image(E, grounded, provider_id="fixture-grounded", provider_kind="grounded-chatgpt-vision")
assert obs["canonicalDoréLearning"] is False
assert promoteable_to_prompt(obs)
assert obs["provenance"]["imageInspected"] is True

try:
    observe_historical_editorial_image(E, ungrounded, provider_id="generic-style-prior", provider_kind="text-only")
except VisualObservationError:
    pass
else:
    raise AssertionError("ungrounded provider must be blocked")

print("EDITORIAL_VISUAL_OBSERVATION_AUTHORITY=PASS")
print("UNGROUNDED_STYLE_PRIOR=BLOCKED")
print("PROVIDER_OUTPUT_IS_NOT_DORE_CANON=PASS")
