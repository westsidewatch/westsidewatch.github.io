#!/usr/bin/env python3
"""Phase 9 HTTP bridge: Design exploration through Core/A2A only."""
import json
from urllib.parse import urlparse

import design_intelligence_a2a as bridge


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
        if path == '/api/design2/intelligence/a2a-health':
            try:
                return self.out(200, {'service': 'dore-design-intelligence', **bridge.health()})
            except Exception as exc:
                return self.out(503, {'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)})
        return original_get(self)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/design2/intelligence/explore':
            try:
                return self.out(200, bridge.explore(body(self)))
            except Exception as exc:
                return self.out(400, {'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)})
        return original_post(self)

    handler_cls.do_GET = do_GET
    handler_cls.do_POST = do_POST
    return handler_cls
