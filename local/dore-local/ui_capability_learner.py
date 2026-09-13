#!/usr/bin/env python3
from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from autonomous_learner import discover_evidence, evidence_pack, iterate_research, blind_assessment
from learning_planner import plan, validate_gate
from self_memory import add_learning, status as learning_status, transition_learning

UI_GATE_FILES = ('ui-v1.json', 'ui-v2.json', 'ui-v3.json', 'ui-v4.json')
UI_POLICY = 'dore-ui-capability-learning-v4'


def now():
    return datetime.now(timezone.utc).isoformat()


def _validate_ui_dependency_graph(gates):
    by_id = {g['id']: g for g in gates}
    if len(by_id) != len(gates):
        seen = set()
        duplicates = []
        for gate in gates:
            gate_id = gate['id']
            if gate_id in seen and gate_id not in duplicates:
                duplicates.append(gate_id)
            seen.add(gate_id)
        raise ValueError('duplicate UI learning gate id: ' + ','.join(duplicates))

    missing = []
    for gate in gates:
        for dep in gate.get('requires') or []:
            if dep not in by_id:
                missing.append(f"{gate['id']}->{dep}")
    if missing:
        raise ValueError('missing UI learning gate dependency: ' + ','.join(missing))

    state = {}
    stack = []

    def visit(gate_id):
        marker = state.get(gate_id, 0)
        if marker == 2:
            return
        if marker == 1:
            try:
                start = stack.index(gate_id)
                cycle = stack[start:] + [gate_id]
            except ValueError:
                cycle = stack + [gate_id]
            raise ValueError('cyclic UI learning gate dependency: ' + '->'.join(cycle))
        state[gate_id] = 1
        stack.append(gate_id)
        for dep in by_id[gate_id].get('requires') or []:
            visit(dep)
        stack.pop()
        state[gate_id] = 2

    for gate_id in by_id:
        visit(gate_id)
    return gates


def load_ui_gates(base: Path | None = None):
    base = base or Path(__file__).resolve().parent
    gate_dir = base / 'learning-gates'
    gates = []
    for filename in UI_GATE_FILES:
        path = gate_dir / filename
        if not path.is_file():
            raise FileNotFoundError('required UI learning gate file missing: ' + filename)
        payload = json.loads(path.read_text(encoding='utf-8'))
        if payload.get('schema') != 'dore.learning-gates.v1':
            raise ValueError('unsupported UI learning gate schema in ' + filename)
        file_gates = payload.get('gates') or []
        if not isinstance(file_gates, list) or not file_gates:
            raise ValueError('UI learning gate file has no gates: ' + filename)
        gates.extend(validate_gate(g) for g in file_gates)
    return _validate_ui_dependency_graph(gates)


def ensure_schema(conn: sqlite3.Connection):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS dore_ui_learning_runs(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      gate_id TEXT NOT NULL,
      phase TEXT NOT NULL,
      score REAL NOT NULL DEFAULT 0,
      evidence_count INTEGER NOT NULL DEFAULT 0,
      result_json TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_dore_ui_learning_gate
      ON dore_ui_learning_runs(gate_id, created_at DESC);
    ''')
    conn.commit()


def _refs(synthesis):
    refs = set()
    if isinstance(synthesis, dict):
        for claim in synthesis.get('claims') or []:
            if isinstance(claim, dict):
                refs.update(claim.get('source_refs') or [])
    return refs


def _score(blind):
    try:
        return float((blind.get('grade') or {}).get('score') or 0)
    except Exception:
        return 0.0


def execute_ui_gate(conn, repo_root: Path, dore_root: Path, gate, model_call=None):
    ensure_schema(conn)
    hits, digest = discover_evidence(repo_root, dore_root, gate, limit=40)
    pack = evidence_pack(hits, max_files=12, max_chars_each=5000)
    result = {
        'gate_id': gate['id'],
        'domain': gate['domain'],
        'stage': gate.get('stage'),
        'fresh_problem': gate.get('fresh_problem'),
        'acceptance': gate.get('acceptance') or [],
        'evidence_hash': digest,
        'evidence': hits,
    }
    phase = 'blocked'
    score = 0.0
    verified = False
    if model_call and len(pack) >= int(gate.get('min_evidence') or 1):
        synthesis, critic, iterations = iterate_research(model_call, gate, pack)
        blind = blind_assessment(model_call, gate, pack)
        score = _score(blind)
        grade = blind.get('grade') or {}
        verified = (
            len(_refs(synthesis)) >= 2
            and not (critic.get('unsupported_claims') or [])
            and not (critic.get('acceptance_missing') or [])
            and score >= 0.82
            and not (grade.get('unsupported') or [])
            and not (grade.get('provenance_failures') or [])
        )
        phase = 'completed' if verified else 'assessment_ready'
        result.update({
            'synthesis': synthesis,
            'critic': critic,
            'iterations': iterations,
            'blind_assessment': blind,
            'verified_by_executor': verified,
        })
    else:
        result['verified_by_executor'] = False
    t = now()
    conn.execute(
        'INSERT INTO dore_ui_learning_runs(gate_id,phase,score,evidence_count,result_json,created_at) VALUES(?,?,?,?,?,?)',
        (gate['id'], phase, score, len(pack), json.dumps(result, ensure_ascii=False), t),
    )
    learning_id = add_learning(
        conn,
        gate['domain'],
        f"Doré UI capability run for {gate['id']}.",
        gate.get('stage'),
        assessment=f'UI blind assessment score={score:.2f}',
        status='pass' if verified else ('researching' if phase == 'assessment_ready' else 'blocked'),
        evidence_ref=f'ui-capability:{gate["id"]}:{t}',
        source_type='ui_capability_executor',
        epistemic_state='observed',
    )
    if verified:
        transition_learning(
            conn,
            learning_id,
            'verified',
            reason='fresh UI capability assessment passed',
            evidence_ref=f'ui-capability:{gate["id"]}:{t}',
            status='pass',
        )
    conn.commit()
    return {
        'gate_id': gate['id'],
        'phase': phase,
        'score': score,
        'evidence_count': len(pack),
        'verified': verified,
    }


def run_ui_cycle(conn, repo_root: Path, dore_root: Path, max_gates=3, model_call=None):
    gates = load_ui_gates()
    planner = plan(learning_status(conn), gates)
    by_id = {g['id']: g for g in gates}
    executed = []
    productive = 0
    for item in planner.get('ready') or []:
        if productive >= max_gates:
            break
        gate = by_id[item['id']]
        result = execute_ui_gate(conn, repo_root, dore_root, gate, model_call=model_call)
        executed.append(result)
        productive += 1
    return {
        'ok': True,
        'policy': UI_POLICY,
        'gate_versions': list(UI_GATE_FILES),
        'gate_count': len(gates),
        'executed': executed,
        'planner': planner,
        'productive_runs': productive,
    }


def status(conn):
    ensure_schema(conn)
    rows = [dict(r) for r in conn.execute(
        'SELECT gate_id,phase,score,evidence_count,result_json,created_at FROM dore_ui_learning_runs ORDER BY id DESC LIMIT 50'
    )]
    for row in rows:
        try:
            row['result'] = json.loads(row.pop('result_json'))
        except Exception:
            row['result'] = None
    return {'ok': True, 'policy': UI_POLICY, 'runs': rows}
