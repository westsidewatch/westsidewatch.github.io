# Dawn Derived Index Layer

This directory is generated/read-oriented infrastructure between the canonical Dawn Resource Registry and site surfaces.

## Rule

A consumer must request a scoped index, editorial selection or single resource. It must not fetch the complete Dawn resource corpus during ordinary page rendering.

Canonical resources remain under `data/dawn-resource-corpus/`. Files under `data/dawn-index/` are disposable derived views and may be rebuilt from canonical resources and relations.

Initial index families:

- `by-type`
- `by-speaker`
- `by-series`
- `by-scripture`
- `by-theme`
- `by-place`
- `by-ministry`
- `by-language`

The same resource ID may appear in multiple indexes without duplicating the canonical resource record.

Surface names are presentation/consumer identities. `LivingWaterWest` is the canonical visible surface name; legacy filesystem/URL paths may remain unchanged during migration.
