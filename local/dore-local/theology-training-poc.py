#!/usr/bin/env python3
"""Doré Theology Alignment micro-POC through the isolated MLX-VLM toolchain."""
from __future__ import annotations
import argparse,json,os,shutil,subprocess,time
from pathlib import Path
CACHE_ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"; VENV=CACHE_ROOT/"venv"; PY=VENV/"bin"/"python"
DEFAULT_TRAINING_MODEL=os.environ.get("DORE_THEOLOGY_MLX_MODEL","mlx-community/gemma-4-e4b-it-4bit"); SIZES=(32,64,128,256)
def die(message): print(json.dumps({"ok":False,"error":message},ensure_ascii=False)); raise SystemExit(2)
def require_quarantine(path):
    resolved=path.expanduser().resolve(); home=Path.home().resolve(); forbidden=[(home/".dore").resolve(),(home/"Library/Application Support/Dore").resolve()]
    for root in forbidden:
        try: resolved.relative_to(root); die("quarantine path must not be inside Doré runtime/core data")
        except ValueError: pass
def count_jsonl(path):
    with path.open("r",encoding="utf-8") as fh: return sum(1 for line in fh if line.strip())
def verify_dataset(root,size):
    train=root/f"train-{size}.jsonl"; valid=root/"valid.jsonl"; test=root/"test.jsonl"
    for p in (train,valid,test):
        if not p.is_file(): die(f"missing quarantined split: {p}")
    tn=count_jsonl(train); vn=count_jsonl(valid); sn=count_jsonl(test)
    if tn!=size: die(f"expected {size} training rows, found {tn}")
    if vn<1 or sn<1: die("valid/test quarantine splits must be non-empty")
    return {"train":str(train),"valid":str(valid),"test":str(test),"train_rows":tn,"valid_rows":vn,"test_rows":sn}
def mlx_vlm_available():
    if not PY.is_file(): return False
    p=subprocess.run([str(PY),"-c","import mlx_vlm, datasets"],text=True,capture_output=True,timeout=30); return p.returncode==0
def build_command(model,dataset_dir,adapter_file,iters,learning_rate="2e-5"):
    return [str(PY),"-m","mlx_vlm.lora","--model-path",model,"--dataset",str(dataset_dir),"--split","train","--iters",str(iters),"--batch-size","1","--learning-rate",str(learning_rate),"--lora-rank","8","--lora-alpha","16","--max-seq-length","2048","--train-on-completions","--steps-per-report","10","--steps-per-eval","20","--val-batches","4","--output-path",str(adapter_file)]
def stage_split(dataset,work):
    stage=work/"dataset"; stage.mkdir(parents=True,exist_ok=True)
    for src,dst in {dataset["train"]:stage/"train.jsonl",dataset["valid"]:stage/"valid.jsonl",dataset["test"]:stage/"test.jsonl"}.items(): shutil.copyfile(src,dst)
    return stage
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--quarantine",required=True); ap.add_argument("--size",type=int,choices=SIZES,default=32); ap.add_argument("--model",default=DEFAULT_TRAINING_MODEL); ap.add_argument("--work",default=str(CACHE_ROOT/"runs")); ap.add_argument("--iters",type=int,default=80); ap.add_argument("--execute",action="store_true"); args=ap.parse_args()
    quarantine=Path(args.quarantine); require_quarantine(quarantine); dataset=verify_dataset(quarantine,args.size)
    work=Path(args.work).expanduser().resolve()/f"n{args.size}"; shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True); stage=stage_split(dataset,work); adapter_dir=work/"adapter"; adapter_dir.mkdir(parents=True,exist_ok=True); adapter_file=adapter_dir/"adapter.safetensors"
    learning_rate=os.environ.get("DORE_THEOLOGY_MLX_LR","2e-5")
    command=build_command(args.model,stage,adapter_file,args.iters,learning_rate)
    report={"ok":True,"protocol":"dore.theology-training-poc/4","training_backend":"mlx-vlm","training_model":args.model,"runtime_model":os.environ.get("DORE_LOCAL_MODEL","gemma4:e4b"),"training_size":args.size,"dataset_rows":{"train":dataset["train_rows"],"valid":dataset["valid_rows"],"test":dataset["test_rows"]},"quarantine":str(quarantine.resolve()),"canonical_ingest":False,"paid_api_required":False,"network_action_performed":False,"adapter_fused_into_base":False,"adapter_path":str(adapter_file),"learning_rate":learning_rate,"command":command,"executed":False}
    if args.execute:
        if not mlx_vlm_available(): die("isolated MLX-VLM training environment is not prepared")
        env=os.environ.copy(); hf_home=CACHE_ROOT/"hf"; env["HF_HOME"]=str(hf_home); env["HF_HUB_CACHE"]=str(hf_home/"hub"); env["HF_HUB_OFFLINE"]="1"; env["TRANSFORMERS_OFFLINE"]="1"; started=time.monotonic()
        proc=subprocess.run(command,cwd=str(work),text=True,capture_output=True,timeout=6900,env=env); report["executed"]=True; report["returncode"]=proc.returncode; report["seconds"]=round(time.monotonic()-started,3); report["stdout_tail"]=proc.stdout[-5000:]; report["stderr_tail"]=proc.stderr[-5000:]; report["ok"]=proc.returncode==0 and adapter_file.is_file(); report["adapter_present"]=adapter_file.is_file(); report["adapter_bytes"]=adapter_file.stat().st_size if adapter_file.is_file() else 0
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
