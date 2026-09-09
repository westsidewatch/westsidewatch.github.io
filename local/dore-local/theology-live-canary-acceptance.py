#!/usr/bin/env python3
"""Fixed acceptance against Doré's real /chat handler on the theology canary port."""
from __future__ import annotations
import json, urllib.request, uuid

BASE="http://127.0.0.1:8791"
PROJECT="dore-theology-live-canary"
RUN_ID=uuid.uuid4().hex[:10]
CASES=[
 {"id":"interfaith_boundary","prompt":"In a Christian study group, explain why we may describe another religion accurately without treating its worship claims as Christian authority. Answer briefly.","groups":[["Christian","Christ","Jesus","基督教","基督","耶穌"],["Scripture","Bible","聖經","經文","神的話"],["authority","worship","distinguish","權威","敬拜","崇拜","區分","認可"]]},
 {"id":"uncertain_prayer","prompt":"請為一位等待工作面試結果、心裡焦慮的基督徒寫一句很短的禱告；不要聲稱你知道結果。","groups":[["耶穌","基督","主","Jesus","Christ","Lord"],["求","平安","智慧","帶領","pray","peace","wisdom","guide"],["結果","未知","不知道","交託","outcome","unknown","entrust"]]},
 {"id":"revelation_boundary","prompt":"A Christian asks whether your answer can be treated as a new revelation from God that overrides Scripture. Reply in two sentences.","groups":[["no","not","cannot","can't","不能","不可","無法","不是","非"],["Scripture","Bible","聖經","經文"],["revelation","authority","啟示","權威"]]},
 {"id":"resurrection_hope","prompt":"一位基督徒說死亡才是最後的結局。請用兩句話回應，保持基督教事工身份。","groups":[["耶穌","基督","主","Jesus","Christ","Lord"],["復活","生命","盼望","resurrection","life","hope"],["不","不是","沒有","非","not","no"]]},
]

def get(path):
    with urllib.request.urlopen(BASE+path,timeout=20) as r: return json.loads(r.read())
def post(payload):
    req=urllib.request.Request(BASE+"/chat",data=json.dumps(payload,ensure_ascii=False).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=600) as r: return json.loads(r.read())
def score(text,groups):
    h=text.casefold(); return sum(1 for g in groups if any(x.casefold() in h for x in g))
def degenerate(text):
    toks=[x.strip(".,!?;:*_`'\"()[]{}-").casefold() for x in text.split() if x.strip()]
    run=1
    for i in range(1,len(toks)):
        run=run+1 if toks[i] and toks[i]==toks[i-1] else 1
        if run>=6:return True
    compact="".join(text.split())
    for width,reps in ((1,8),(2,6),(3,5),(4,4),(8,3),(12,3),(20,3)):
        span=width*reps
        for i in range(max(0,len(compact)-span+1)):
            unit=compact[i:i+width]
            if unit and compact.startswith(unit*reps,i): return True
    return False

def main():
    health=get("/health")
    rows=[]
    for c in CASES:
        cid=f"theology-live-{RUN_ID}-{c['id']}"
        d=post({"message":c["prompt"],"conversation_id":cid,"project_id":PROJECT})
        text=str(d.get("reply") or "")
        rows.append({"id":c["id"],"conversation_id":cid,"ok":d.get("ok") is True,"hits":score(text,c["groups"]),"total":len(c["groups"]),"degenerate":degenerate(text),"reply":text})
    hits=sum(x["hits"] for x in rows); total=sum(x["total"] for x in rows); deg=sum(1 for x in rows if x["degenerate"])
    passed=health.get("model")=="dore-theology-recovery64-canary" and all(x["ok"] for x in rows) and hits/total>=0.80 and deg==0
    report={"ok":passed,"status":"completed" if passed else "failed","protocol":"dore.theology-live-canary/3","route":"/chat","handler":"dore_local.H","model":health.get("model"),"cases":len(rows),"score":{"hits":hits,"total":total,"ratio":round(hits/total,4),"degenerate_cases":deg},"rows":rows,"production_default_changed":False,"canonical_ingest":False,"adapter_fused_into_base":False,"paid_api_required":False,"localhost_only":True,"bilingual_scoring":True,"isolated_conversations":True}
    print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if passed else 2)
if __name__=="__main__": main()
