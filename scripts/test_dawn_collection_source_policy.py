#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> int:
    queue_builder = load_module('dawn_queue_builder', ROOT / 'scripts/build_dawn_10k_work_queue.py')
    canonical = load_module('dawn_canonical', ROOT / 'scripts/build_dawn_canonical_substrate.py')

    forbidden_cases = [
        {'provider': 'zh-wikisource', 'sourceUrl': 'https://example.org/book'},
        {'provider': 'Legacy import', 'sourceUrl': 'https://zh.wikisource.org/wiki/Test'},
        {'provider': 'Legacy import', 'evidence': {'url': 'https://en.wikisource.org/wiki/Test'}},
        {'source': 'Wikisource', 'url': 'https://example.org/book'},
    ]
    for case in forbidden_cases:
        assert queue_builder.contains_forbidden_wikisource(case), case
        assert canonical.contains_forbidden_wikisource(case), case

    allowed = {'provider': 'Project Gutenberg', 'sourceUrl': 'https://www.gutenberg.org/ebooks/30'}
    assert not queue_builder.contains_forbidden_wikisource(allowed)
    assert not canonical.contains_forbidden_wikisource(allowed)

    assert queue_builder.language_priority({'languages': ['chi']}) == 0
    assert queue_builder.language_priority({'languages': ['zh-Hant']}) == 0
    assert queue_builder.language_priority({'languages': ['fra']}) == 1
    assert queue_builder.language_priority({'languages': ['eng']}) == 2

    clean_queue = {
        'items': [
            {
                'queueId': 'work::clean-a',
                'workId': 'OL1W',
                'title': 'Clean A',
                'author': 'A',
                'authors': ['A'],
                'languages': ['chi'],
                'authorityIds': {'openLibraryWork': 'OL1W'},
            },
            {
                'queueId': 'work::clean-b',
                'workId': 'OL2W',
                'title': 'Clean B',
                'author': 'B',
                'authors': ['B'],
                'languages': ['eng'],
                'authorityIds': {'openLibraryWork': 'OL2W'},
            },
        ]
    }
    index, _, _ = canonical.build(clean_queue, {'shelves': []}, {'items': []}, [])
    assert index['workCount'] == 2

    poisoned_queue = {
        'items': clean_queue['items'] + [
            {
                'queueId': 'work::poisoned',
                'title': 'Legacy Wikisource Candidate',
                'authors': [],
                'providers': ['zh-wikisource'],
                'pointers': ['https://zh.wikisource.org/wiki/Test'],
                'authorityIds': {},
            }
        ]
    }
    try:
        canonical.build(poisoned_queue, {'shelves': []}, {'items': []}, [])
    except ValueError as exc:
        assert 'Wikisource' in str(exc)
    else:
        raise AssertionError('final canonical admission accepted a Wikisource-tainted queue item')

    poisoned_surface = {
        'shelves': [
            {
                'id': 'legacy',
                'items': [
                    {
                        'title': 'Surface Poison',
                        'provider': 'zh-wikisource',
                        'sourceUrl': 'https://zh.wikisource.org/wiki/Test',
                    }
                ],
            }
        ]
    }
    try:
        canonical.build(clean_queue, poisoned_surface, {'items': []}, [])
    except ValueError as exc:
        assert 'Wikisource' in str(exc)
    else:
        raise AssertionError('final canonical admission accepted a Wikisource-tainted surface item')

    print('PASS: Dawn Wikisource dual gate + Chinese-first ordering + clean workCount invariance')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
