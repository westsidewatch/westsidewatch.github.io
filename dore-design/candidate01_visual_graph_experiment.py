"""Candidate 01 Visual Graph experiment.

A/B-only visual-source swap. It deliberately leaves Candidate 01 structure,
4W labels, locked current motion, text, focus behaviour and responsive rules
unchanged. The first ONE card remains live and may replace its own image from
ONE data at runtime.
"""

# Only assets whose current Visual Graph / map-profile evidence permits the
# site-facing experiment are used here. This is intentionally not a new visual
# authority store; canonical provenance remains in Dawn Library Visual Graph.
_DORE = "https://commons.wikimedia.org/wiki/Special:Redirect/file/016.The_Testing_of_Abraham%27s_Faith.jpg?width=2303"
_GALILEE = "https://media.artmuseum.princeton.edu/iiif/3/collection/INV33869/full/max/0/default.jpg"
_CHINA = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Child_reading,_while_Pastor_Wang_Lieh-guang_and_missionaries_look_on.jpg?width=1024"
_PEF = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Survey_of_Western_Palestine_1880.17.jpg?width=3840"

# product-1 is ONE and is intentionally left alone because the existing ONE
# runtime replaces it with the chapter illustration. The seven remaining
# cards receive authority-backed visual material. Repetition is deliberate:
# this experiment tests visual weight and motion before expanding the corpus.
_CARD_IMAGES = {
    2: _CHINA,
    3: _PEF,
    4: _GALILEE,
    5: _DORE,
    6: _CHINA,
    7: _PEF,
    8: _GALILEE,
}


def _swap_candidate_visuals(doc):
    base = "https://tympanus.net/Tutorials/GridToFullPreview/assets/products/"
    for index, image_url in _CARD_IMAGES.items():
        # Replace the card image and all three preview representations without
        # touching any DOM structure or motion code.
        for suffix in ("", "-detail-1", "-detail-2"):
            doc = doc.replace(f"{base}product-{index}{suffix}.webp", image_url)
    return doc


def install(current):
    previous_render = current.multipage_wysiwyg.render_canvas

    def render_canvas(page_id="homepage", edit=False):
        doc = previous_render(page_id, edit=edit)
        if page_id == current.living_water_candidate.PAGE_ID:
            return _swap_candidate_visuals(doc)
        return doc

    current.multipage_wysiwyg.render_canvas = render_canvas
