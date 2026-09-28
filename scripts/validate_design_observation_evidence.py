#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'static' / 'dore-design'
SCHEMA = D / 'design-observation-evidence.schema.v1.json'

REQUIRED_OBSERVATION_LAYERS = (
    'visualFacts', 'componentGrammar', 'compositionGrammar',
    'editorialGrammar', 'motionGrammar', 'responsiveBehavior'
)
ALLOWED_METHODS = {
    'dom', 'css', 'computed-style', 'render', 'vision', 'human',
    'motion-capture', 'document-analysis'
}

def validate(item):
    errors = []
    if item.get('schema') != 'dore.design-observation-evidence.v1':
        errors.append('wrong schema identity')
    source = item.get('source') or {}
    if source.get('kind') not in {'url','render','screenshot','scan','candidate','artifact'}:
        errors.append('invalid source kind')
    if not source.get('locator'):
        errors.append('source locator required')
    obs = item.get('observations') or {}
    for layer in REQUIRED_OBSERVATION_LAYERS:
        if layer not in obs:
            errors.append(f'missing observation layer: {layer}')
    provenance = item.get('provenance') or {}
    if not provenance.get('evidenceRefs'):
        errors.append('evidence provenance required')
    methods = set(provenance.get('method') or [])
    if not methods or not methods.issubset(ALLOWED_METHODS):
        errors.append('invalid provenance method')
    authority = item.get('authority') or {}
    if authority.get('class') != 'observational-evidence':
        errors.append('observation cannot claim design authority')
    if authority.get('mayPromoteCanonical') is not False:
        errors.append('observation cannot auto-promote canonical design')
    if authority.get('requiresBeautifulGate') is not True:
        errors.append('Beautiful Gate is mandatory before learning/promotion')
    for layer in REQUIRED_OBSERVATION_LAYERS[1:]:
        for i, claim in enumerate(obs.get(layer) or []):
            if not claim.get('statement') or not claim.get('evidenceRefs'):
                errors.append(f'{layer}[{i}] lacks statement/evidence')
            confidence = claim.get('confidence')
            if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                errors.append(f'{layer}[{i}] invalid confidence')
    for i, inference in enumerate(obs.get('inferredRationale') or []):
        if inference.get('status') != 'inference-not-fact':
            errors.append(f'inferredRationale[{i}] must remain inference-not-fact')
    return errors

def main(paths):
    if not SCHEMA.exists():
        print('FAIL: canonical observation schema missing')
        return 1
    if not paths:
        print('PASS: schema present; no evidence envelopes supplied.')
        return 0
    failures = 0
    for raw in paths:
        path = Path(raw)
        data = json.loads(path.read_text())
        items = data.get('items', []) if isinstance(data, dict) and 'items' in data else [data]
        for item in items:
            errors = validate(item)
            if errors:
                failures += 1
                for error in errors: print(f'FAIL {item.get("id","<unknown>")}: {error}')
            else:
                print(f'PASS {item["id"]}: observational evidence boundary intact')
    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
