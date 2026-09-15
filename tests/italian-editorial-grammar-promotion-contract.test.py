import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_promotion_contract_gate():
    p=subprocess.run([sys.executable,str(ROOT/'scripts'/'validate_italian_editorial_grammar_promotion.py')],cwd=ROOT,text=True,capture_output=True)
    assert p.returncode==0, p.stdout+p.stderr

def test_no_admission_without_contract():
    data=json.loads((ROOT/'static'/'dore-design'/'italian-editorial-grammar-candidates.v1.json').read_text())
    for item in data['items']:
        if item['state']=='admitted':
            checks=item.get('promotionContract',{}).get('checks',{})
            assert all(checks.get(k) is True for k in ('evidenceProvenance','generationComparison','noCanonicalRegression'))
