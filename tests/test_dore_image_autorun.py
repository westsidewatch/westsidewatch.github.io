from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dore_core.capabilities.image_runtime_config import load_resident_image_config


class ResidentImageAutorunTests(unittest.TestCase):
    def test_config_is_loopback_only(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "resident.json"
            path.write_text(json.dumps({
                "schema": "dore.image.resident.v1",
                "endpoint": "https://paid.example/image",
                "model": "x",
                "template": "x.json",
                "output_dir": "out",
            }))
            with self.assertRaises(ValueError):
                load_resident_image_config(path)

    def test_local_config_loads_without_provider_dependency(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "resident.json"
            path.write_text(json.dumps({
                "schema": "dore.image.resident.v1",
                "endpoint": "http://127.0.0.1:8188",
                "model": "local.safetensors",
                "template": "dore-image/workflows/editorial.json",
                "output_dir": "dore-image/generated",
            }))
            cfg = load_resident_image_config(path)
            self.assertEqual(cfg.endpoint, "http://127.0.0.1:8188")
            self.assertEqual(cfg.model, "local.safetensors")

    def test_missing_required_fields_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "resident.json"
            path.write_text(json.dumps({"schema": "dore.image.resident.v1", "endpoint": "http://localhost:8188"}))
            with self.assertRaises(ValueError):
                load_resident_image_config(path)


if __name__ == "__main__":
    unittest.main()
