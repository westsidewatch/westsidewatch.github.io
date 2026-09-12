# Doré Folio / 多寫 — Content Boundary

Status: LOCKED

## Immediate presentation rule

Until the underlying corpus/index purge is complete, excluded resources MUST NOT be visible anywhere on Doré Folio / 多寫 pages.

Fail closed: if a resource cannot be confidently admitted, do not render it.

### Block before render
Suppress any card, search result, recommendation, preview, related-content item, cached item, or source item whose primary subject is:
- modern politics or political parties
- nationalism
- modern ethnic/national conflict
- modern warfare or military advocacy
- geopolitical position-taking
- political propaganda or ideological confrontation

Known regression fixtures that must never render:
- 《巴勒斯坦、阿拉伯人民反击以色列侵略》
- 《巴勒斯坦游击队不断袭击以色列侵略军》

This temporary/defensive render gate remains mandatory even after purge until ingestion and index admission gates are verified.

## Permanent admitted scope
Doré Folio / 黎明書局 brand surfaces are limited to resources serving Scripture and biblical understanding, Christian theology, church history, spiritual/devotional tradition, and inner-life formation in Christ.

## Required architecture
1. ingestion admission gate
2. persistence/index admission gate
3. recommendation/render admission gate
4. purge existing excluded records/assets/cache
5. rebuild index and invalidate caches
6. regression tests proving the fixtures above produce zero visible results

This is a brand-scope boundary, not a judgment on the scholarly value or truth/falsity of excluded materials.
