#!/usr/bin/env python3
import json, sqlite3, tempfile
from pathlib import Path
from self_memory import ensure_schema, upsert_self, add_learning
from bridge_reminder import bridge_packet

with tempfile.TemporaryDirectory() as td:
    db = Path(td)/'dore.sqlite3'
    c=sqlite3.connect(db); c.row_factory=sqlite3.Row; ensure_schema(c)
    upsert_self(c,'coordination.bridge_protocol','ChatGPT bridges consequential Doré information.','system_policy','dore-bridge-protocol-v1','verified')
    upsert_self(c,'coordination.bridge_trigger',"去读多雷备忘 restores Bridge Protocol.",'system_policy','dore-bridge-protocol-v1','verified')
    add_learning(c,'Coordination','OPEN GOAL: shared User + ChatGPT + Doré conversation.','Shared Conversation',status='open',evidence_ref='dore-bridge-protocol-v1',source_type='user_goal',epistemic_state='observed')
    p1=bridge_packet(c); c.close()
    c=sqlite3.connect(db); c.row_factory=sqlite3.Row
    p2=bridge_packet(c); c.close()
    assert p1['bridge_required'] is True
    assert p1['packet_sha256']==p2['packet_sha256']
    assert '去读多雷备忘' in p2['trigger_phrases']
    assert any(x['key']=='coordination.bridge_protocol' for x in p2['policies'])
    assert any(x['status']=='open' for x in p2['open_items'])
    assert 'ChatGPT' in p2['instruction']
    print(json.dumps({'ok':True,'marker':'DORE_BRIDGE_REMINDER_CONTRACT_PASS','packet_sha256':p2['packet_sha256']},ensure_ascii=False))
