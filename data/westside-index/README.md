# Westside Core Derived Indexes

`Westside Core` is neutral site infrastructure. It is not Dawn Bookshop / 黎明書局 and does not belong to any publication surface.

Canonical shared resources live under `/data/westside-core/`. Disposable generated views live under `/data/westside-index/`.

Consumers use `/js/westside-resource-query.js` (`window.WestsideResources`) and request only scoped indexes, editorial selections or individual resources.

Legacy `/data/dawn-*` and `/js/dawn-resource-query.js` paths are migration-only and must not be used by new integrations. They may be removed after existing references are verified and migrated.
