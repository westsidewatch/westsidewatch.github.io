"""Reference-grounded editorial art direction for the existing Doré speaker worker.

Only use a real, authorized reference photograph. This module does not generate
an image, authorize publishing, or claim a local model has passed visual QA.
"""
from pathlib import Path

PROFILE = "olive-engraved-portrait-v1"

def build_reference_profile(spec, reference):
    path = Path(reference).expanduser().resolve()
    if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("A readable PNG/JPEG/WebP reference photograph is required")
    if path.stat().st_size == 0:
        raise ValueError("Reference photograph is empty")
    slug = spec["slug"]
    prompt = (
        "REFERENCE-DEPENDENT PORTRAIT. Use the supplied photograph as the sole "
        "source of the person's face, age, hair, glasses, beard, and facial proportions. "
        "Preserve recognizable identity and asymmetries; do not invent or idealize features. "
        "Produce an art-directed Italian editorial magazine portrait illustration, "
        "not a generic engraving filter. Strongly cropped head and shoulders, oversized "
        "face near the left edge, bold silhouette, confident asymmetrical composition, "
        "dramatic off-center negative space reserved for live website typography. "
        "One ink only: deep olive green #174B35 on pure white #FFFFFF. "
        "High fidelity copperplate and wood-engraving line language: fine directional "
        "cross-hatching follows actual facial volumes, variable line density for "
        "convincing midtones, crisp paper knockout highlights, expressive hair strands, "
        "carefully controlled dark masses. No flat vector shadows, stipple noise, "
        "plastic smoothing, generic face, gold, black, beige, sepia, gradients, "
        "frames, captions, letters, logos, signatures, or text. "
        "Illustration only. No typography baked into the raster image. "
        "Crop must still read at a mobile thumbnail size. "
        "Avoid face distortions, extra glasses rims, doubled features, and "
        "hatching that destroys facial recognition. "
        "Deliver high-detail portrait artwork suitable for a magazine spread."
    )
    return {
        "profile": PROFILE,
        "speaker": slug,
        "referenceImage": str(path),
        "requiresReferenceConditioning": True,
        "requiresIdentityReview": True,
        "requiresHumanArtApproval": True,
        "publishAutomatically": False,
        "artOnly": True,
        "canvas": [1536, 2048],
        "ink": "#174B35",
        "paper": "#FFFFFF",
        "typography": "LIVE_HTML_CSS_ONLY",
        "composition": {
            "portraitCrop": "extreme-asymmetric-left",
            "negativeSpace": "right",
            "focalPoint": "eyes",
            "preserveGlassesAndFacialHair": True
        },
        "prompt": prompt,
        "rejectIf": [
            "identity differs from reference",
            "unreadable face at thumbnail size",
            "fake engraving made from uniform noise",
            "generated text or watermark",
            "palette violates green-white image rule",
            "distorted anatomy or eyeglasses",
            "insufficient negative space for HTML type"
        ]
    }
