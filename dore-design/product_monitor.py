#!/usr/bin/env python3
"""Doré Design product invariant monitor used by coordination receipts."""
from __future__ import annotations
import json,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE='http://127.0.0.1:4310'

def get_text(path):
    try:
        return urllib.request.urlopen(BASE+path,timeout=8).read().decode('utf-8','replace'),200
    except urllib.error.HTTPError as e:
        return '',e.code
    except Exception:
        return '',0

def get_bytes(path):
    try:
        return urllib.request.urlopen(BASE+path,timeout=8).read(),200
    except urllib.error.HTTPError as e:
        return b'',e.code
    except Exception:
        return b'',0

def main():
    source=(ROOT/'layouts/index.html').read_text(encoding='utf-8') if (ROOT/'layouts/index.html').exists() else ''
    journal,journal_status=get_text('/journal/')
    wall,wall_status=get_bytes('/images/jerusalem-wall.png')
    expected='images/jerusalem-wall.png'
    checks={
        'journal_live':journal_status==200,
        'cover_wall_required_by_source':expected in source,
        'cover_wall_dom_present':'hero__wall' in journal,
        'cover_wall_reference_present':'jerusalem-wall.png' in journal,
        'cover_wall_asset_served':wall_status==200 and len(wall)>100,
    }
    alerts=[]
    if checks['cover_wall_required_by_source'] and not checks['cover_wall_asset_served']:
        alerts.append({'code':'JOURNAL_COVER_ASSET_MISSING','severity':'warning','asset':'/images/jerusalem-wall.png','http_status':wall_status})
    if checks['cover_wall_required_by_source'] and not checks['cover_wall_reference_present']:
        alerts.append({'code':'JOURNAL_COVER_ASSET_NOT_BOUND','severity':'warning','asset':'/images/jerusalem-wall.png'})
    status='PASS' if not alerts else 'WARN'
    print(json.dumps({'ok':True,'product_monitor':status,'journal_cover_wall':checks,'alerts':alerts},ensure_ascii=False))

if __name__=='__main__':main()
