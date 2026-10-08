#!/usr/bin/env python3
"""Generate a temporary Hugo content overlay for testing Doré in the real site layout.

Never modifies production content, config or templates. Uses Hugo's existing
surface-carrier template and loads existing site CSS through baseof.html.
"""
import argparse,json,re
from pathlib import Path

SAFE_ROUTE=re.compile(r'^/[a-z0-9][a-z0-9/_-]*/$')
def render_frontmatter(spec,asset,title):
 route=spec['page_resolution']['route'] if spec.get('page_resolution') else None
 if not route or not SAFE_ROUTE.fullmatch(route):
  raise ValueError('A resolved canonical route is required for a Hugo proof')
 if route not in ('/olive/','/cinema/','/church/','/journal/','/dawn-library/','/one/'):
  raise ValueError('Route not yet approved for template proof: '+route)
 if not re.fullmatch(r'[a-zA-Z0-9._/-]+',asset) or '..' in asset:
  raise ValueError('Unsafe asset path')
 # Standalone test page under the original section; actual production CSS and base layout.
 section=route.strip('/')
 safe_title=json.dumps(title,ensure_ascii=False)
 content='''---
title: %s
layout: "dore-proof"
draft: false
url: "/%s/dore-proof/"
dore_image: "/%s"
dore_palette: "%s"
dore_slot: "%s"
---
'''%(safe_title,section,asset,spec['palette'],spec['slot'])
 return section,content
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--spec',required=True)
 p.add_argument('--image',required=True)
 p.add_argument('--title',default='EDITORIAL')
 p.add_argument('--out',default='local/dore-hugo-overlay')
 a=p.parse_args()
 spec=json.loads(Path(a.spec).read_text(encoding='utf-8'))
 image=Path(a.image)
 if not image.is_file():p.error('image missing')
 section,content=render_frontmatter(spec,'dore-proof/'+image.name,a.title)
 out=Path(a.out);page=out/'content'/section/'dore-proof.md'
 page.parent.mkdir(parents=True,exist_ok=True)
 page.write_text(content,encoding='utf-8')
 import shutil
 target=out/'static'/'dore-proof'/image.name
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(image,target)
 print(page)
if __name__=='__main__':main()
