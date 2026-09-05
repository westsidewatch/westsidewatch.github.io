import unittest

from dore_core.capabilities.providers import sanitize_system_stats


class ProviderSanitizationTests(unittest.TestCase):
    def test_system_stats_drops_argv_paths_and_unknown_fields(self):
        payload = {
            "system": {
                "os": "darwin",
                "python_version": "3.12",
                "comfyui_version": "0.33.0",
                "ram_total": 123,
                "argv": ["python", "main.py", "--output-directory", "/Users/private/render"],
                "secret_path": "/Users/private/models",
            },
            "devices": [{
                "name": "mps",
                "type": "mps",
                "index": 0,
                "vram_total": 456,
                "vram_free": 321,
                "model_path": "/Users/private/checkpoints/model.safetensors",
            }],
            "unknown": {"token": "secret"},
        }
        safe = sanitize_system_stats(payload)
        self.assertEqual(safe["system"]["os"], "darwin")
        self.assertEqual(safe["devices"][0]["vram_free"], 321)
        rendered = repr(safe)
        self.assertNotIn("argv", rendered)
        self.assertNotIn("/Users/private", rendered)
        self.assertNotIn("token", rendered)
        self.assertNotIn("model_path", rendered)

    def test_empty_or_unexpected_shapes_fail_to_minimal_metadata(self):
        self.assertEqual(sanitize_system_stats({}), {})
        self.assertEqual(sanitize_system_stats({"system": "bad", "devices": "bad"}), {})


if __name__ == "__main__":
    unittest.main()
