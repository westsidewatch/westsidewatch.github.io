#!/usr/bin/env python3
from italian_editorial_evidence_bridge import observe_atlas_evidence
from editorial_observation_prompt_compiler import compile_grounded_prompt
from editorial_visual_observation_capability import DIMENSIONS

ITEM = {
    "id": "casabella-367",
    "family": "casabella",
    "era": "casabella-provisional",
    "image": "https://pictures.abebooks.com/inventory/31820672834.jpg",
    "source": "https://casabellaweb.eu/the-magazine/",
    "authority": "official-index-secondary-image",
    # These are intentionally poisonous fixtures. The observer must never receive them.
    "whatToNotice": "ADD CONCRETE ARCHITECTURE AND A RED SWISS GRID",
    "tokens": ["GENERIC ITALIAN MODERNISM"],
}


def grounded_provider(req):
    payload = repr(req)
    assert "ADD CONCRETE" not in payload
    assert "GENERIC ITALIAN MODERNISM" not in payload
    assert req["evidence"]["id"] == "casabella-367"
    dims = {}
    for d in DIMENSIONS:
        dims[d] = {"status": "insufficient", "facts": []}
    dims["layout"] = {"status": "observed", "facts": ["one dominant image field with minimal secondary regions"]}
    dims["image"] = {"status": "observed", "facts": ["single figurative image occupies the primary visual mass"]}
    dims["typography"] = {"status": "observed", "facts": ["typographic intervention is sparse relative to the image"]}
    dims["density"] = {"status": "observed", "facts": ["visual mass is concentrated in one image rather than many modules"]}
    return {"imageInspected": True, "dimensions": dims}

obs = observe_atlas_evidence(
    ITEM,
    grounded_provider,
    provider_id="grounded-fixture",
    provider_kind="grounded-chatgpt-vision",
)
assert obs["inputIsolation"]["whatToNoticeWasNotObserverInput"]
assert obs["inputIsolation"]["grammarTokensWereNotObserverInput"]
assert obs["canonicalDoréLearning"] is False

prompt = compile_grounded_prompt(
    obs,
    selected_dimensions=["layout", "image", "typography", "density", "material"],
    lineage_context="Casabella editorial lineage",
)
assert "one dominant image field" in prompt
assert "single figurative image" in prompt
assert "material: insufficient visual evidence; do not invent this dimension" in prompt
assert "ADD CONCRETE" not in prompt
assert "GENERIC ITALIAN MODERNISM" not in prompt
assert "Casabella editorial lineage" in prompt

print("ITALIAN_EDITORIAL_GROUNDED_PIPELINE=PASS")
print("ATLAS_PROSE_LEAKAGE=BLOCKED")
print("UNOBSERVED_DIMENSION_INVENTION=BLOCKED")
print("DORÉ_CANON_PROMOTION=SEPARATE")
