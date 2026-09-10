"""Motion route now points to the new site-native Codrops 8:5 lab."""
from codrops_site_8x5 import PAGE_ID, install_workspace, install_editor, render

def render_p1(edit=False):
    return render(edit=edit)
