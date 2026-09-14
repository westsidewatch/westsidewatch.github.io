from __future__ import annotations

FORBIDDEN_STYLE_SHORTCUTS = (
    "campo grafico",
    "italian style",
    "vintage magazine",
)

GRAMMARS = {
    "hierarchy-before-decoration": {
        "signals": {"threshold", "gate", "dawn", "watch", "city", "ruin", "light", "silence"},
        "directive": "Build one unmistakable visual hierarchy before any decorative treatment; let one dominant form carry the semantic center.",
    },
    "coherence-without-sameness": {
        "signals": {"archive", "objects", "fragments", "witness", "documents", "city"},
        "directive": "Allow heterogeneous elements to retain distinct visual identities while a precise spatial relation makes them read as one editorial argument.",
    },
    "content-medium-rewrites-grid": {
        "signals": {"image", "photograph", "map", "archive", "object", "stone", "gate"},
        "directive": "Let the dominant image or object determine the spatial system; secondary elements adapt to the remaining field rather than forcing a preset grid.",
    },
    "material-evidence-before-abstraction": {
        "signals": {"stone", "archive", "document", "artifact", "ruin", "gate"},
        "directive": "Preserve physical evidence—surface, edge, wear, scale, paper or stone—as meaningful structure; do not smooth it into generic polish.",
    },
    "identity-survives-format-instability": {
        "signals": {"sequence", "issue", "spread", "cover", "threshold"},
        "directive": "Keep editorial identity legible through proportion, hierarchy and relation rather than repeated motifs or a fixed template.",
    },
}

NEGATIVE_CONSTRAINTS = (
    "No nostalgic period cosplay, copied mastheads, logos, or recognizable historical page imitations.",
    "No generic luxury-editorial styling, decorative collage, arbitrary distressing, or texture without semantic reason.",
    "Do not use a style-name shortcut; composition must be justified by the content.",
)


def _flatten_brief(brief: dict) -> str:
    values = []
    for value in brief.values():
        if isinstance(value, (list, tuple)):
            values.extend(str(item) for item in value)
        else:
            values.append(str(value))
    return " ".join(values).lower()


def compile_editorial_prompt(brief: dict, max_grammars: int = 4) -> dict:
    if not brief.get("semantic_intent"):
        raise ValueError("semantic_intent is required")

    text = _flatten_brief(brief)
    scored = []
    for grammar_id, spec in GRAMMARS.items():
        score = sum(1 for signal in spec["signals"] if signal in text)
        if score:
            scored.append((score, grammar_id))
    scored.sort(key=lambda item: (-item[0], item[1]))

    selected = [grammar_id for _, grammar_id in scored[:max_grammars]]
    directives = [GRAMMARS[grammar_id]["directive"] for grammar_id in selected]

    if not selected:
        return {
            "status": "DECLINED_NOT_APPLICABLE",
            "semantic_intent": brief["semantic_intent"],
            "selected_grammars": [],
            "negative_constraints": list(NEGATIVE_CONSTRAINTS),
            "image_prompt": None,
        }

    prompt = " ".join(
        [
            f"Create an editorial image whose meaning is: {brief['semantic_intent']}",
            *directives,
            *NEGATIVE_CONSTRAINTS,
        ]
    )

    lowered = prompt.lower()
    if any(term in lowered for term in FORBIDDEN_STYLE_SHORTCUTS):
        raise AssertionError("forbidden style-name shortcut leaked into compiled prompt")

    return {
        "status": "COMPILED",
        "semantic_intent": brief["semantic_intent"],
        "selected_grammars": selected,
        "negative_constraints": list(NEGATIVE_CONSTRAINTS),
        "image_prompt": prompt,
    }


if __name__ == "__main__":
    sample = {
        "semantic_intent": "A city still in shadow watches for dawn: the gate is present as a threshold, ancient stone carries memory, and first light must feel promised rather than decorative.",
        "content_objects": ["ancient stone gate", "dark city mass", "first light at horizon"],
        "desired_use": "Westside editorial hero image",
        "notes": "No text inside image. Silence and waiting matter more than spectacle.",
    }
    print(compile_editorial_prompt(sample))
