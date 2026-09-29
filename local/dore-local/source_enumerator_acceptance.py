#!/usr/bin/env python3
from source_enumerator import enumerate_collection, SCHEMA


def main() -> None:
    api = enumerate_collection({
        "sourceUrl": "https://catalog.example/collection",
        "records": [
            {"id": "1", "url": "/item/1", "title": "甲"},
            {"id": "2", "url": "/item/2", "title": "乙"},
            {"id": "2", "url": "/item/2", "title": "乙 duplicate"},
        ],
        "next": "/collection?page=2",
    })
    assert api["schema"] == SCHEMA and api["count"] == 2
    assert api["continuation"]["evidence"] == "pagination"
    assert api["authority"] is False and api["storesSourceMedia"] is False

    html = enumerate_collection({
        "sourceUrl": "https://archive.example/index",
        "html": '<a href="/work/a">A</a><a href="/work/b">B</a><a href="/work/a">A again</a>',
    })
    assert html["count"] == 2
    assert {x["sourceUrl"] for x in html["items"]} == {"https://archive.example/work/a", "https://archive.example/work/b"}

    manifest = enumerate_collection({
        "sourceUrl": "https://images.example/manifest",
        "manifest": {"items": [{"id": "/image/1", "label": "一"}, {"id": "/image/2", "label": "二"}]},
    })
    assert manifest["count"] == 2
    assert all(x["evidence"] == "manifest" for x in manifest["items"])

    missing = enumerate_collection({})
    assert missing["ok"] is False and missing["reason"] == "source-url-required"
    print("DORE_SOURCE_ENUMERATOR_V1_ACCEPTANCE=PASS")
    print("DORE_SOURCE_ENUMERATOR_API_COUNT=2")
    print("DORE_SOURCE_ENUMERATOR_HTML_COUNT=2")
    print("DORE_SOURCE_ENUMERATOR_MANIFEST_COUNT=2")


if __name__ == "__main__":
    main()
