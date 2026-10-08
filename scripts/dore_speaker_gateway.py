#!/usr/bin/env python3
"""Restricted speaker worker binding for the existing Companion A2A ingress."""
import hashlib
import json
import os
import shlex
import subprocess
import sys
import threading
from pathlib import Path

CAPABILITY = 'design.speaker-cover.render'
ROOT = Path(os.environ.get('DORE_SPEAKER_WORKER_ROOT') or Path(__file__).resolve().parents[1]).resolve()
PYTHON = os.environ.get('DORE_SPEAKER_PYTHON') or sys.executable
LOCK = threading.Lock()


def dispatch(payload):
    if not isinstance(payload, dict) or payload.get('capability_id') != CAPABILITY:
        return None
    reply = {key: payload.get(key) for key in
             ('request_id', 'conversation_id', 'session_id', 'consumer_id', 'capability_id')}
    reply['protocol'] = 'dore.a2a/1'
    try:
        if payload.get('protocol') != 'dore.a2a/1' or payload.get('action', 'dispatch') != 'dispatch':
            raise ValueError('Unsupported speaker envelope')
        for key in ('request_id', 'conversation_id', 'session_id'):
            if not isinstance(payload.get(key), str) or not payload[key].strip():
                raise ValueError('Missing ' + key)
        if payload.get('consumer_id') != 'design':
            raise ValueError('Speaker worker requires design consumer')
        args = payload.get('payload', {})
        if not isinstance(args, dict) or set(args) - {'speaker', 'dry_run'}:
            raise ValueError('Only speaker and dry_run are accepted')
        speaker = args.get('speaker', 'david-pawson')
        records = json.loads((ROOT / 'data/westside-core/entities/sermon-speakers.v1.json').read_text())['records']
        if not isinstance(speaker, str) or 'speaker:' + speaker not in {r['id'] for r in records}:
            raise ValueError('Unknown canonical speaker')
        dry = args.get('dry_run', False)
        if not isinstance(dry, bool):
            raise ValueError('dry_run must be boolean')
        key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        base = ROOT / 'local/dore-speaker-jobs/a2a' / key
        job = base / speaker
        receipt = base / 'receipt.json'
        if not LOCK.acquire(blocking=False):
            raise RuntimeError('Speaker worker busy; retry later')
        try:
            if receipt.exists():
                return json.loads(receipt.read_text())
            subprocess.run([PYTHON, str(ROOT / 'scripts/prepare_dore_local_image_job.py'),
                            '--speaker', speaker, '--out', str(base)], check=True, capture_output=True, text=True, timeout=30)
            backend = shlex.join([PYTHON, str(ROOT / 'scripts/dore_speaker_image_backend.py'),
                                  '--prompt-file', '{prompt_file}', '--output-file', '{output_file}'])
            command = [PYTHON, str(ROOT / 'scripts/run_dore_speaker_a2a.py'), '--job', str(job), '--backend-command', backend]
            if dry:
                command.append('--dry-run')
            process = subprocess.run(command, capture_output=True, text=True, timeout=2000)
            if process.returncode:
                raise RuntimeError(process.stderr[-1800:] or process.stdout[-1800:])
            result = json.loads(process.stdout)
            reply.update(status='succeeded', result=result)
            if not dry:
                result['provenance'] = json.loads((job / 'generated-background.png.provenance.json').read_text())
                receipt.write_text(json.dumps(reply, ensure_ascii=False, indent=2) + '\n')
            return reply
        finally:
            LOCK.release()
    except Exception as exc:
        reply.update(status='failed', error={'code': 'speaker_worker_failed', 'message': str(exc)})
        return reply
