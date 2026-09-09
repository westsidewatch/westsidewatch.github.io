#!/usr/bin/env python3
"""Deterministic self-test for the lightweight Doré template layer."""
import copy
import homepage_candidates
import template_library

rows=template_library.list_templates()
assert rows['ok'] and rows['count']==3, rows
assert {x['source_page_id'] for x in rows['templates']}==set(homepage_candidates.PAGES), rows

class Base:
    def __init__(self):
        self.w={'revision':7,'pages':[{'id':pid,'name':name,'canvas':{'w':1200,'h':930},'nodes':[{'id':'home-title','type':'text','text':'Template','x':1,'y':2,'w':300}]} for pid,(name,_) in homepage_candidates.PAGES.items()]}
    def workspace(self):return copy.deepcopy(self.w)
    def save(self,w):
        w=copy.deepcopy(w);w['revision']+=1;self.w=w;return copy.deepcopy(w)
class Multi:
    SUPPORTED=set(homepage_candidates.PAGES)

base=Base();pages_before=len(base.w['pages'])
first=rows['templates'][0]
result=template_library.instantiate(base,homepage_candidates,Multi,first['id'])
assert result['ok'] and result['detached_copy'] and result['revision']==8,result
assert len(base.w['pages'])==pages_before+1
page=next(p for p in base.w['pages'] if p['id']==result['page_id'])
assert page['template_id']==first['id'] and page['template_source_page_id']==first['source_page_id'] and page['template_detached'] is True
assert result['page_id'] in Multi.SUPPORTED and result['page_id'] in homepage_candidates.PAGES
source=next(p for p in base.w['pages'] if p['id']==first['source_page_id'])
page['nodes'][0]['text']='Detached edit'
assert source['nodes'][0]['text']=='Template'
print('DORE_TEMPLATE_LIBRARY_SELFTEST_PASS')
