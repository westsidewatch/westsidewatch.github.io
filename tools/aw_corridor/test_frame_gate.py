import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
for name in ("mask_evidence", "png_raster", "frame_gate"):
    if name in sys.modules:
        continue
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)

PNG = sys.modules["png_raster"]
MODULE = sys.modules["frame_gate"]


class FrameGateTests(unittest.TestCase):
    def test_generated_pixels_enter_only_unseen_region(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            known = bytes([10,11,12, 20,21,22, 30,31,32, 40,41,42])
            generated = bytes([110,111,112, 120,121,122, 130,131,132, 140,141,142])
            PNG.write_png(root/"known.png", 2, 2, 3, known)
            PNG.write_png(root/"generated.png", 2, 2, 3, generated)
            PNG.write_png(root/"mask.png", 2, 2, 1, bytes([0,255,0,255]))
            report = MODULE.compose(root/"known.png", root/"generated.png", root/"mask.png", root/"out.png")
            _, _, _, out = PNG.read_png(root/"out.png")
            self.assertEqual(out, bytes([10,11,12, 120,121,122, 30,31,32, 140,141,142]))
            self.assertEqual(report["known_channel_delta_count"], 0)
            self.assertEqual(report["unseen_pixel_count"], 2)

    def test_dimension_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            PNG.write_png(root/"known.png", 2, 2, 3, bytes(range(12)))
            PNG.write_png(root/"generated.png", 1, 2, 3, bytes(range(6)))
            PNG.write_png(root/"mask.png", 2, 2, 1, bytes([0,255,0,255]))
            with self.assertRaises(MODULE.FrameGateError):
                MODULE.compose(root/"known.png", root/"generated.png", root/"mask.png", root/"out.png")

    def test_channel_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            PNG.write_png(root/"known.png", 2, 2, 3, bytes(range(12)))
            PNG.write_png(root/"generated.png", 2, 2, 4, bytes(range(16)))
            PNG.write_png(root/"mask.png", 2, 2, 1, bytes([0,255,0,255]))
            with self.assertRaises(MODULE.FrameGateError):
                MODULE.compose(root/"known.png", root/"generated.png", root/"mask.png", root/"out.png")


if __name__ == "__main__":
    unittest.main()
