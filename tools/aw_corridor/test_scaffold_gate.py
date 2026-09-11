import hashlib
import importlib.util
import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
for name in ("mask_evidence", "scaffold_gate"):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)

MODULE = sys.modules["scaffold_gate"]


def write_png(path: Path, width: int, height: int, samples: list[int]) -> None:
    assert len(samples) == width * height
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw.extend(samples[y * width : (y + 1) * width])
    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
    data = bytearray(b"\x89PNG\r\n\x1a\n")
    data.extend(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)))
    data.extend(chunk(b"IDAT", zlib.compress(bytes(raw))))
    data.extend(chunk(b"IEND", b""))
    path.write_bytes(bytes(data))


class ScaffoldGateTests(unittest.TestCase):
    def make_fixture(self, root: Path, *, known_mask=None, unseen_mask=None, source_sha="abc"):
        write_png(root / "known.png", 2, 2, [10, 20, 30, 40])
        write_png(root / "known-mask.png", 2, 2, known_mask or [255, 255, 0, 0])
        write_png(root / "unseen-mask.png", 2, 2, unseen_mask or [0, 0, 255, 255])
        build = {
            "aw_id": "AW-011",
            "source": {"sha256": source_sha, "canonical_pose_id": "P000"},
            "camera": {"ordered_pose_ids": ["P000", "P001", "P000"]},
        }
        scaffold = {
            "aw_id": "AW-011",
            "canonical_source_sha256": source_sha,
            "provider": "fixture-provider",
            "poses": [{
                "id": "P001",
                "known": "known.png",
                "known_mask": "known-mask.png",
                "unseen_mask": "unseen-mask.png"
            }]
        }
        (root / "build.json").write_text(json.dumps(build), encoding="utf-8")
        (root / "scaffold.json").write_text(json.dumps(scaffold), encoding="utf-8")
        return root / "build.json", root / "scaffold.json"

    def test_accepts_complete_partition_bound_to_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build, scaffold = self.make_fixture(root)
            report = MODULE.validate(build, scaffold)
            self.assertEqual(report["status"], "SCAFFOLD_ACCEPTED")
            self.assertEqual(report["pose_count"], 1)
            self.assertEqual(report["poses"][0]["known_pixels"], 2)
            self.assertEqual(report["poses"][0]["unseen_pixels"], 2)

    def test_rejects_source_fingerprint_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build, scaffold = self.make_fixture(root)
            obj = json.loads(scaffold.read_text())
            obj["canonical_source_sha256"] = "wrong"
            scaffold.write_text(json.dumps(obj), encoding="utf-8")
            with self.assertRaises(MODULE.ScaffoldError):
                MODULE.validate(build, scaffold)

    def test_rejects_mask_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build, scaffold = self.make_fixture(
                root,
                known_mask=[255, 255, 0, 0],
                unseen_mask=[255, 0, 255, 255],
            )
            with self.assertRaises(MODULE.ScaffoldError):
                MODULE.validate(build, scaffold)

    def test_rejects_mask_holes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build, scaffold = self.make_fixture(
                root,
                known_mask=[255, 0, 0, 0],
                unseen_mask=[0, 0, 255, 255],
            )
            with self.assertRaises(MODULE.ScaffoldError):
                MODULE.validate(build, scaffold)

    def test_rejects_canonical_pose_from_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build, scaffold = self.make_fixture(root)
            obj = json.loads(scaffold.read_text())
            obj["poses"].append({
                "id": "P000",
                "known": "known.png",
                "known_mask": "known-mask.png",
                "unseen_mask": "unseen-mask.png"
            })
            scaffold.write_text(json.dumps(obj), encoding="utf-8")
            with self.assertRaises(MODULE.ScaffoldError):
                MODULE.validate(build, scaffold)


if __name__ == "__main__":
    unittest.main()
