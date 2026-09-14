"""Boot-time registration for standalone Doré Design experiment surfaces."""

try:
    import app_visual as _visual
    import multipage_wysiwyg as _mp
    import living_water_third_alive_lab as _third

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

    _mp.SUPPORTED.add(_third.PAGE_ID)
    _previous_render = _mp.render_canvas

    def _third_alive_render(page_id="homepage", edit=False):
        if page_id == _third.PAGE_ID:
            return _third.render(edit=edit)
        return _previous_render(page_id, edit=edit)

    _mp.render_canvas = _third_alive_render

    _atlas_id = "italian-editorial-atlas"
    if not any(p.get("id") == _atlas_id for p in _pages):
        _pages.append({
            "id": _atlas_id,
            "name": "Italian Editorial Atlas / 義大利編輯圖譜",
            "path": "/dore-design/italian-editorial-atlas.html",
            "kind": "design-research",
            "nodes": [],
        })
        _workspace["revision"] = int(_workspace.get("revision", 0)) + 1
        _visual.base.save_workspace(_workspace)

    _mp.SUPPORTED.add(_atlas_id)
    _previous_atlas_render = _mp.render_canvas

    def _atlas_render(page_id="homepage", edit=False):
        if page_id == _atlas_id:
            return '<!doctype html><html><body style="margin:0"><iframe src="/dore-design/italian-editorial-atlas.html" style="border:0;width:100vw;height:100vh"></iframe></body></html>'
        return _previous_atlas_render(page_id, edit=edit)

    _mp.render_canvas = _atlas_render
except Exception:
    pass
