#!/usr/bin/env python3
"""Live acceptance for Doré Coordination Hardening 1.0."""
import json,sys,urllib.request
BASE='http://127.0.0.1:4310';expected=sys.argv[1] if len(sys.argv)>1 else None
def get(path):return json.loads(urllib.request.urlopen(BASE+path,timeout=12).read().decode())
health=get('/api/health');coord=get('/api/coordination/status')
checks={
 'design_version':health.get('version')=='1.7.2',
 'hardening_declared':health.get('coordination_hardening')=='1.0' and coord.get('hardening')=='1.0',
 'status_endpoint_live':coord.get('ok') is True,
 'daemon_observable':coord.get('daemon_health') not in (None,'unknown'),
 'queue_observable':isinstance(coord.get('queue_depth'),int),
 'current_task_visible':(not expected) or coord.get('last_received')==expected,
 'current_task_running':(not expected) or coord.get('last_status') in ('RECEIVED','RUNNING'),
}
ok=all(checks.values());print(json.dumps({'ok':ok,'code':'DORE_COORDINATION_HARDENING_1_PASS' if ok else 'DORE_COORDINATION_HARDENING_1_FAIL','expected_task':expected,'coordination':coord,'checks':checks},ensure_ascii=False));raise SystemExit(0 if ok else 1)
