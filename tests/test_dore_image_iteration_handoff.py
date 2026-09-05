from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dore_core.capabilities.image_artifacts import ImageArtifactRecord
from dore_core.capabilities.image_handoff import build_design_image_patch
from dore_core.capabilities.image_iteration import iterate_image
from dore_core.capabilities.image_renderer import RenderArtifact
from dore_core.capabilities.image_workflow import WorkflowTemplate


class FakeRenderer:
    def __init__(self):
        self.count = 0

    def render(self, request):
        self.count += 1
        return RenderArtifact(
            f"prompt-{self.count}",
            ({"filename": f"asset-{self.count}.png", "subfolder": "", "type": "output"},),
            {"engine": "comfyui", "provider": "fake-local", "cost_class": "local_free", "seed": request.seed},
        )

    def fetch_image(self, ref, target: Path):
        target.write_bytes(b"\x89PNG\r\n\x1a\n" + ref["filename"].encode())
        return target


class IterationAndHandoffTests(unittest.TestCase):
    def test_loop_corrects_then_accepts(self):
        graph = {str(i): {"inputs": {}} for i in (3, 4, 6, 7)}
        seen = {"n": 0}

        def vision_reader(path, recipe, brief):
            seen["n"] += 1
            if seen["n"] == 1:
                return {"composition": .4, "style_fidelity": .9, "typography": .8, "product_fit": .8, "empty_paper_ratio": .1, "ink_count": 2}
            return {"composition": .9, "style_fidelity": .9, "typography": .9, "product_fit": .9, "empty_paper_ratio": .35, "ink_count": 2}

        with tempfile.TemporaryDirectory() as td:
            result = iterate_image(
                renderer=FakeRenderer(), template=WorkflowTemplate("editorial", graph), brief={},
                subject="watchman", model="local.safetensors", seed=10, output_dir=Path(td),
                vision_reader=vision_reader, max_iterations=3,
            )
            self.assertTrue(result.accepted)
            self.assertEqual(len(result.steps), 2)
            self.assertEqual(result.stop_reason, "accepted")

    def test_handoff_preserves_asset_identity(self):
        artifact = ImageArtifactRecord("image:abc", "/tmp/a.png", "abc123", 10, {"seed": 1}, {"grammar": "x"}, {"subject": "x"})
        patch = build_design_image_patch(artifact, page_id="cover", placement={"x": 0, "y": 0, "w": 1200, "h": 930})
        self.assertEqual(patch.schema, "dore.design.image-patch.v1")
        self.assertEqual(patch.asset_id, "image:abc")
        self.assertEqual(patch.sha256, "abc123")
        self.assertEqual(patch.fit, "cover")

    def test_handoff_rejects_invalid_geometry(self):
        artifact = ImageArtifactRecord("image:abc", "/tmp/a.png", "abc123", 10, {}, {}, {})
        with self.assertRaises(ValueError):
            build_design_image_patch(artifact, page_id="cover", placement={"x": 0, "y": 0, "w": 0, "h": 930})


if __name__ == "__main__":
    unittest.main()
