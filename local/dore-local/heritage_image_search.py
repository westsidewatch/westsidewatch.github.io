#!/usr/bin/env python3
"""Free/open image discovery with provenance-first, production-safe results."""
from __future__ import annotations
import argparse,json,urllib.parse,urllib.request

ENDPOINT='https://api.openverse.org/v1/images/'
ALLOWED={'cc0','pdm','by','by-sa'}

def _request(url:str,timeout:int=20)->dict:
 # HTTP header values stay ASCII-only: some edge security layers reject the
 # accented product name before the request reaches Openverse.
 req=urllib.request.Request(url,headers={'User-Agent':'Dore-Image-Studio/0.1 (+https://westsidewatch.github.io)'})
 with urllib.request.urlopen(req,timeout=timeout) as response:return json.load(response)

def normalize(item:dict)->dict|None:
 license_id=str(item.get('license') or '').lower()
 if license_id not in ALLOWED:return None
 landing=item.get('foreign_landing_url')
 if not landing:return None
 return {
  'id':item.get('id'),'title':item.get('title'),'creator':item.get('creator'),
  'creator_url':item.get('creator_url'),'provider':item.get('provider'),
  'source':item.get('source'),'source_url':landing,'image_url':item.get('url'),
  'thumbnail':item.get('thumbnail'),'width':item.get('width'),'height':item.get('height'),
  'license':license_id,'license_version':item.get('license_version'),
  'license_url':item.get('license_url'),'attribution':item.get('attribution'),
  'rights_status':'discovered_unverified','production_approved':False,
  'required_next_gate':'verify license and provenance on original source item page'
 }

def search(query:str,limit:int=12,requester=_request)->dict:
 query=query.strip()
 if not query:raise ValueError('empty_query')
 limit=max(1,min(int(limit),20))
 params=urllib.parse.urlencode({'q':query,'page_size':limit,'license':','.join(sorted(ALLOWED))})
 raw=requester(ENDPOINT+'?'+params);results=[]
 for item in raw.get('results') or []:
  row=normalize(item)
  if row:results.append(row)
 return {'schema':'dore.heritage-image-search.v1','ok':True,'capability':'heritage.maps-images','provider':'openverse','query':query,'result_count':len(results),'results':results,'provenance_preserved':True,'production_approved':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('query');p.add_argument('--limit',type=int,default=12);a=p.parse_args()
 print(json.dumps(search(a.query,a.limit),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
