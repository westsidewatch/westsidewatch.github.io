from __future__ import annotations

import unittest

from dore_core.capabilities.image_renderer import ComfyUIRenderer, RenderRequest
from dore_core.capabilities.image_style import compile_editorial_recipe
from dore_core.capabilities.providers import ProviderDescriptor


class ImageStyleTests(unittest.TestCase):
    def test_compiler_enforces_editorial_grammar(self):
        recipe = compile_editorial_recipe({"dominant_ink": "gold", "accent_ink": "black"})
        self.assertEqual(recipe.grammar, "dore.editorial-mono.v1")
        self.assertLessEqual(recipe.dominant_ratio, .85)
        self.assertGreaterEqual(recipe.empty_paper_ratio, .25)
        self.assertIn("reference is grammar not template", recipe.invariants)

    def test_compiler_rejects_style_drift(self):
        with self.assertRaises(ValueError):
            compile_editorial_recipe({"empty_paper_ratio": .1})
        with self.assertRaises(ValueError):
            compile_editorial_recipe({"dominant_ratio": .95})


class RendererContractTests(unittest.TestCase):
    def test_paid_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            ComfyUIRenderer(ProviderDescriptor("x", "http-json", "http://127.0.0.1:8188", "metered"))

    def test_image_refs_are_structured(self):
        item = {"outputs": {"9": {"images": [{"filename": "a.png", "subfolder": "", "type": "output"}]}}}
        refs = ComfyUIRenderer.image_refs(item)
        self.assertEqual(refs[0]["filename"], "a.png")
        self.assertEqual(refs[0]["type"], "output")

    def test_render_request_carries_provenance_inputs(self):
        req = RenderRequest({"1": {"class_type": "SaveImage"}}, seed=42, model="local-model", workflow_id="acceptance")
        self.assertEqual(req.seed, 42)
        self.assertEqual(req.model, "local-model")


if __name__ == "__main__":
    unittest.main()
