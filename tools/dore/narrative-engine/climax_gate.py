#!/usr/bin/env python3
"""Detect narrative truncation at the Golden Gate siege climax."""
import json
import re
from pathlib import Path
from narrative import extract

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md"

def check(text):
    section = extract(text)
    required = {
        "siege_opening": r"六月(?:七日|七日前後)",
        "failed_assault": r"六月十三日",
        "siege_tower": r"攻城塔",
        "final_assault": r"七月十四日|七月十五日",
        "civilian_aftermath": r"屠殺|殺戮|遇害|居民.{0,25}(?:死|殺)",
    }
    found = {name: bool(re.search(pattern, section)) for name, pattern in required.items()}
    tail = section[-1100:]
    premature = bool(re.search(r"真正的攻城還在後面", tail))
    return {"status": "PASS" if all(found.values()) and not premature else "BLOCK",
            "required_beats": found, "ends_before_climax": premature,
            "source": str(SOURCE.relative_to(ROOT))}

def test():
    raw = SOURCE.read_text(encoding="utf-8")
    result = check(raw)
    assert result["status"] == "BLOCK" if "真正的攻城還在後面" in extract(raw)[-1100:] else True
    sample = "## 金門\n\n六月七日開始圍城。六月十三日攻城失敗。攻城塔完成。七月十五日登城。居民遇害。"
    assert check(sample)["status"] == "PASS"
    assert check(sample.replace("居民遇害", "勝利慶祝"))["status"] == "BLOCK"
    assert check(sample.replace("七月十五日登城", "七月漸近"))["status"] == "BLOCK"
    print("PASS: climax and civilian-aftermath regression checks")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print(json.dumps(check(SOURCE.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
