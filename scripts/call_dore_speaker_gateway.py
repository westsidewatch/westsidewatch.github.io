#!/usr/bin/env python3
"""Call the installed Mac mini A2A speaker capability; no remote shell needed."""
import argparse
import json
import uuid
from urllib.request import Request, urlopen

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--speaker', default='david-pawson')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--request-id', default=None, help='Reuse to replay a completed receipt')
    args = parser.parse_args()
    payload = {'protocol': 'dore.a2a/1', 'action': 'dispatch',
               'request_id': args.request_id or str(uuid.uuid4()),
               'conversation_id': 'dore-speaker-cover', 'session_id': 'mac-mini',
               'consumer_id': 'design', 'capability_id': 'design.speaker-cover.render',
               'payload': {'speaker': args.speaker, 'dry_run': args.dry_run}}
    request = Request('http://127.0.0.1:4312/a2a', data=json.dumps(payload).encode(),
                      headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=2100) as response:
        result = json.load(response)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get('status') == 'succeeded' else 1)
