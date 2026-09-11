import importlib.util
import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
for name in ("mask_evidence", "plan_anchors", "run_aw011", "scaffold_gate", "run_pipeline"):
    if name in sys.modules:
        continue
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)

MODULE = sys.modules["run_pipeline"]


def write_png(path: Path, width: int, height: int, samples: list[int]) -> None:
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


class PipelineTests(unittest.TestCase):
    def fixture(self, root: Path):
        source = root / "dore-011.bin"
        source.write_bytes(b"canonical")
        (root / "camera.json").write_text(json.dumps({"poses": [{"id":"P000"},{"id":"P001"},{"id":"P000"}]}), encoding="utf-8")
        write_png(root / "unseen.png", 2, 2, [0, 0, 255, 255])
        write_png(root / "coverage.png", 2, 2, [0, 0, 255, 255])
        (root / "mask.json").write_text(json.dumps({
            "max_residual_unseen_fraction": 0.0,
            "poses": [{"id":"P001","unseen_mask":"unseen.png"}],
            "candidates": [{"id":"A001","coverage_masks":{"P001":"coverage.png"}}]
        }), encoding="utf-8")
        production = root / "production.json"
        production.write_text(json.dumps({
            "aw_id":"AW-011",
            "source":{"asset":"dore-011.bin","canonical_pose_id":"P000"},
            "camera":{"spine_file":"camera.json"},
            "scaffold":{"provider":"fixture"},
            "anchors":{"mask_manifest_file":"mask.json"}
        }), encoding="utf-8")
        return production, source

    def test_stops_cleanly_while_waiting_for_scaffold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            production, _ = self.fixture(root)
            report = MODULE.run(production, root / "out")
            self.assertEqual(report["status"], "AWAITING_SCAFFOLD")

    def test_accepts_scaffold_and_advances_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            production, source = self.fixture(root)
            write_png(root / "known.png", 2, 2, [10,20,30,40])
            write_png(root / "known-mask.png", 2, 2, [255,255,0,0])
            write_png(root / "unseen-scaffold.png", 2, 2, [0,0,255,255])
            import hashlib
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            scaffold = root / "scaffold.json"
            scaffold.write_text(json.dumps({
                "aw_id":"AW-011",
                "canonical_source_sha256":source_sha,
                "provider":"fixture",
                "poses":[{"id":"P001","known":"known.png","known_mask":"known-mask.png","unseen_mask":"unseen-scaffold.png"}]
            }), encoding="utf-8")
            report = MODULE.run(production, root / "out", scaffold)
            self.assertEqual(report["status"], "SCAFFOLD_ACCEPTED")
            self.assertEqual(report["scaffold"]["pose_count"], 1)


if __name__ == "__main__":
    unittest.main()
