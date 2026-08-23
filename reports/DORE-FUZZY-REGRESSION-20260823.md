# Doré fuzzy search regression — 2026-08-23

Required browser-search behavior:

- `耶和華` returns candidate verses containing the phrase.
- `我終日等候你` returns Psalm 25:5.
- `耶和華啊，我終日等候你` must also return Psalm 25:5 even though the remembered query combines an unmatched prefix with a strong matching suffix.

This regression guards multi-fragment remembered Scripture queries. The browser scorer must not reject a verse merely because one remembered fragment is absent when another long, distinctive fragment matches strongly.
