from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


LIBRARY_UI_SCHEMA = "dawn-library-view-model/v1"


@dataclass(frozen=True)
class LibrarySelection:
    work_id: str
    mode: str = "bilingual"


def build_library_shell(index: Mapping, recommendations: Mapping | None = None) -> dict:
    """Stable semantic contract between Doré core and any Dawn Library visual UI.

    Layout, animation and editorial styling may be replaced without changing the
    corpus, translation or remote-holdings layers.
    """
    recommendations = recommendations or {}
    return {
        "schema": LIBRARY_UI_SCHEMA,
        "identity": {
            "name": "黎明書局",
            "purpose": "read-and-read-in-Chinese",
        },
        "leftPage": {
            "role": "discovery-index",
            "primaryEntries": [
                {"id": "morning-stars", "label": "三晨星", "kind": "recommendation-standard"},
                {"id": "catalogue", "label": "館藏", "kind": "catalogue"},
                {"id": "search", "label": "搜尋", "kind": "search"},
            ],
            "catalogue": {
                "count": index.get("count", 0),
                "pageSize": index.get("pageSize", 250),
                "pageCount": index.get("pageCount", 0),
                "pages": index.get("pages", []),
                "facets": index.get("facets", {}),
                "load": "on-demand",
            },
            "recommendations": {
                "morningStars": recommendations.get("morningStars", []),
            },
        },
        "rightPage": {
            "role": "reader",
            "emptyState": "select-work",
            "modes": [
                {"id": "source", "label": "原文"},
                {"id": "zh-Hant", "label": "繁中"},
                {"id": "bilingual", "label": "對照"},
            ],
            "defaultMode": "bilingual",
            "contentFetch": "on-demand",
            "translation": "dore-language-faculty",
        },
        "invariants": {
            "threeMorningStarsBelongsToLibrary": True,
            "threeMorningStarsIsNotSpectrum": True,
            "threeMorningStarsIsNotCuratedCollection": True,
            "spectrumAndCuratedCollectionAreSiteLevelEditorialSurfaces": True,
            "uiMayBeReplacedWithoutCorpusMigration": True,
            "fullTextStoredLocally": False,
            "initialFullCatalogueLoad": False,
        },
    }


def select_work(shell: Mapping, work: Mapping, mode: str = "bilingual") -> dict:
    allowed = {item["id"] for item in shell["rightPage"]["modes"]}
    if mode not in allowed:
        raise ValueError(f"unsupported reading mode: {mode}")
    return {
        "schema": "dawn-library-reader-selection/v1",
        "work": {
            "id": work.get("id"),
            "title": work.get("title"),
            "creator": work.get("creator"),
            "date": work.get("date"),
            "cover": work.get("cover"),
        },
        "mode": mode,
        "sourceResolution": "remote-pointer",
        "contentFetch": "on-demand",
        "translation": "dore-language-faculty" if mode != "source" else None,
    }
