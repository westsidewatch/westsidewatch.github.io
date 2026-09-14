"""Boot-time registration for the standalone Third Alive Design experiment.

This intentionally registers a separate Design page and does not modify
Candidate 01 or its locked first-layer homepage structure.
"""

try:
    import app_visual as _visual
    import multipage_wysiwyg as _mp
    import living_water_third_alive_lab as _third

    # Register a real workspace page so it appears as its own Design page.
    _workspace = _visual.base.workspace()
    _pages = _workspace.setdefault("pages", [])
    if not any(p.get("id") == _third.PAGE_ID for p in _pages):
        _pages.append({
            "id": _third.PAGE_ID,
            "name": _third.PAGE_TITLE,
            "path": "/experiments/living-water-third-alive/",
            "kind": "design-experiment",
            "design_experiment": {
                "status": "lab",
                "scope": "standalone",
                "concept": "third-alive-4w-weighted-length-navigation",
                "candidate_01_untouched": True,
                "movements": ["WATCH", "WITNESS", "WALK", "WORSHIP"],
                "atomic_unit": "5:8",
                "weights": [1, 2, 3],
            },
        })
        _workspace["revision"] = int(_workspace.get("revision", 0)) + 1
        _visual.base.save_workspace(_workspace)

    # Make the page a first-class editor target. app_visual_v2 later wraps the
    # current renderer and falls through to this renderer for unknown pages.
    _mp.SUPPORTED.add(_third.PAGE_ID)
    _previous_render = _mp.render_canvas

    def _third_alive_render(page_id="homepage", edit=False):
        if page_id == _third.PAGE_ID:
            return _third.render(edit=edit)
        return _previous_render(page_id, edit=edit)

    _mp.render_canvas = _third_alive_render

    # Add one independent sidebar entry; no insertion into Candidate 01.
    if _third.PAGE_ID not in _mp.EDITOR_HTML:
        _anchor = '<button class="page" data-page="living-water-second-layer-lab">'
        _entry = (
            '<button class="page" data-page="' + _third.PAGE_ID + '">'
            '<span class="page-dot"></span><span>' + _third.PAGE_TITLE + '</span></button>'
        )
        if _anchor in _mp.EDITOR_HTML:
            _mp.EDITOR_HTML = _mp.EDITOR_HTML.replace(_anchor, _entry + _anchor, 1)
        else:
            _mp.EDITOR_HTML = _mp.EDITOR_HTML.replace('</aside>', _entry + '</aside>', 1)
except Exception:
    # Never block Design startup if an experimental registration cannot load.
    pass
