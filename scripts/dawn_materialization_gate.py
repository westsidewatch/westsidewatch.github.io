#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IDENTITY=ROOT/'.dore-build/dawn-source-identity-map.json'
CAPS=ROOT/'.dore-build/dawn-source-capability-map.json'
OUT=ROOT/'.dore-build/dawn-materialization-identity-map.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def build(identity,caps):
    if identity.get('schema')!='dore.source-identity-admission.v1': raise ValueError('invalid identity map')
    if caps.get('schema')!='dore.dawn-source-capability-map.v1': raise ValueError('invalid capability map')
    cclaims=caps.get('claims') or {}; admitted={}; rejected=[]
    for ref,row in (identity.get('claims') or {}).items():
        cap=cclaims.get(ref) or {}; env=cap.get('capabilityEnvelope') or {}; dispatch=cap.get('dispatch') or env.get('dispatch') or {}
        ok=(cap.get('canonicalWorkId')==row.get('canonicalWorkId') and cap.get('status')=='static-ready' and env.get('ok') is True and env.get('schema')=='dore.source-capability-envelope.v1' and dispatch.get('schema')=='dore.source-dispatch.v1' and dispatch.get('ok') is True and dispatch.get('materializationReady') is True and dispatch.get('requiresRuntime') is False)
        if ok:
            item=dict(row); item['capabilityAdmissionStatus']='admitted-for-materialization'; item['sourceDispatchMode']=dispatch.get('mode'); admitted[ref]=item
        else:
            rejected.append({'sourceRef':ref,'canonicalWorkId':row.get('canonicalWorkId'),'capabilityStatus':cap.get('status') or 'missing','dispatchStatus':dispatch.get('status') or 'missing'})
    out=dict(identity); out['claims']=dict(sorted(admitted.items())); out['claimCount']=len(admitted)
    out['materializationAdmission']={'schema':'dore.dawn-materialization-admission.v1','sourceCapabilityEnvelopeRequired':True,'sourceDispatcherRequired':True,'acceptedStatus':'static-ready','browserRuntimeMaterialization':False,'admittedCount':len(admitted),'rejectedCount':len(rejected),'rejected':rejected}
    return out
def main():
    p=argparse.ArgumentParser(); p.add_argument('--identity-map',type=Path,default=IDENTITY); p.add_argument('--capability-map',type=Path,default=CAPS); p.add_argument('--out',type=Path,default=OUT); p.add_argument('--minimum-admitted',type=int,default=1); a=p.parse_args()
    payload=build(load(a.identity_map),load(a.capability_map)); a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    s=payload['materializationAdmission']; print(json.dumps({'admittedCount':s['admittedCount'],'rejectedCount':s['rejectedCount']},ensure_ascii=False))
    if s['admittedCount']<a.minimum_admitted: raise SystemExit('materialization admission below minimum')
    return 0
if __name__=='__main__': raise SystemExit(main())
