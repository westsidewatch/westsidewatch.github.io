import unittest
from unittest.mock import patch
import conversation_gateway as gateway


class GatewayTests(unittest.TestCase):
    def test_canonical_a2a_success_is_preserved(self):
        result = {'status': 'succeeded', 'execution': {'execution_status': 'PASS', 'completion_evidence': {'verified': True}}}
        with patch.object(gateway.native_host, 'route_payload', return_value=result) as route:
            response = gateway.call('context.fuzzy-search', {'query': 'test'}, request_id='contract-1')
        self.assertTrue(response['ok'])
        self.assertEqual(response['result'], result)
        self.assertEqual(route.call_args.args[0]['request_id'], 'contract-1')

    def test_failed_or_pending_status_overrides_legacy_ok(self):
        for status in ('failed', 'pending', 'running'):
            with self.subTest(status=status), patch.object(gateway.native_host, 'route_payload', return_value={'status': status, 'ok': True}):
                self.assertFalse(gateway.call('test', {})['ok'])

    def test_legacy_success_without_status(self):
        with patch.object(gateway.native_host, 'route_payload', return_value={'ok': True}):
            self.assertTrue(gateway.call('test', {})['ok'])


if __name__ == '__main__':
    unittest.main()
