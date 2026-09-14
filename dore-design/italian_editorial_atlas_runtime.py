"""Install Italian Editorial Atlas into the live Doré Design resident."""

PAGE_ID = 'italian-editorial-atlas'
PAGE_NAME = 'Italian Editorial Atlas / 義大利編輯圖譜'


def install(current):
    base = current.visual.base
    mp = current.multipage_wysiwyg

    workspace = base.workspace()
    if not any(p.get('id') == PAGE_ID for p in workspace.get('pages', [])):
        workspace.setdefault('pages', []).append({
            'id': PAGE_ID,
            'name': PAGE_NAME,
            'path': '/dore-design/italian-editorial-atlas.html',
            'kind': 'design-research',
            'canvas': {'w': 1200, 'h': 930},
            'nodes': [],
        })
        base.save(workspace)

    mp.SUPPORTED.add(PAGE_ID)
    previous = mp.render_canvas

    def render_canvas(page_id='homepage', edit=False):
        if page_id == PAGE_ID:
            return '<!doctype html><html><body style="margin:0"><iframe src="/dore-design/italian-editorial-atlas.html" style="border:0;width:100vw;height:100vh" title="Italian Editorial Atlas"></iframe></body></html>'
        return previous(page_id, edit=edit)

    mp.render_canvas = render_canvas

    marker = "<script>supported.add('italian-editorial-atlas')</script>"
    if marker not in mp.EDITOR_HTML:
        mp.EDITOR_HTML = mp.EDITOR_HTML.replace('</body>', marker + '</body>', 1)
