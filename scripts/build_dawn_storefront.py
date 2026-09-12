#!/usr/bin/env python3
"""Project only reviewed complete books; provider feeds never bypass admission."""
import json,urllib.parse
from datetime import datetime,timezone
from pathlib import Path
from resource_selection import book_allowed,book_decision
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'static/dawn-library/biblical-world/catalog.json'
OUT=ROOT/'static/dawn-library/storefront.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-STOREFRONT.json'

def build():
    groups={}
    for book in json.loads(CAT.read_text()).get('items',[]):
        if not book_allowed(book):continue
        work=book['work'];source=next((s for s in book.get('sources',[]) if s.get('url')),None)
        if not source:continue
        provider=source['provider'];url=source['url'];rights=book.get('rights',{})
        item={'id':book['id'],'title':work['title'],'author':work.get('author',''),'language':work.get('language',''),
            'source':{'provider':provider,'url':url,'kind':'reviewed-book','catalogId':book['id']},
            'cover':book.get('cover',{'mode':'one-fallback'}),'rights':rights,
            'quality':'reviewed-complete-book','admission':book_decision(book),'contentDownloaded':False}
        if provider=='中文維基文庫' and rights.get('status')=='public-domain':
            page=urllib.parse.unquote(url.split('/wiki/',1)[-1]).replace('_',' ')
            item['source']['downloadUrl']='https://ws-export.wmcloud.org/?'+urllib.parse.urlencode({'format':'epub','lang':'zh','page':page})
        groups.setdefault(provider,[]).append(item)
    shelves=[{'id':'reviewed-'+str(i),'title':provider+' · 核定書籍','kind':'reviewed-book-shelf','source':provider,'items':items} for i,(provider,items) in enumerate(groups.items())]
    items=[b for s in shelves for b in s['items']];now=datetime.now(timezone.utc).isoformat()
    metrics={'shelves':len(shelves),'mappedBooks':len(items),'sourceCovers':sum(bool(i.get('cover',{}).get('url')) for i in items),'directPublications':sum(bool(i['source'].get('downloadUrl')) for i in items),'providers':{k:len(v) for k,v in groups.items()},'identity':{'resolved':0}}
    data={'schema':'dawn.library.storefront.v3','generatedAt':now,'title':'黎明書局','storagePolicy':'index-only','principle':'先確認內容與書籍身分，再選取；不以數量換取館藏。','shelves':shelves,'metrics':metrics,'errors':[]}
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    REPORT.write_text(json.dumps({'schema':'dawn.library.storefront.report.v5','generatedAt':now,**metrics,'contentDownloaded':False,'admission':'reviewed-complete-books-only'},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(metrics,ensure_ascii=False))
if __name__=='__main__':build()
