#!/usr/bin/env python3
"""Aggregate opt-in G1 R05 anonymous text-test JSON files, entirely offline.

Usage:
    python summarize-g1-r05.py ./responses ./aggregate.csv

The output intentionally contains NO open-ended answers, device IDs, timestamps,
names, e-mails, or religious information. Human raters must separately score
comprehension against the research rubric; no model guesses scores.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import median


def safe_rating(value):
    if type(value) is int and 1 <= value <= 5:
        return value
    return None


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python summarize-g1-r05.py RESPONSES_DIRECTORY OUTPUT.csv")
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    if not source.is_dir():
        raise SystemExit("Responses directory not found.")
    files = sorted(source.glob("*.json"))
    groups = defaultdict(list)
    accepted = 0
    rejected = 0
    for path in files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if data.get("schema") != "gospel-youtube-g1-r05-1":
                raise ValueError("Unsupported schema")
            responses = data.get("responses")
            if not isinstance(responses, list) or len(responses) != 2:
                raise ValueError("Expect exactly 2 topic responses")
            seen = set()
            normalized = []
            for entry in responses:
                topic, variant = entry.get("topic"), entry.get("version")
                if topic not in ("T1", "T2") or variant not in ("A", "B") or topic in seen:
                    raise ValueError("Unknown topic/version or duplicate")
                seen.add(topic)
                normalized.append((topic, variant, entry))
            for topic, variant, entry in normalized:
                groups[(topic, variant)].append(entry)
            accepted += 1
        except (OSError, ValueError, TypeError, AttributeError, json.JSONDecodeError):
            rejected += 1
            continue
    headers = [
        "topic", "version", "n", "clarity_median", "jargon_difficulty_median",
        "respect_median", "next_step_median", "n_with_written_answers"
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for topic in ("T1", "T2"):
            for variant in ("A", "B"):
                items = groups.get((topic, variant), [])
                def med(field):
                    values = [safe_rating(item.get(field)) for item in items]
                    values = [v for v in values if v is not None]
                    return median(values) if values else ""
                written = sum(
                    any(str(a).strip() for a in item.get("answers", [])
                        if isinstance(a, str))
                    for item in items
                )
                writer.writerow([
                    topic, variant, len(items), med("clarity"),
                    med("jargon_difficulty"), med("respect"), med("next_step"), written
                ])
    print("Accepted anonymous files:", accepted)
    print("Skipped invalid / unsupported files:", rejected)
    print("Aggregate created:", str(output))
    print("Do not interpret medians as representative population estimates.")
    print("Written comprehension answers are not auto-scored and are not exported.")


if __name__ == "__main__":
    main()
