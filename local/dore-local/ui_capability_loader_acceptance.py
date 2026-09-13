#!/usr/bin/env python3
from __future__ import annotations
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import ui_capability_learner as learner

EXPECTED_FILES = ['ui-v1.json', 'ui-v2.json', 'ui-v3.json', 'ui-v4.json']
EXPECTED_GATE_COUNT = 25
EXPECTED_FINAL_GATE = 'ui-design-intelligence-graduation-iv'


def _expect_error(fn, needle):
    try:
        fn()
    except Exception as exc:
        if needle not in str(exc):
            raise AssertionError(f'expected {needle!r}, got {type(exc).__name__}: {exc}')
        return str(exc)
    raise AssertionError(f'expected error containing {needle!r}')


def _copy_gate_dir(dst: Path):
    src = HERE / 'learning-gates'
    out = dst / 'learning-gates'
    out.mkdir(parents=True, exist_ok=True)
    for name in EXPECTED_FILES:
        shutil.copy2(src / name, out / name)
    return out


def main():
    gates = learner.load_ui_gates(HERE)
    ids = [g['id'] for g in gates]
    assert learner.UI_POLICY == 'dore-ui-capability-learning-v4'
    assert list(learner.UI_GATE_FILES) == EXPECTED_FILES
    assert len(gates) == EXPECTED_GATE_COUNT, len(gates)
    assert len(set(ids)) == EXPECTED_GATE_COUNT
    assert EXPECTED_FINAL_GATE in ids
    assert 'core-v1.json' not in learner.UI_GATE_FILES

    order = {gate_id: idx for idx, gate_id in enumerate(ids)}
    for gate in gates:
        for dep in gate.get('requires') or []:
            assert dep in order, (gate['id'], dep)
            assert order[dep] < order[gate['id']], (gate['id'], dep)

    with tempfile.TemporaryDirectory(prefix='dore-ui-loader-') as td:
        base = Path(td)
        gate_dir = _copy_gate_dir(base)

        p = gate_dir / 'ui-v4.json'
        payload = json.loads(p.read_text(encoding='utf-8'))
        payload['gates'][0]['id'] = 'ui-taste-memory-graduation-iii'
        p.write_text(json.dumps(payload), encoding='utf-8')
        duplicate_error = _expect_error(lambda: learner.load_ui_gates(base), 'duplicate UI learning gate id')

    with tempfile.TemporaryDirectory(prefix='dore-ui-loader-') as td:
        base = Path(td)
        gate_dir = _copy_gate_dir(base)
        p = gate_dir / 'ui-v4.json'
        payload = json.loads(p.read_text(encoding='utf-8'))
        payload['gates'][0]['requires'] = ['ui-does-not-exist']
        p.write_text(json.dumps(payload), encoding='utf-8')
        missing_error = _expect_error(lambda: learner.load_ui_gates(base), 'missing UI learning gate dependency')

    with tempfile.TemporaryDirectory(prefix='dore-ui-loader-') as td:
        base = Path(td)
        gate_dir = _copy_gate_dir(base)
        p = gate_dir / 'ui-v1.json'
        payload = json.loads(p.read_text(encoding='utf-8'))
        payload['gates'][0]['requires'] = ['ui-motion-system-i']
        p.write_text(json.dumps(payload), encoding='utf-8')
        cycle_error = _expect_error(lambda: learner.load_ui_gates(base), 'cyclic UI learning gate dependency')

    print(json.dumps({
        'ok': True,
        'policy': learner.UI_POLICY,
        'gate_files': EXPECTED_FILES,
        'gate_count': len(gates),
        'final_gate': EXPECTED_FINAL_GATE,
        'core_gate_separated': True,
        'dependency_order_valid': True,
        'duplicate_guard': duplicate_error,
        'missing_dependency_guard': missing_error,
        'cycle_guard': cycle_error,
        'production_promotion': False,
    }, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
