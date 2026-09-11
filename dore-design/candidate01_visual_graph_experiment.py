"""Candidate 01 — direct Codrops GridToFullPreview 8:5 resident."""
from __future__ import annotations
import html as html_lib
import design_motion_registry as motion
import codrops_site_8x5


def focus_screen(screen_no, labels):
    # IMPORTANT: Candidate 01 must not wrap, restyle, or augment the motion engine.
    # The resident embeds the verified Codrops-derived 8:5 page directly.
    doc = codrops_site_8x5.render(edit=False)
    srcdoc = html_lib.escape(doc, quote=True)
    return (
        '<section class="candidate-focus-screen" data-current="focus" data-layer="first" '
        'data-screen="%s">'
        '<iframe title="GridToFullPreview 8:5 %s" loading="eager" srcdoc="%s"></iframe>'
        '</section>'
    ) % (screen_no, screen_no - 1, srcdoc)


def install(current):
    motion._candidate_focus_screen = focus_screen
