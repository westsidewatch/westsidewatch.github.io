#!/usr/bin/env python3
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError
import dore_speaker_gateway as gateway
import dore_speaker_image_backend as backend


class GatewayTests(unittest.TestCase):
    def envelope(self, **args):
        return {'protocol': 'dore.a2a/1', 'request_id': 'gateway-test',
                'conversation_id': 'test', 'session_id': 'test', 'consumer_id': 'design',
                'capability_id': gateway.CAPABILITY, 'payload': args}

    def test_legacy_capabilities_are_not_intercepted(self):
        self.assertIsNone(gateway.dispatch({'capability_id': 'design.compose'}))

    def test_arbitrary_backend_commands_are_rejected(self):
        result = gateway.dispatch(self.envelope(backend_command='rm -rf /'))
        self.assertEqual(result['status'], 'failed')
        self.assertIn('Only speaker', result['error']['message'])

    def test_unknown_speaker_and_path_escape_are_rejected(self):
        self.assertEqual(gateway.dispatch(self.envelope(speaker='../../escape'))['status'], 'failed')

    def test_non_boolean_dry_run_is_rejected(self):
        self.assertEqual(gateway.dispatch(self.envelope(dry_run='false'))['status'], 'failed')

    def test_busy_worker_fails_without_starting_another_model(self):
        gateway.LOCK.acquire()
        try:
            self.assertIn('busy', gateway.dispatch(self.envelope())['error']['message'])
        finally:
            gateway.LOCK.release()

    def test_no_network_or_model_required_for_dry_run(self):
        result = gateway.dispatch(self.envelope(dry_run=True))
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(result['result']['status'], 'READY_FOR_A2A')

    def test_svg_fallback_is_refused(self):
        from io import BytesIO
        with patch.object(backend, 'urlopen', return_value=BytesIO(json.dumps({'model_backed': False}).encode())):
            with self.assertRaisesRegex(RuntimeError, 'SVG fallback refused'):
                backend.generate('unused', 'unused')


if __name__ == '__main__':
    unittest.main()
