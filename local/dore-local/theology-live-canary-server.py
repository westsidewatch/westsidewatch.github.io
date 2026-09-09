#!/usr/bin/env python3
"""Opt-in localhost Doré /chat canary using the passed theology recovery adapter.

This reuses Doré's real HTTP handler and memory/context pipeline. It runs on a
separate localhost port and replaces only the inference function inside this
canary process. The production 8788 process and default Ollama engine are not
modified.
"""
from __future__ import annotations
import json, os, sys
from http.server import ThreadingHTTPServer
from pathlib import Path

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import dore_local as dl

CACHE=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
HF_HOME=CACHE/"hf"
PY=CACHE/"venv"/"bin"/"python"
MODEL="mlx-community/gemma-4-e4b-it-4bit"
ADAPTER_DIR=CACHE/"runs"/"n64-recovery"/"adapter"
ADAPTER_FILE=ADAPTER_DIR/"adapter.safetensors"
ADAPTER_CONFIG=CACHE/"runs"/"n64"/"adapter"/"adapter_config.json"
BUNDLE=CACHE/"runs"/"n64-recovery"/"live-canary-bundle"
PORT=int(os.environ.get("DORE_THEOLOGY_CANARY_PORT","8791"))

_model=None
_processor=None

def ensure_bundle():
    import shutil
    if not PY.is_file() or not ADAPTER_FILE.is_file() or not ADAPTER_CONFIG.is_file():
        raise RuntimeError("theology_canary_inputs_missing")
    BUNDLE.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ADAPTER_CONFIG,BUNDLE/"adapter_config.json")
    shutil.copyfile(ADAPTER_FILE,BUNDLE/"adapters.safetensors")

def mlx_inference(messages):
    global _model,_processor
    os.environ["HF_HOME"]=str(HF_HOME)
    os.environ["HF_HUB_CACHE"]=str(HF_HOME/"hub")
    os.environ["HF_HUB_OFFLINE"]="1"
    os.environ["TRANSFORMERS_OFFLINE"]="1"
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    if _model is None:
        ensure_bundle()
        _model,_processor=load(MODEL,adapter_path=str(BUNDLE))
    # Doré's real /chat handler already constructs the system+memory prompt.
    user='\n\n'.join(str(x.get('content') or '') for x in messages if x.get('role')!='system')
    system='\n\n'.join(str(x.get('content') or '') for x in messages if x.get('role')=='system')
    combined=(system+'\n\n'+user).strip()
    prompt=apply_chat_template(_processor,_model.config,combined,num_images=0)
    out=generate(_model,_processor,prompt=prompt,max_tokens=256,temperature=0.0,verbose=False)
    text=out if isinstance(out,str) else getattr(out,"text",str(out))
    if not text.strip(): raise RuntimeError("theology_canary_empty_content")
    return text.strip()

def main():
    ensure_bundle()
    dl.ollama=mlx_inference
    dl.MODEL="dore-theology-recovery64-canary"
    dl.ROOT.joinpath('data').mkdir(parents=True,exist_ok=True)
    dl.ROOT.joinpath('archive','conversations').mkdir(parents=True,exist_ok=True)
    dl.ensure_design_schema(); dl.bootstrap_legacy_memory(); dl.bootstrap_self_memory()
    print(json.dumps({"ok":True,"mode":"theology_canary","host":"127.0.0.1","port":PORT,"model":MODEL,"adapter":str(ADAPTER_FILE),"production_default_changed":False,"offline_only":True},ensure_ascii=False),flush=True)
    ThreadingHTTPServer(("127.0.0.1",PORT),dl.H).serve_forever()

if __name__=="__main__": main()
