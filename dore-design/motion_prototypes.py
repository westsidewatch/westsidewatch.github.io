"""Motion route now points to the new site-native Codrops 8:5 lab.

Runtime installation is intentionally idempotent: an existing motion page is
never rewritten merely because the resident process restarted.
"""
import codrops_site_8x5 as _codrops

PAGE_ID=_codrops.PAGE_ID
install_editor=_codrops.install_editor
render=_codrops.render


def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        if not any(p.get('id')==PAGE_ID for p in w.get('pages',[])):
            w['pages'].append(_codrops._page())
            w=base.save(w)
        return w
    base.workspace=workspace


def render_p1(edit=False):
    return render(edit=edit)
