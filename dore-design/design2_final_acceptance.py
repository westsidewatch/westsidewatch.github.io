#!/usr/bin/env python3
"""Executable final acceptance used by rollout/diagnostics."""
from pathlib import Path
def check(base):
 import design2_closeout_acceptance
 root=Path(__file__).parent
 required=['design2_ui.py','design2_layers_ui.py','design2_arrange_ui.py','design2_layer_ops.py','design2_cover_render.py','design2_cover_interaction.py','design2_typography_ui.py']
 files={p:(root/p).exists() for p in required};close=design2_closeout_acceptance.check(base)
 return {'ok':close['ok'] and all(files.values()),'schema':'dore.design2.final-acceptance.v1','phase':7,'files':files,'closeout':close}
