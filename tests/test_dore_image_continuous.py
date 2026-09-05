from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dore_core.capabilities.image_artifacts import persist_record, record_image
from dore_core.capabilities.image_critic import correction_direction, critique_from_observations
from dore_core.capabilities.image_style import compile_editorial_recipe
from dore_core.capabilities.image_workflow import WorkflowTemplate, compile_comfy_workflow


class ContinuousImageTests(unittest.TestCase):
    def test_recipe_compiles_into_provider_graph(self):
        graph = {str(i): {"inputs": {}} for i in (3, 4, 6, 7)}
        recipe = compile_editorial_recipe({"dominant_ink": "gold", "accent_ink": "black"})
        result = compile_comfy_workflow(WorkflowTemplate("x", graph), subject="Jerusalem at dawn", recipe=recipe, model="model.safetensors", seed=77)
        self.assertEqual(result["3"]["inputs"]["seed"], 77)
        self.assertEqual(result["4"]["inputs"]["ckpt_name"], "model.safetensors")
        self.assertIn("visible warm paper", result["6"]["inputs"]["text"])

    def test_artifact_record_hashes_real_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            image = Path(td) / "asset.png"
            image.write_bytes(b"real-render-bytes")
            record = record_image(image, provenance={"seed": 1}, recipe={"grammar": "x"}, brief={"subject": "x"})
            manifest = Path(td) / "asset.json"
            persist_record(record, manifest)
            self.assertTrue(record.sha256)
            self.assertEqual(record.bytes, len(b"real-render-bytes"))
            self.assertTrue(manifest.exists())

    def test_critic_cannot_accept_without_real_visual_review(self):
        recipe = compile_editorial_recipe({}).to_payload()
        observations = {"composition": .9, "style_fidelity": .9, "typography": .9, "product_fit": .9, "empty_paper_ratio": .35, "ink_count": 2}
        result = critique_from_observations(recipe, observations, real_visual_review=False)
        self.assertFalse(result.accepted)

    def test_critic_emits_correction_direction(self):
        result = critique_from_observations({}, {"composition": .4, "style_fidelity": .8, "typography": .4, "product_fit": .4, "empty_paper_ratio": .1, "ink_count": 4}, real_visual_review=True)
        self.assertFalse(result.accepted)
        self.assertIn("restore 25–55%", correction_direction(result))
        self.assertIn("target product surface", correction_direction(result))


if __name__ == "__main__":
    unittest.main()
