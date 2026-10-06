#!/usr/bin/env python3
"""Deterministic contract tests for Doré Video task progress."""
import importlib.util
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BRIDGE=ROOT/"local"/"dore-local"/"video_bridge.py"
spec=importlib.util.spec_from_file_location("dore_video_bridge",BRIDGE)
bridge=importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        video=root/"0_video"; audio=root/"1_audio"
        video.mkdir(); audio.mkdir()
        for i in range(3):
            (video/f"{i:03}.ts").write_bytes(b"v")
            (audio/f"{i:03}.ts").write_bytes(b"a")
        (video/"._000.ts").write_bytes(b"meta")
        p=bridge.segment_progress(root,5)
        assert p=={"segments":3,"total_segments":5,"percent":60},p
        for i in range(3,5):
            (video/f"{i:03}.ts").write_bytes(b"v")
            (audio/f"{i:03}.ts").write_bytes(b"a")
        p=bridge.segment_progress(root,5)
        assert p=={"segments":5,"total_segments":5,"percent":100},p
        q=bridge.segment_progress(root)
        assert q=={"segments":5},q
    print("Doré Video progress contract: PASS")

if __name__=="__main__": main()
