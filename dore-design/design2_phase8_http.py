#!/usr/bin/env python3
"""Phase 8 HTTP bridge for contextual Doré Design intelligence."""
import json
from urllib.parse import urlparse

import design_intelligence_runtime as intelligence


def install(handler_cls, base):
    original_get = handler_cls.do_GET
    original_post = handler_cls.do_POST

    def body(self, limit=262144):
        size = int(self.headers.get('Content-Length', '0'))
        if size < 1 or size > limit:
            raise ValueError('invalid_body_size')
        return json.loads(self.rfile.read(size))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/design2/intelligence/health':
            try:
                with intelligence.connect() as conn:
                    status = intelligence.route_task({}, conn=conn)
                return self.out(200, {
                    'ok': True,
                    'service': 'dore-design-intelligence',
                    'phase': 8,
                    'policy': status['policy'],
                    'model_inference_connected': status['model_inference_connected'],
                    'authority': status['authority'],
                })
            except Exception as exc:
                return self.out(503, {'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)})
        return original_get(self)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            if path == '/api/design2/intelligence/route':
                return self.out(200, intelligence.route_task(body(self)))
            if path == '/api/design2/intelligence/comparison':
                return self.out(201, intelligence.record_observed_comparison(body(self)))
            if path == '/api/design2/intelligence/rejection':
                return self.out(201, intelligence.record_observed_rejection(body(self)))
        except Exception as exc:
            return self.out(400, {'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)})
        return original_post(self)

    handler_cls.do_GET = do_GET
    handler_cls.do_POST = do_POST
    return handler_cls
