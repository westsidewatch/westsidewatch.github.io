"""Source-grounded editorial ink palettes.

Source: static/css/westside-color-authority.css on main, audited 2026-10-08.
These are image-generation ink roles, NOT a replacement for runtime CSS variables.
Olive Mountain's approved green/white editorial image palette intentionally differs
from the generic --ws-olive section anchor.
"""
PALETTES={
 'olive-mountain':{'paper':'#FFFFFF','image_ink':'#174B35','secondary_ink':'#47735E','type_ink':'#174B35','source':'approved Olive Mountain image palette'},
 'magazine':{'paper':'#FAF9F5','image_ink':'#A2872A','secondary_ink':'#D2BC69','type_ink':'#252525','source':'--ws-first-light and --ws-paper'},
 'cinema':{'paper':'#FAF9F5','image_ink':'#A14D57','secondary_ink':'#B8944A','type_ink':'#252525','source':'--ws-crimson, --ws-harvest and --ws-paper'},
 'church':{'paper':'#FAF9F5','image_ink':'#5B8FA8','secondary_ink':'#738A5A','type_ink':'#252525','source':'--ws-water, --ws-olive and --ws-paper'},
 'dawn-library':{'paper':'#FAF9F5','image_ink':'#B8944A','secondary_ink':'#D2BC69','type_ink':'#252525','source':'--ws-harvest and --ws-paper'},
 'bible':{'paper':'#EEE4C9','image_ink':'#252525','secondary_ink':'#CEBD74','type_ink':'#252525','source':'--ws-papyrus and --ws-pale-gold'},
}
def validate_palette(name):
 p=PALETTES[name]
 for role in ('paper','image_ink','secondary_ink','type_ink'):
  assert len(p[role])==7 and p[role].startswith('#'),(name,role)
 return p
