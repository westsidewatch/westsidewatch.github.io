from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dore_core.capabilities.image_pipeline import generate_resident_image
from dore_core.capabilities.image_renderer import RenderArtifact
from dore_core.capabilities.image_workflow import WorkflowTemplate


class FakeRenderer:
    def render(self, request):
        self.request = request
        return RenderArtifact(
            "prompt-1",
            ({"filename": "asset.png", "subfolder": "", "type": "output"},),
            {"engine": "comfyui", "provider": "fake-local", "cost_class": "local_free", "seed": request.seed},
        )

    def fetch_image(self, ref, target: Path):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"\x89PNG\r\n\x1a\nactual-render-bytes")
        return target


class ResidentPipelineTests(unittest.TestCase):
    def test_pipeline_reaches_real_bytes_but_not_visual_acceptance(self):
        graph = {str(i): {"inputs": {}} for i in (3, 4, 6, 7)}
        template = WorkflowTemplate("editorial", graph)
        renderer = FakeRenderer()
        with tempfile.TemporaryDirectory() as td:
            result = generate_resident_image(
                renderer=renderer,
                template=template,
                brief={"dominant_ink": "gold", "accent_ink": "black"},
                subject="Jerusalem at dawn",
                model="local.safetensors",
                seed=101,
                output_dir=Path(td),
            )
            self.assertTrue(Path(result.artifact.uri).exists())
            self.assertGreater(result.artifact.bytes, 8)
            self.assertTrue(result.artifact.sha256)
            self.assertFalse(result.critic_input["real_visual_review"])
            self.assertEqual(renderer.request.seed, 101)
            self.assertIn("Jerusalem at dawn", renderer.request.workflow["6"]["inputs"]["text"])
            self.assertTrue((Path(td) / "prompt-1.json").exists())

    def test_correction_direction_reenters_generation_prompt(self):
        graph = {str(i): {"inputs": {}} for i in (3, 4, 6, 7)}
        renderer = FakeRenderer()
        with tempfile.TemporaryDirectory() as td:
            generate_resident_image(
                renderer=renderer,
                template=WorkflowTemplate("editorial", graph),
                brief={},
                subject="watchman",
                model="local.safetensors",
                seed=5,
                output_dir=Path(td),
                correction_direction="restore 35% visible paper",
            )
            prompt = renderer.request.workflow["6"]["inputs"]["text"]
            self.assertIn("restore 35% visible paper", prompt)


if __name__ == "__main__":
    unittest.main()
