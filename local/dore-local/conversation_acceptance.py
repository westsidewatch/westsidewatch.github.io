#!/usr/bin/env python3
import json, urllib.request, urllib.parse, uuid, time
BASE='http://127.0.0.1:8788'; PROJECT='dore-search'; CID='acceptance-'+uuid.uuid4().hex[:12]

def get(path):
 with urllib.request.urlopen(BASE+path,timeout=20) as r:return json.loads(r.read())
def post(path,payload,timeout=300):
 req=urllib.request.Request(BASE+path,data=json.dumps(payload,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.loads(r.read())

def chat(msg):
 d=post('/chat',{'message':msg,'conversation_id':CID,'project_id':PROJECT})
 return d, str(d.get('reply') or '')

checks=[]; turns=[]
def check(name,ok,detail=''):
 checks.append({'name':name,'pass':bool(ok),'detail':detail[:1000]})

try:
 h=get('/health'); check('health',h.get('ok') is True,json.dumps(h,ensure_ascii=False)); check('gemma-engine',h.get('model')=='gemma4:e4b',str(h.get('model')))
 prompts=[
  '這是持久對話驗收第1輪。請記住代碼 Cedar-731，以及數字37。只需確認你記住。',
  '第2輪：上一輪的代碼和數字是什麼？',
  '第3輪：再記住第二個代碼 Olive-204。請同時告訴我第一個代碼。',
  '第4輪：不要猜。請列出目前兩個代碼，以及第1輪的數字。',
  '第5輪：我們前一輪要求你做了什麼？用一句話回答。',
  '第6輪：請回顧第1輪與第3輪分別新增了什麼記憶。',
  '第7輪：請把目前這段對話濃縮成兩點，但必須保留 Cedar-731、Olive-204 和 37。',
  '第8輪：最終驗收。只根據本對話，輸出 Cedar-731、Olive-204、37，並說明它們分別在哪一輪首次出現。'
 ]
 for i,p in enumerate(prompts,1):
  d,r=chat(p); turns.append({'turn':i,'prompt':p,'reply':r,'ok':d.get('ok')}); check(f'turn-{i}-http',d.get('ok') is True,r)
  if i==2: check('turn-2-recall','Cedar-731' in r and '37' in r,r)
  if i==3: check('turn-3-recall','Cedar-731' in r and 'Olive-204' in r,r)
  if i in (4,7,8): check(f'turn-{i}-deep-recall',all(x in r for x in ('Cedar-731','Olive-204','37')),r)

 q=urllib.parse.urlencode({'project_id':PROJECT,'conversation_id':CID})
 hist=get('/conversation?'+q); msgs=hist.get('messages') or []
 check('history-api',hist.get('ok') is True and len(msgs)>=16,f'messages={len(msgs)}')
 roles=[m.get('role') for m in msgs]
 check('history-role-order',roles[:2]==['user','assistant'] and roles[-2:]==['user','assistant'],str(roles))
 # Simulate leaving the page and reopening later by discarding all client state and re-fetching only by durable id.
 time.sleep(1)
 reopened=get('/conversation?'+q); rmsgs=reopened.get('messages') or []
 check('leave-reopen',len(rmsgs)==len(msgs) and len(rmsgs)>=16,f'before={len(msgs)} after={len(rmsgs)}')
 # Continue after reopen with a ninth turn.
 d9,r9=chat('第9輪：假設我剛離開又回來。請直接告訴我兩個代碼與數字，不要重新猜。')
 turns.append({'turn':9,'prompt':'reopen continuation','reply':r9,'ok':d9.get('ok')}); check('turn-9-after-reopen',d9.get('ok') is True and all(x in r9 for x in ('Cedar-731','Olive-204','37')),r9)
 lst=get('/conversations?'+urllib.parse.urlencode({'project_id':PROJECT})); ids=[x.get('id') for x in (lst.get('conversations') or [])]
 check('conversation-list-reopenable',CID in ids,f'listed={CID in ids}; count={len(ids)}')
 excepted=False
except Exception as e:
 check('uncaught-exception',False,repr(e)); excepted=True

passed=sum(1 for x in checks if x['pass']); result={'schema':'dore.conversation-acceptance.v1','conversation_id':CID,'rounds_attempted':len(turns),'checks_passed':passed,'checks_total':len(checks),'pass':passed==len(checks),'checks':checks,'turns':turns}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['pass'] else 1)
