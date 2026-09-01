#!/usr/bin/env python3
"""Idempotently add three editable homepage concept pages to the Doré workspace."""
import copy
import app_workspace as base
from homepage_candidates import PAGES

w=base.workspace();home=base.page(w,'homepage')
if not home:raise SystemExit('homepage_missing')
changed=False
for page_id,(name,_) in PAGES.items():
 p=base.page(w,page_id)
 if not p:
  p=copy.deepcopy(home);p['id']=page_id;p['name']=name;p['renderer']='homepage-candidate';w['pages'].append(p);changed=True
 else:p['name']=name;p['renderer']='homepage-candidate'
if changed:base.save(w)
print({'ok':True,'changed':changed,'pages':[p['id'] for p in w['pages'] if p['id'] in PAGES]})
