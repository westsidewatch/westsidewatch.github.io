#!/usr/bin/env python3
"""Resolve known site routes and page metadata to Doré editorial scenarios.

Fail closed on ambiguous routes: never silently guess a person's identity or
section palette from a generic page name.
"""
import argparse,json,re
from pathlib import Path

ROUTES={
 '/journal/':('essay-concept','feature-lead',None),
 '/archive/':('archive-thumbnail','thumbnail',None),
 '/magazine/':('essay-concept','feature-lead',None),
 '/cinema/':('cinema-program','hero',None),
 '/olive-mountain/':('section-hero','hero','olive-mountain'),
 '/church/':('section-hero','hero',None),
 '/olive/':('section-hero','hero','olive-mountain'),
}
LAYOUT_SLOTS={'hero':'hero','cover':'cover','feature':'feature-lead','feature-lead':'feature-lead',
              'inline':'inline','profile':'profile-card','profile-card':'profile-card',
              'thumbnail':'thumbnail','card':'profile-card'}
def normalize(path):
 path='/'+path.strip().strip('/')+'/'
 return re.sub('/+','/',path)
def parse_frontmatter(path):
 data=Path(path).read_text(encoding='utf-8')
 if not data.startswith('---\n'):return {}
 m=re.match(r'^---\n(.*?)\n---',data,re.S)
 if not m:return {}
 out={}
 for line in m.group(1).splitlines():
  pair=re.match(r'^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$',line)
  if pair:out[pair.group(1)]=pair.group(2).strip().strip('"\'')
 return out
def resolve(route,frontmatter=None):
 route=normalize(route)
 fm=frontmatter or {}
 base=ROUTES.get(route)
 scenario=fm.get('dore_scenario') or (base[0] if base else None)
 slot=fm.get('dore_slot') or (base[1] if base else None)
 palette=fm.get('dore_palette') or (base[2] if base else None)
 if not scenario or not slot:
  raise ValueError('No explicit editorial route mapping: '+route+
                   '. Set dore_scenario, dore_slot and dore_palette in front matter or mapping.')
 from dore_editorial_scenarios import SCENARIOS,SLOTS
 if scenario not in SCENARIOS:raise ValueError('Unknown scenario: '+scenario)
 if slot not in SLOTS:raise ValueError('Unknown slot: '+slot)
 if not palette:
  raise ValueError('No verified section palette for '+route+
                   '. Set dore_palette explicitly; do not default to Olive Mountain.')
 from compile_dore_editorial_brief import PALETTES
 if palette not in PALETTES:raise ValueError('Palette not implemented: '+palette)
 return {'route':route,'scenario':scenario,'slot':slot,'palette':palette,
         'source':'frontmatter+route-registry','needs_visual_review':True}
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--route',required=True)
 p.add_argument('--content-file')
 a=p.parse_args()
 print(json.dumps(resolve(a.route,parse_frontmatter(a.content_file) if a.content_file else None),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
