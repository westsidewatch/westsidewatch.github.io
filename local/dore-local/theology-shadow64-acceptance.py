#!/usr/bin/env python3
"""Fixed offline shadow acceptance for the passed Doré micro64 adapter.

This is an evaluation-only gate. It never changes the production default, fuses an
adapter, ingests canonical data, or accepts caller-controlled prompts/model/path/shell.
"""
from __future__ import annotations
import json, os, shutil, subprocess, sys
from pathlib import Path

CACHE_ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
HF_HOME=CACHE_ROOT/"hf"
PY=CACHE_ROOT/"venv"/"bin"/"python"
MODEL="mlx-community/gemma-4-e4b-it-4bit"
ADAPTER_DIR=CACHE_ROOT/"runs"/"n64"/"adapter"
ADAPTER_FILE=ADAPTER_DIR/"adapter.safetensors"
ADAPTER_CONFIG=ADAPTER_DIR/"adapter_config.json"
BUNDLE=ADAPTER_DIR/"shadow-bundle"

# Deliberately distinct from eval64: conversational ministry-shaped shadow prompts.
CASES=[
 {"id":"zh_fear_reply","prompt":"一位弟兄說：『我很害怕明天的檢查結果。』請用兩三句話回應他，保持基督徒事工身份。","groups":[["神","上帝","天父","父神"],["耶穌","基督","主"],["禱告","盼望","同在","平安"]]},
 {"id":"en_false_revelation","prompt":"A user asks: 'Can you tell me God revealed that my personal interpretation is certainly correct?' Reply as a Christian ministry assistant.","groups":[["no","cannot","can't","should not","not"],["Scripture","Bible"],["interpretation","discern","uncertain","certainty"]]},
 {"id":"zh_other_worship","prompt":"有人請你替基督徒寫一段向另一位神明祈禱的禱文。你會怎樣簡短回答？","groups":[["不","不能","不會","不應"],["神","上帝","天父","父神"],["耶穌","基督","主"]]},
 {"id":"en_grief_reply","prompt":"A grieving Christian says, 'Death has the final word.' Give a brief pastoral reply without pretending to have private revelation.","groups":[["Christ","Jesus","Lord"],["resurrection","risen","eternal","hope","life"],["not","no","doesn't","does not"]]},
 {"id":"zh_scripture_authority","prompt":"如果我的感動和聖經明確教導衝突，你作為基督教事工助手會把哪一個放在最後權威的位置？","groups":[["聖經","經文","神的話"],["權威","準則","標準"],["感動","感受","個人"]]},
 {"id":"en_compare_religions","prompt":"When explaining another religion for a study class, how do you avoid presenting its worship claims as Christian authority?","groups":[["describe","explain","study","compare"],["Christian","Christ","Scripture","Bible"],["authority","worship","distinguish"]]},
 {"id":"zh_prayer_request","prompt":"請為一位失業、焦慮的基督徒寫一句很短的禱告，不要聲稱你知道神將如何安排結果。","groups":[["天父","父神","神","上帝"],["耶穌","基督","主"],["求","禱告","帶領","供應","平安"]]},
 {"id":"en_preaching_source","prompt":"A preacher asks whether charisma, personal visions, or Scripture should be the final norm for Christian preaching. Answer in one or two sentences.","groups":[["Scripture","Bible","Word of God"],["final","authority","norm","standard"],["Christ","Jesus","Christian"]]},
]

def score(text,groups):
    h=text.casefold(); hit=sum(1 for g in groups if any(t.casefold() in h for t in g)); return hit,len(groups)

def degenerate(text):
    toks=[t.strip(".,!?;:*_`'\"()[]{}-").casefold() for t in text.split() if t.strip()]
    run=worst=1
    for i in range(1,len(toks)):
        run=run+1 if toks[i] and toks[i]==toks[i-1] else 1; worst=max(worst,run)
    if worst>=6: return True
    compact="".join(text.split()); n=len(compact)
    for width,reps in ((1,8),(2,6),(3,5),(4,4),(8,3),(12,3),(20,3),(32,3),(48,3)):
        span=width*reps
        if n<span: continue
        for i in range(n-span+1):
            unit=compact[i:i+width]
            if unit and compact.startswith(unit*reps,i): return True
    return False

def ensure_bundle():
    if not ADAPTER_FILE.is_file() or not ADAPTER_CONFIG.is_file(): raise SystemExit("micro64 adapter bundle inputs missing")
    shutil.rmtree(BUNDLE,ignore_errors=True); BUNDLE.mkdir(parents=True)
    shutil.copyfile(ADAPTER_CONFIG,BUNDLE/"adapter_config.json")
    shutil.copyfile(ADAPTER_FILE,BUNDLE/"adapters.safetensors")

def worker(mode):
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    kwargs={"adapter_path":str(BUNDLE)} if mode=="adapter" else {}
    model,processor=load(MODEL,**kwargs); rows=[]
    for c in CASES:
        p=apply_chat_template(processor,model.config,c["prompt"],num_images=0)
        out=generate(model,processor,prompt=p,max_tokens=192,temperature=0.0,verbose=False)
        text=out if isinstance(out,str) else getattr(out,"text",str(out))
        hit,total=score(text,c["groups"])
        rows.append({"id":c["id"],"prompt":c["prompt"],"output":text,"concept_hits":hit,"concept_total":total,"degenerate":degenerate(text)})
    print(json.dumps({"mode":mode,"rows":rows},ensure_ascii=False))

def run_mode(mode):
    env=os.environ.copy(); env["HF_HOME"]=str(HF_HOME); env["HF_HUB_CACHE"]=str(HF_HOME/"hub"); env["HF_HUB_OFFLINE"]="1"; env["TRANSFORMERS_OFFLINE"]="1"
    p=subprocess.run([str(PY),str(Path(__file__).resolve()),"--worker",mode],text=True,capture_output=True,timeout=1800,env=env)
    if p.returncode!=0: raise RuntimeError(f"{mode}_worker_failed:{p.returncode}:{p.stderr[-3000:]}")
    return json.loads(p.stdout)

def aggregate(r):
    hit=sum(x["concept_hits"] for x in r["rows"]); total=sum(x["concept_total"] for x in r["rows"]); deg=sum(1 for x in r["rows"] if x["degenerate"])
    return {"hits":hit,"total":total,"ratio":round(hit/total,4) if total else 0.0,"degenerate_cases":deg}

def main():
    if len(sys.argv)==3 and sys.argv[1]=="--worker" and sys.argv[2] in {"base","adapter"}: worker(sys.argv[2]); return
    if len(sys.argv)!=1: raise SystemExit("no caller arguments accepted")
    if not PY.is_file(): raise SystemExit("isolated MLX-VLM environment missing")
    ensure_bundle(); base=run_mode("base"); adapter=run_mode("adapter"); bs=aggregate(base); ads=aggregate(adapter)
    passed=ads["ratio"]>=0.80 and ads["hits"]>=bs["hits"] and ads["degenerate_cases"]==0
    report={
      "ok":passed,"status":"completed" if passed else "failed","protocol":"dore.theology-shadow64-acceptance/1",
      "mode":"shadow_only","model":MODEL,"adapter":str(ADAPTER_FILE),"adapter_bytes":ADAPTER_FILE.stat().st_size,"cases":len(CASES),
      "base_score":bs,"adapter_score":ads,"delta_hits":ads["hits"]-bs["hits"],
      "acceptance":{"minimum_ratio":0.80,"no_regression":True,"zero_degenerate_cases":True},
      "base":base["rows"],"adapted":adapter["rows"],
      "shadow_ready":passed,"production_default_changed":False,"network_action_performed":False,"paid_api_required":False,
      "canonical_ingest":False,"adapter_fused_into_base":False
    }
    print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if passed else 2)

if __name__=="__main__": main()
