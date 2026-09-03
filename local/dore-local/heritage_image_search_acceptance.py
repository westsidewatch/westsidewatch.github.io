#!/usr/bin/env python3
from heritage_image_search import search

def fixture(_url):
 return {'results':[
  {'id':'ok','title':'Morning star engraving','creator':'Archive','provider':'wikimedia','source':'wikimedia','foreign_landing_url':'https://example.test/item/ok','url':'https://example.test/ok.jpg','thumbnail':'https://example.test/t.jpg','width':1200,'height':1600,'license':'cc0','license_url':'https://creativecommons.org/publicdomain/zero/1.0/'},
  {'id':'bad','title':'Restricted','foreign_landing_url':'https://example.test/item/bad','license':'by-nc'},
  {'id':'missing-source','title':'No original page','license':'cc0'}]}
r=search('morning star engraving',requester=fixture)
assert r['ok'] and r['capability']=='heritage.maps-images'
assert r['result_count']==1 and r['results'][0]['id']=='ok'
assert r['results'][0]['production_approved'] is False
assert r['results'][0]['rights_status']=='discovered_unverified'
assert r['results'][0]['source_url'].startswith('https://')
print('DORE_HERITAGE_IMAGE_SEARCH_ACCEPTANCE=PASS')
