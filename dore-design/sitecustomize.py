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
    _atlas_previous_render = _mp.render_canvas

    def _atlas_render(page_id="homepage", edit=False):
        if page_id == _atlas_id:
            return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body,iframe{margin:0;width:100%;height:100%;border:0}body{overflow:hidden}</style></head><body><iframe src="/dore-design/italian-editorial-atlas.html" title="Italian Editorial Atlas"></iframe></body></html>'
        return _atlas_previous_render(page_id, edit=edit)

    _mp.render_canvas = _atlas_render

    if 'data-page="italian-editorial-atlas"' not in _mp.EDITOR_HTML:
        _entry = '<button class="page" data-page="italian-editorial-atlas"><span class="page-dot"></span><span>Italian Editorial Atlas / 義大利編輯圖譜</span></button>'
        _anchor = '<button class="page" data-page="journal-vol-00">'
        if _anchor in _mp.EDITOR_HTML:
            _mp.EDITOR_HTML = _mp.EDITOR_HTML.replace(_anchor, _entry + _anchor, 1)
        else:
            _mp.EDITOR_HTML = _mp.EDITOR_HTML.replace('</aside>', _entry + '</aside>', 1)

    _mp.EDITOR_HTML = _mp.EDITOR_HTML.replace(
        "'journal-vol-00'])",
        "'journal-vol-00','italian-editorial-atlas'])",
        1,
    )
except Exception:
    pass
