#!/usr/bin/env python3
import json,re,urllib.request,uuid,sys
BASE='http://127.0.0.1:8788'
CASES=[
 '請用繁體中文簡短說明約書亞記第三章的核心事件。',
 '請繼續用繁體中文說明約旦河斷流與亞當城的關係。',
 '請用繁體中文比較烏陵與土明，不要切換語言。',
 '請解釋為什麼耶穌受試探時引用申命記六至八章。',
 '請用繁體中文總結前面四個問題，每點一句。',
 '現在談網站設計：請用繁體中文說明什麼是資訊層級。',
 '請繼續，只談排版，不要談模型本身。',
 '請用繁體中文回答：你目前使用哪個本地推理引擎？',
 '請回憶本輪第一個問題的主題，仍只用繁體中文回答。',
 '最後請用繁體中文總結這輪對話，不要加入任何其他文字系統。',
]
# Kana, Thai, Hangul. Han characters are valid Chinese and therefore not flagged.
BAD=re.compile(r'[\u3040-\u30ff\u0e00-\u0e7f\uac00-\ud7af]')
cid='language-acceptance-'+str(uuid.uuid4())
rows=[]
for i,q in enumerate(CASES,1):
 data=json.dumps({'message':q,'conversation_id':cid,'project_id':'dore-search'}).encode()
 req=urllib.request.Request(BASE+'/chat',data=data,headers={'Content-Type':'application/json'})
 try: out=json.loads(urllib.request.urlopen(req,timeout=300).read())
 except Exception as e: rows.append({'turn':i,'ok':False,'error':str(e)}); break
 answer=str(out.get('answer') or out.get('response') or '')
 chars=BAD.findall(answer)
 rows.append({'turn':i,'ok':not chars,'unexpected_chars':chars[:40],'answer':answer})
report={'schema':'dore.language-acceptance.v1','conversation_id':cid,'turns':rows,'pass':len(rows)==len(CASES) and all(x.get('ok') for x in rows)}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['pass'] else 1)
