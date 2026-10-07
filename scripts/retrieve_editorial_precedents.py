#!/usr/bin/env python3
"""Retrieve traceable real editorial precedents from Doré's canonical evidence atlas."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"static/dore-design/italian-editorial-evidence.v1.json"

FAMILY_HINTS={
 "full-bleed":["architectural construction","object as world","subject structure becomes page structure"],
 "asymmetric-split":["asymmetrical hierarchy","free spatial balance","controlled break"],
 "negative-space":["deliberate negative space","paper-like restraint","controlled contrast"],
 "portrait-inset":["documentary anchor plus graphic intervention","precise crop","observational inhabitation"],
 "extreme-crop":["decisive scale shift","precise crop","object as world"],
 "typographic-no-portrait":["type as image","asymmetrical hierarchy","rigor and clarity","multi-scale information hierarchy"]
}

def load():return json.loads(E.read_text(encoding="utf-8"))["items"]

def retrieve(family,limit=4):
 hints=FAMILY_HINTS.get(family,[])
 ranked=[]
 for x in load():
  hay=set(x.get("tokens",[]))
  hits=[h for h in hints if h in hay]
  if hits: ranked.append((len(hits),x))
 ranked.sort(key=lambda z:(-z[0],z[1]["id"]))
 return [{"id":x["id"],"label":x["label"],"source":x["source"],"image":x.get("image"),
          "authority":x.get("authority"),"whatToNotice":x.get("whatToNotice"),"matchedTokens":hits}
         for _,x in ranked[:limit] for hits in [[h for h in hints if h in set(x.get("tokens",[]))]]]

def main():
 p=argparse.ArgumentParser();p.add_argument("--family",required=True,choices=sorted(FAMILY_HINTS));p.add_argument("--limit",type=int,default=4);a=p.parse_args()
 print(json.dumps({"schema":"dore.editorial-precedents.v1","family":a.family,"items":retrieve(a.family,a.limit)},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
