#!/usr/bin/env python3
"""Idempotently add three editable homepage concept pages to the Doré workspace."""
import copy
import app_workspace as base
from homepage_candidates import PAGES
from promotion_pipeline import registry

w=base.workspace();home=base.page(w,'homepage')
if not home:raise SystemExit('homepage_missing')
changed=False
for page_id,(name,_) in PAGES.items():
 p=base.page(w,page_id)
 if not p:
  p=copy.deepcopy(home);p['id']=page_id;p['name']=name;p['renderer']='homepage-candidate';w['pages'].append(p);changed=True
 else:
  if p.get('name')!=name or p.get('renderer')!='homepage-candidate':changed=True
  p['name']=name;p['renderer']='homepage-candidate'
if changed:base.save(w)
promoted=registry().get('candidates',[])
missing=[x.get('page_id') for x in promoted if not base.page(w,x.get('page_id'))]
if missing:raise SystemExit('promoted_candidate_pages_missing:'+','.join(missing))
print({'ok':True,'changed':changed,'pages':[p['id'] for p in w['pages'] if p['id'] in PAGES],'promoted_candidates':[x.get('id') for x in promoted]})
