# Dawn URL Surface Contract

## Principle

Dawn Library is a small index over resources that remain on the public web. A pointer is not copied into Dawn merely to be previewed. Presentation capabilities are detachable adapters selected by a small resolver.

## Boundary

`Discovery / judgment -> Pointer -> URL Resolver -> Surface adapter`

Preview is presentation, not relevance. A successful preview MUST NOT promote a candidate, change its relevance status, delete it, or convert an external resource into Dawn-owned content.

## Initial adapter classes

- `iiif-visual-surface`: existing IIIF / VisualSurface path.
- `pdfjs`: direct PDF documents.
- `book-reader`: direct EPUB/MOBI pointers when a reader is available.
- `bibliographic-page`: known book pages such as Project Gutenberg; metadata/identity first, reading endpoint resolved separately.
- `zotero-translate`: bibliographic/catalog pages that benefit from structured interpretation.
- `oembed-opengraph`: lightweight general-web preview; Readability is a fallback for readable HTML rather than a mandatory dependency.

These names describe capability contracts. Mature third-party implementations remain replaceable behind adapters; Dawn Core must not depend on a provider-specific response shape.

## Real-corpus acceptance gate

The existing discovery queue is the benchmark, not a synthetic fixture. At the time this contract was introduced, `reports/DAWN-LIBRARY-DISCOVERY.json` reports 939 queued candidates.

The benchmark must:

1. evaluate at least 900 real candidate pointers;
2. route at least 95% to a presentation capability or explicitly report why a pointer is unresolved;
3. preserve every candidate and external pointer;
4. perform no admission/promotion/deletion;
5. keep preview capability independent from relevance qualification;
6. emit per-pointer routes so later live-adapter work can be measured against the same corpus.

The first engineering milestone is routing coverage. The next milestone is live adapter success: a routed pointer must actually return a renderable Surface payload, with failures falling back without affecting the index.
