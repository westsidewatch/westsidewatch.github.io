#!/usr/bin/env python3
import argparse, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'static'/'dore-design'/'design-generation-consumers.v1.json'
MAGAZINE_PROFILE=ROOT/'static'/'dore-design'/'magazine-profile.olive-speaker.v1.json'
RESOLVER=ROOT/'scripts'/'resolve_design_generation_prompt.py'
MAGAZINE_CANDIDATES=ROOT/'scripts'/'generate_magazine_candidates.py'
MAGAZINE_SCORER=ROOT/'scripts'/'score_magazine_candidates.py'
MAGAZINE_COMPOSER=ROOT/'scripts'/'compose_magazine_production.py'

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def resolver():
    spec=importlib.util.spec_from_file_location('dore_generation_resolver',RESOLVER)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def consumers(): return {x['id']:x for x in load(REGISTRY).get('consumers',[]) if x.get('enabled')}

def magazine_profile(consumer,artifact_type):
    if consumer!='westside-watch' or artifact_type!='speaker-cover': return None
    profile=load(MAGAZINE_PROFILE)
    if profile.get('consumer')!=consumer or profile.get('artifactType')!=artifact_type: raise ValueError('magazine profile authority mismatch')
    return profile

def compose_magazine(consumer,artifact_type,speaker,portrait_state='missing'):
    if not magazine_profile(consumer,artifact_type): return None
    if not speaker: raise ValueError('speaker-cover composition requires speaker slug')
    candidates=module(MAGAZINE_CANDIDATES,'dore_magazine_candidates').generate(speaker,portrait_state)
    scored=module(MAGAZINE_SCORER,'dore_magazine_scorer').rank(candidates)
    production=module(MAGAZINE_COMPOSER,'dore_magazine_composer').produce(scored,magazine_profile(consumer,artifact_type))
    return {**scored,'production':production}

def prepare(consumer,era,subject=None,artifact_type='image',modules=None,exploration=False,constraints=None,speaker=None,portrait_state='missing'):
    known=consumers()
    if consumer not in known: raise ValueError('unregistered generation consumer: '+consumer)
    resolved=resolver().resolve(era,modules,subject,artifact_type,consumer,exploration)
    profile=magazine_profile(consumer,artifact_type)
    composition=compose_magazine(consumer,artifact_type,speaker,portrait_state) if profile else None
    prompt=resolved['canonical_prompt']
    extra=[str(x).strip() for x in (constraints or []) if str(x).strip()]
    if extra: prompt+='\n\nConsumer constraints:\n- '+'\n- '.join(extra)
    return {'schema':'dore.design-generation-gateway.v1','status':'READY_FOR_GENERATOR','composition_profile':profile,'composition':composition,'consumer':consumer,'formal':not exploration,'generator_prompt':prompt,'resolution':resolved,'must_visual_verify':True,'may_be_historical_authority':False}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--consumer',required=True); p.add_argument('--era',required=True); p.add_argument('--subject'); p.add_argument('--artifact-type',default='image'); p.add_argument('--module',action='append',dest='modules'); p.add_argument('--constraint',action='append',dest='constraints'); p.add_argument('--speaker'); p.add_argument('--portrait-state',choices=['verified','missing'],default='missing'); p.add_argument('--exploration',action='store_true'); p.add_argument('--prompt-only',action='store_true'); a=p.parse_args()
    try: out=prepare(a.consumer,a.era,a.subject,a.artifact_type,a.modules,a.exploration,a.constraints,a.speaker,a.portrait_state)
    except (ValueError,FileNotFoundError,json.JSONDecodeError) as e: print('BLOCKED:',e,file=sys.stderr); return 2
    print(out['generator_prompt'] if a.prompt_only else json.dumps(out,ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
