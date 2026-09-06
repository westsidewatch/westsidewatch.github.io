import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / 'runtime'
sys.path.insert(0, str(RUNTIME))
import wake_runtime as wr  # noqa: E402


class WakeRuntimeTests(unittest.TestCase):
    def test_probe_idempotency_and_pass(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / 'wake.sqlite3'
            conn = wr.connect(db)
            payload = {'argv': [sys.executable, '-c', 'raise SystemExit(0)']}
            a = wr.enqueue(conn, 'probe', payload, idempotency_key='same')
            b = wr.enqueue(conn, 'probe', payload, idempotency_key='same')
            self.assertEqual(a, b)
            conn.close()
            result = wr.run_once(db)
            self.assertEqual(result['passed'], 1)
            rows = wr.status(db)
            self.assertEqual(rows[0]['state'], 'passed')

    def test_failed_probe_retries_then_fails(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / 'wake.sqlite3'
            conn = wr.connect(db)
            task_id = wr.enqueue(
                conn,
                'probe',
                {'argv': [sys.executable, '-c', 'raise SystemExit(7)']},
                max_attempts=1,
            )
            conn.close()
            wr.run_once(db)
            rows = wr.status(db)
            row = next(x for x in rows if x['id'] == task_id)
            self.assertEqual(row['state'], 'failed')

    def test_promote_file_requires_passing_verifier_and_keeps_backup(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            db = root / 'wake.sqlite3'
            target = root / 'target.txt'
            candidate = root / 'candidate.txt'
            target.write_text('old', encoding='utf-8')
            candidate.write_text('new', encoding='utf-8')
            conn = wr.connect(db)
            task_id = wr.enqueue(
                conn,
                'promote_file',
                {
                    'candidate_path': str(candidate),
                    'target_path': str(target),
                    'verifier_argv': [sys.executable, '-c', "from pathlib import Path; raise SystemExit(0 if Path(r'%s').read_text() == 'new' else 1)" % candidate],
                },
                max_attempts=1,
            )
            conn.close()
            result = wr.run_once(db)
            self.assertEqual(result['passed'], 1)
            self.assertEqual(target.read_text(encoding='utf-8'), 'new')
            conn = sqlite3.connect(db)
            row = conn.execute('SELECT backup_path,status FROM promotion_log WHERE task_id=?', (task_id,)).fetchone()
            conn.close()
            self.assertEqual(row[1], 'promoted')
            self.assertEqual(Path(row[0]).read_text(encoding='utf-8'), 'old')

    def test_failed_verifier_never_promotes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            db = root / 'wake.sqlite3'
            target = root / 'target.txt'
            candidate = root / 'candidate.txt'
            target.write_text('old', encoding='utf-8')
            candidate.write_text('bad', encoding='utf-8')
            conn = wr.connect(db)
            wr.enqueue(
                conn,
                'promote_file',
                {
                    'candidate_path': str(candidate),
                    'target_path': str(target),
                    'verifier_argv': [sys.executable, '-c', 'raise SystemExit(1)'],
                },
                max_attempts=1,
            )
            conn.close()
            wr.run_once(db)
            self.assertEqual(target.read_text(encoding='utf-8'), 'old')
            self.assertEqual(wr.status(db)[0]['state'], 'failed')

    def test_expired_lease_is_recovered(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / 'wake.sqlite3'
            conn = wr.connect(db)
            task_id = wr.enqueue(conn, 'probe', {'argv': [sys.executable, '-c', 'raise SystemExit(0)']})
            conn.execute("UPDATE wake_tasks SET state='running', lease_until=0 WHERE id=?", (task_id,))
            conn.commit()
            recovered = wr.recover_expired_leases(conn)
            state = conn.execute('SELECT state FROM wake_tasks WHERE id=?', (task_id,)).fetchone()[0]
            conn.close()
            self.assertEqual(recovered, 1)
            self.assertEqual(state, 'pending')


if __name__ == '__main__':
    unittest.main()
