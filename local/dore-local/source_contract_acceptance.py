#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
CONTRACT=ROOT/'dore-core/runtime/source-capability-contract.v1.json'
REGISTRY=ROOT/'dore-core/runtime/capability-registry.v1.json'
CINEMA=ROOT/'local/dore-companion-extension/runtime_probe_background.js'
DAWN=ROOT/'scripts/build_dawn_source_capability_map.py'
MULTIWRITE=ROOT/'static/multiwrite/source-capability-admission.mjs'


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec)
    assert spec and spec.loader; spec.loader.exec_module(mod); return mod


def envelope_fixture(runtime=False):
    modes=['browser-runtime'] if runtime else ['static-http']
    return {
        'ok':True,'schema':'dore.source-capability-envelope.v1','sourcePointer':'https://example.org/a',
        'access':{'modes':modes,'preferred':modes[0]},
        'runtimeBoundary':{'required':runtime,'mode':modes[0]},
        'authority':{'canonicalIdentityAuthority':False,'envelopeAuthority':False},
        'rights':{'rehost':False},'editorialBoundary':{'sourceContentMayBeRewrittenSilently':False},
        'operations':['read','cite','extract'],'persistence':'request-scoped-none'
    }


def main():
    contract=json.loads(CONTRACT.read_text())
    assert contract['schema']=='dore.source-capability-contract.v1'
    assert contract['status']=='frozen-v1'
    assert contract['pipeline']==['source.probe','source.capability-envelope','source.dispatch','consumer-admission']
    assert contract['boundaries']['productsMayReinterpretAccess'] is False
    assert contract['boundaries']['canonicalIdentityAuthority'] is False
    assert contract['boundaries']['rightsAuthority'] is False
    assert contract['boundaries']['persistence']=='request-scoped-none'

    dispatcher=load_module('source_dispatcher',HERE/'source_dispatcher.py')
    bad=dispatcher.dispatch({})
    assert bad=={'ok':False,'status':'blocked','schema':'dore.source-dispatch.v1','reason':'invalid-capability-envelope'}
    static=dispatcher.dispatch(envelope_fixture(False)); runtime=dispatcher.dispatch(envelope_fixture(True))
    assert static['status']=='ready' and static['mode']=='static-http' and static['materializationReady'] is True
    assert runtime['status']=='runtime-required' and runtime['mode']=='browser-runtime' and runtime['requiresRuntime'] is True
    for row in (static,runtime):
        assert row['providerSpecificRouting'] is False and row['authority'] is False and row['persistence']=='request-scoped-none'

    registry=json.loads(REGISTRY.read_text())
    caps={x['id']:x for x in registry.get('capabilities',[])}
    assert 'source.probe' in caps and 'source.capability-envelope' in caps and 'source.dispatch' in caps
    d=caps['source.dispatch']
    assert d.get('execution')=='in-process' and d.get('authority') is False and d.get('provider_neutral') is True
    assert d.get('requires')==['source.capability-envelope']

    cinema=CINEMA.read_text(); dawn=DAWN.read_text(); multi=MULTIWRITE.read_text()
    assert 'dispatch.requiresRuntime' in cinema
    assert 'initialEnvelope.runtimeBoundary' not in cinema
    assert "needs.includes('runtime-browser-probe')" not in cinema
    assert "decision.get('materializationReady')" in dawn
    assert "projected.get('access')" not in dawn and "runtime.get('required')" not in dawn
    assert 'dispatch.requiresRuntime' in multi and 'envelope.runtimeBoundary' not in multi
    assert 'RIGHTS_GATED' in multi and 'EDITORIAL_GATED' in multi

    print('DORE_SOURCE_CONTRACT_SCHEMA_FROZEN=PASS')
    print('DORE_SOURCE_CONTRACT_STABLE_ERRORS=PASS')
    print('DORE_SOURCE_CONTRACT_DISPATCH_BOUNDARY=PASS')
    print('DORE_SOURCE_CONTRACT_CINEMA_CONFORMANCE=PASS')
    print('DORE_SOURCE_CONTRACT_DAWN_CONFORMANCE=PASS')
    print('DORE_SOURCE_CONTRACT_MULTIWRITE_CONFORMANCE=PASS')
    print('DORE_SOURCE_CONTRACT_AUTHORITY_RIGHTS_PERSISTENCE=PASS')

if __name__=='__main__': main()
