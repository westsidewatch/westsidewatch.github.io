import unittest

from dore_core.capabilities.image_artifacts import ImageArtifactRecord
from dore_core.capabilities.image_handoff import build_design_image_patch


class NativeAssetShapeTests(unittest.TestCase):
    def test_generated_artifact_compiles_to_asset_and_normal_image_shape(self):
        artifact = ImageArtifactRecord(
            "image:abc", "/tmp/a.png", "abc123", 10,
            {"seed": 7}, {"grammar": "editorial-mono"}, {"subject": "watchman"},
        )
        patch = build_design_image_patch(
            artifact,
            page_id="cover",
            placement={"x": 72, "y": 80, "w": 720, "h": 850},
            fit="cover",
        )
        asset, shape = patch.to_asset_and_shape()
        self.assertEqual(asset.id, "image:abc")
        self.assertEqual(asset.kind, "image")
        self.assertEqual(asset.sha256, "abc123")
        self.assertEqual(shape.type, "image")
        self.assertEqual(shape.asset_id, asset.id)
        self.assertEqual((shape.x, shape.y, shape.w, shape.h), (72.0, 80.0, 720.0, 850.0))
        self.assertEqual(shape.fit, "cover")

    def test_asset_identity_is_independent_from_canvas_engine(self):
        artifact = ImageArtifactRecord("image:stable", "/tmp/a.png", "hash", 1, {}, {}, {})
        patch = build_design_image_patch(
            artifact, page_id="cover", placement={"x": 0, "y": 0, "w": 100, "h": 100}
        )
        asset, shape = patch.to_asset_and_shape()
        payload = {"asset": asset.to_payload(), "shape": shape.to_payload()}
        serialized = repr(payload).lower()
        self.assertNotIn("konva", serialized)
        self.assertNotIn("polotno", serialized)
        self.assertNotIn("tldraw", serialized)


if __name__ == "__main__":
    unittest.main()
