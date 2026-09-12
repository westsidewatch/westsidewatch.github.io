"""Motion route now points to the new site-native Codrops 8:5 lab."""
import codrops_site_8x5 as _codrops

PAGE_ID=_codrops.PAGE_ID
install_editor=_codrops.install_editor
render=_codrops.render


def install_workspace(base):
    """Register the motion page without mutating workspace revision on reads.

    The original Codrops installer rewrote the existing page and called save()
    on every base.workspace() access. That made a plain GET advance revision and
    caused Phase 4 candidate creation to see a stale revision immediately after
    reading it. Runtime rendering already comes from this module, so the
    workspace only needs a stable page registration.
    """
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
