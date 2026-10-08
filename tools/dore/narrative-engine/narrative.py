#!/usr/bin/env python3
"""Deterministic scene inventory and editorial checks for historical nonfiction."""
import argparse
import json
import re
from pathlib import Path

SECTION = "金門"
HEAD = re.compile(r"^## (.+)$", re.M)
DATES = re.compile(r"(?:10[0-9]{2}|11[0-9]{2})年(?:[一二三四五六七八九十0-9]+月)?|(?:六月|七月)(?:[一二三四五六七八九十0-9]+日)?")
ACTORS = ("戈弗雷", "雷蒙", "鮑德溫", "伊夫提哈爾", "博希蒙德", "守軍", "士兵", "工匠", "居民")
ACTIONS = ("走", "抵達", "攻", "守", "搬", "拖", "推", "砍", "造", "開", "射", "登", "渡", "逃", "等待", "祈禱", "決定", "交戰")
EXPOSITION = ("這意味著", "這說明", "不能直接", "這個地層關係很重要", "研究者指出", "可以確定的是")
DIALOGUE = re.compile(r"[「『][^」』]{2,}[」』]")

def extract(text, section=SECTION):
    matches = list(HEAD.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() == section:
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            return text[match.end():end].strip()
    raise ValueError("Section not found: " + section)

def audit(text):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    records = []
    for index, para in enumerate(paragraphs, 1):
        actors = [name for name in ACTORS if name in para]
        actions = [verb for verb in ACTIONS if verb in para]
        dates = DATES.findall(para)
        flags = [phrase for phrase in EXPOSITION if phrase in para]
        if DIALOGUE.search(para):
            flags.append("quoted_text_verify_source")
        if len(para) > 140 and not actions:
            flags.append("long_exposition_without_action")
        records.append({"paragraph": index, "characters": len(para), "actors": actors, "actions": actions, "dates": dates, "flags": flags})
    return {"paragraphs": len(paragraphs), "action_paragraphs": sum(bool(r["actions"]) for r in records), "dated_paragraphs": sum(bool(r["dates"]) for r in records), "flagged": [r for r in records if r["flags"]], "inventory": records}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("extract", "audit", "test"))
    parser.add_argument("file", nargs="?")
    args = parser.parse_args()
    if args.command == "test":
        sample = "# X\n\n## 金門\n\n戈弗雷六月十三日攻城。\n\n## 尾聲\n\n其他內容"
        assert extract(sample) == "戈弗雷六月十三日攻城。"
        result = audit(extract(sample))
        assert result["paragraphs"] == 1
        assert result["inventory"][0]["actors"] == ["戈弗雷"]
        assert result["inventory"][0]["actions"]
        try:
            extract(sample, "不存在")
            raise AssertionError("Missing heading must fail")
        except ValueError:
            pass
        print("PASS: extraction, section boundaries, action inventory, missing-heading guard")
        return
    if not args.file:
        parser.error("file required")
    section = extract(Path(args.file).read_text(encoding="utf-8"))
    if args.command == "extract":
        print(json.dumps({"section": SECTION, "characters": len(section), "text": section}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(audit(section), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
