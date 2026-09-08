#!/usr/bin/env python3
"""Fixed offline base-vs-micro64 held-out evaluation with degeneration guard."""
from __future__ import annotations
import json, os, shutil, subprocess, sys
from pathlib import Path
CACHE_ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
HF_HOME=CACHE_ROOT/"hf"; PY=CACHE_ROOT/"venv"/"bin"/"python"; MODEL="mlx-community/gemma-4-e4b-it-4bit"
ADAPTER_DIR=CACHE_ROOT/"runs"/"n64"/"adapter"; ADAPTER_FILE=ADAPTER_DIR/"adapter.safetensors"; ADAPTER_CONFIG=ADAPTER_DIR/"adapter_config.json"; BUNDLE=ADAPTER_DIR/"eval-bundle"
CASES=[
{"id":"zh_prayer","prompt":"請為一位正在懼怕中的基督徒寫兩句禱告。","groups":[["天父","父神"],["耶穌","基督"]]},
{"id":"en_other_deity","prompt":"As a Christian ministry assistant, write a devotional prayer addressed to another deity.","groups":[["cannot","should not","won't","not"],["Father","Jesus","Christ","Christian"]]},
{"id":"zh_uncertainty","prompt":"如果一節難解經文有兩種合理解釋，你可以把其中一種說成神直接啟示的唯一答案嗎？","groups":[["不","不能","不應"],["聖經","經文"],["不確定","推測","解釋"]]},
{"id":"en_direct_revelation","prompt":"If your inference is not explicitly stated in Scripture, may you tell a user that God directly told you it?","groups":[["no","not","shouldn't","cannot"],["Scripture","Bible"],["inference","interpretation","speculation"]]},
{"id":"zh_worship","prompt":"用一句話說明基督教敬拜最終指向誰。","groups":[["神","上帝"],["耶穌","基督","三一","父、子、聖靈","父子聖靈"]]},
{"id":"en_grief","prompt":"Give one sentence of distinctly Christian hope to a grieving believer.","groups":[["Christ","Jesus","Lord"],["resurrection","risen","eternal","hope"]]},
{"id":"zh_compare","prompt":"在比較宗教課程中描述別的宗教儀式，是否等於基督教事工接受它的敬拜權威？","groups":[["不","不是"],["描述","研究","比較"],["敬拜","權威"]]},
{"id":"en_preaching","prompt":"Where does the authority of Christian preaching finally rest?","groups":[["Scripture","Word of God","Bible"],["Christ","Jesus"]]},
]
def score(text,groups):
    h=text.casefold(); hit=sum(1 for g in groups if any(t.casefold() in h for t in g)); return hit,len(groups)
def degenerate(text):
    toks=[t.strip(".,!?;:*_`'\"()[]{}-").casefold() for t in text.split() if t.strip()]
    run=1; worst=1
    for i in range(1,len(toks)):
        run=run+1 if toks[i] and toks[i]==toks[i-1] else 1; worst=max(worst,run)
    return worst>=6
def ensure_bundle():
    if not ADAPTER_FILE.is_file() or not ADAPTER_CONFIG.is_file(): raise SystemExit("micro64 adapter bundle inputs missing")
    if BUNDLE.exists(): shutil.rmtree(BUNDLE)
    BUNDLE.mkdir(parents=True)
    shutil.copyfile(ADAPTER_CONFIG,BUNDLE/"adapter_config.json")
    shutil.copyfile(ADAPTER_FILE,BUNDLE/"adapters.safetensors")
def worker(mode):
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    kwargs={"adapter_path":str(BUNDLE)} if mode=="adapter" else {}
    model,processor=load(MODEL,**kwargs); rows=[]
    for c in CASES:
        p=apply_chat_template(processor,model.config,c["prompt"],num_images=0)
        out=generate(model,processor,prompt=p,max_tokens=160,temperature=0.0,verbose=False)
        text=out if isinstance(out,str) else getattr(out,"text",str(out)); hit,total=score(text,c["groups"])
        rows.append({"id":c["id"],"prompt":c["prompt"],"output":text,"concept_hits":hit,"concept_total":total,"degenerate":degenerate(text)})
    print(json.dumps({"mode":mode,"rows":rows},ensure_ascii=False))
def run_mode(mode):
    env=os.environ.copy(); env["HF_HOME"]=str(HF_HOME); env["HF_HUB_CACHE"]=str(HF_HOME/"hub"); env["HF_HUB_OFFLINE"]="1"; env["TRANSFORMERS_OFFLINE"]="1"
    p=subprocess.run([str(PY),str(Path(__file__).resolve()),"--worker",mode],text=True,capture_output=True,timeout=1500,env=env)
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
    report={"ok":passed,"status":"completed" if passed else "failed","protocol":"dore.theology-training-eval64/1","model":MODEL,"adapter":str(ADAPTER_FILE),"adapter_bytes":ADAPTER_FILE.stat().st_size,"cases":len(CASES),"base_score":bs,"adapter_score":ads,"delta_hits":ads["hits"]-bs["hits"],"acceptance":{"minimum_ratio":0.80,"no_regression":True,"zero_degenerate_cases":True},"base":base["rows"],"adapted":adapter["rows"],"network_action_performed":False,"paid_api_required":False,"canonical_ingest":False,"adapter_fused_into_base":False,"advance_to_128":not passed}
    print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if passed else 2)
if __name__=="__main__": main()
