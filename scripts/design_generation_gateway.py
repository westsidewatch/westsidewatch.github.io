#!/usr/bin/env python3
import argparse, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'static'/'dore-design'/'design-generation-consumers.v1.json'
RESOLVER=ROOT/'scripts'/'resolve_design_generation_prompt.py'

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def resolver():
    spec=importlib.util.spec_from_file_location('dore_generation_resolver',RESOLVER)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def consumers(): return {x['id']:x for x in load(REGISTRY).get('consumers',[]) if x.get('enabled')}

def prepare(consumer,era,subject=None,artifact_type='image',modules=None,exploration=False,constraints=None):
    known=consumers()
    if consumer not in known: raise ValueError('unregistered generation consumer: '+consumer)
    resolved=resolver().resolve(era,modules,subject,artifact_type,consumer,exploration)
    prompt=resolved['canonical_prompt']
    extra=[str(x).strip() for x in (constraints or []) if str(x).strip()]
    if extra: prompt+='\n\nConsumer constraints:\n- '+'\n- '.join(extra)
    return {'schema':'dore.design-generation-gateway.v1','status':'READY_FOR_GENERATOR','consumer':consumer,'formal':not exploration,'generator_prompt':prompt,'resolution':resolved,'must_visual_verify':True,'may_be_historical_authority':False}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--consumer',required=True); p.add_argument('--era',required=True); p.add_argument('--subject'); p.add_argument('--artifact-type',default='image'); p.add_argument('--module',action='append',dest='modules'); p.add_argument('--constraint',action='append',dest='constraints'); p.add_argument('--exploration',action='store_true'); p.add_argument('--prompt-only',action='store_true'); a=p.parse_args()
    try: out=prepare(a.consumer,a.era,a.subject,a.artifact_type,a.modules,a.exploration,a.constraints)
    except (ValueError,FileNotFoundError,json.JSONDecodeError) as e: print('BLOCKED:',e,file=sys.stderr); return 2
    print(out['generator_prompt'] if a.prompt_only else json.dumps(out,ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
