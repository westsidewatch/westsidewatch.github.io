#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, time
from pathlib import Path
C=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
PY=C/"venv"/"bin"/"python"
MODEL="mlx-community/gemma-4-e4b-it-4bit"
BASE_DIR=C/"runs"/"n64"/"adapter"
BASE_FILE=BASE_DIR/"adapter.safetensors"
BASE_CONFIG=BASE_DIR/"adapter_config.json"
WORK=C/"runs"/"n64-recovery"
DATA=WORK/"dataset"
RESUME=WORK/"resume-bundle"
OUT_DIR=WORK/"adapter"
OUT=OUT_DIR/"adapter.safetensors"
TRAIN=[
("When explaining another religion in a Christian study class, what boundary should be kept?","Describe it accurately, but distinguish its worship claims from Christian authority; Christian faith remains governed by Scripture and centered on Jesus Christ."),
("How can a Christian ministry assistant compare religions without endorsing another religion's devotional claims?","Explain fairly while distinguishing description from Christian worship and authority under Scripture and Christ."),
("A class asks for a description of Buddhist worship. What boundary should a Christian assistant keep?","Give an accurate academic description, but do not present Buddhist worship as Christian authority; distinguish study from Christian worship governed by Scripture and Christ."),
("Does respectful interfaith explanation require treating every religion's worship claims as Christian authority?","No. Respectful explanation can be accurate while distinguishing other claims from Christian worship and Scripture's authority."),
("請為一位失業焦慮的基督徒寫一句很短的禱告。","主耶穌，求你在焦慮中賜下平安與今日所需的恩典；我們把未知的結果交在你手中。"),
("請為一位不知道工作結果的基督徒作一句不預知結果的禱告。","主耶穌，求你賜智慧、供應與平安；我們不宣稱未知結果，只在基督裡信靠你的帶領。"),
("Give one short Christian prayer for unemployment anxiety without claiming to know the outcome.","Lord Jesus, give peace, wisdom, and daily provision; we entrust the unknown outcome to you."),
("Write a brief Christ-centered prayer for uncertainty about work.","Jesus Christ, grant peace and faithful wisdom today, and help us trust you without claiming certainty about tomorrow."),
]
def row(p):
 u,a=p; return {"messages":[{"role":"user","content":u},{"role":"assistant","content":a}]}
def write(path,items):
 with path.open("w",encoding="utf-8") as f:
  for p in items: f.write(json.dumps(row(p),ensure_ascii=False,separators=(",",":"))+"\n")
def main():
 if len(sys.argv)!=1: raise SystemExit("no caller arguments accepted")
 if not PY.is_file() or not BASE_FILE.is_file() or not BASE_CONFIG.is_file(): raise SystemExit("recovery inputs missing")
 shutil.rmtree(WORK,ignore_errors=True); DATA.mkdir(parents=True); RESUME.mkdir(parents=True); OUT_DIR.mkdir(parents=True)
 shutil.copyfile(BASE_CONFIG,RESUME/"adapter_config.json"); shutil.copyfile(BASE_FILE,RESUME/"adapters.safetensors")
 write(DATA/"train.jsonl",TRAIN); write(DATA/"valid.jsonl",TRAIN[:4]); write(DATA/"test.jsonl",TRAIN[4:])
 cmd=[str(PY),"-m","mlx_vlm.lora","--model-path",MODEL,"--dataset",str(DATA),"--split","train","--iters","12","--batch-size","1","--learning-rate","1e-6","--lora-rank","8","--lora-alpha","16","--max-seq-length","2048","--train-on-completions","--steps-per-report","4","--steps-per-eval","6","--val-batches","4","--adapter-path",str(RESUME),"--output-path",str(OUT)]
 env=os.environ.copy(); hf=C/"hf"; env["HF_HOME"]=str(hf); env["HF_HUB_CACHE"]=str(hf/"hub"); env["HF_HUB_OFFLINE"]="1"; env["TRANSFORMERS_OFFLINE"]="1"
 t=time.monotonic(); p=subprocess.run(cmd,text=True,capture_output=True,timeout=3600,env=env)
 ok=p.returncode==0 and OUT.is_file() and OUT.stat().st_size>0
 print(json.dumps({"ok":ok,"status":"completed" if ok else "failed","protocol":"dore.theology-training-recovery64/3","model":MODEL,"training_rows":8,"learning_rate":"1e-6","iterations":12,"seconds":round(time.monotonic()-t,3),"returncode":p.returncode,"resume_bundle":str(RESUME),"adapter":str(OUT),"adapter_bytes":OUT.stat().st_size if OUT.is_file() else 0,"stdout_tail":p.stdout[-3000:],"stderr_tail":p.stderr[-3000:],"offline_only":True,"canonical_ingest":False,"adapter_fused_into_base":False,"production_default_changed":False,"paid_api_required":False},ensure_ascii=False,indent=2)); raise SystemExit(0 if ok else 2)
if __name__=="__main__": main()
