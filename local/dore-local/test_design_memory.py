#!/usr/bin/env python3
from design_memory import DesignEvidence, classify_scope, consolidate


def run():
    assert classify_scope('為西望設計新的網站模板') == 'westside_brand'
    assert classify_scope('CSS spacing fix', inherited_scope='westside_brand') == 'westside_brand'
    assert classify_scope('馬太福音視覺時間軸') == 'scripture_church_theology'
    assert classify_scope('unrelated private note') == 'candidate'

    old = DesignEvidence('figma-old', 'Existing Figma draft', 'reference', scope='westside_brand')
    attempt = DesignEvidence('penpot-attempt', 'Layers created in Penpot', 'attempt', scope='westside_brand')
    failure = DesignEvidence('penpot-fail', 'Rendered composition unusable', 'corrected', scope='westside_brand', supersedes='penpot-attempt')
    rule = DesignEvidence('rule-1', '5:8 is the mother proportion', 'final', scope='westside_brand')
    verified = DesignEvidence('rule-2', '5:8 verified in production composition', 'verified', scope='westside_brand', supersedes='rule-1')
    view = consolidate([old, attempt, failure, rule, verified])

    current_ids = {x['evidence_id'] for x in view['current']}
    historical_ids = {x['evidence_id'] for x in view['historical']}
    assert 'rule-2' in current_ids
    assert 'rule-1' not in current_ids
    assert 'penpot-attempt' in historical_ids
    assert 'penpot-fail' in historical_ids
    assert 'figma-old' in {x['evidence_id'] for x in view['references']}
    print('DORE_DESIGN_MEMORY_D1_D2_D3_CORE_PASS')


if __name__ == '__main__':
    run()
