# Doré Witness Access Architecture

Status: REQUIRED

Doré's research mandate is broad: important Bible versions should be known, compared, evaluated, and made reachable where lawful. That mandate does not imply that every copyrighted full text may be copied into GitHub.

## Four access tiers

### Tier 1 — Local Corpus
For public-domain, permissively licensed, owned, or explicitly authorized text.

Doré may retain a pinned snapshot, ingest the complete witness, index it, align it, benchmark it, and perform corpus-wide statistics subject to the license.

### Tier 2 — Licensed / Official API
For a copyrighted witness available through an authorized API or licensed data service.

Doré retrieves only through the authorized interface and obeys query, quotation, caching, and redistribution terms. Full-text persistence is not assumed.

### Tier 3 — External Reader / MCP
For a legitimate external Bible reader or research service whose terms permit automated navigation or retrieval but not local corpus replication.

Doré stores the witness dossier, canonical-reference routing rules, source identity, and access policy. At research time it may route a canonical reference to the external source, obtain only what is permitted for the current task, align the permitted result with other witnesses, and retain provenance rather than an unauthorized mirror.

This is the ONE principle generalized into Doré: Doré does not need to own every library collection; it must know where a collection is, whether it may enter, how to request the right passage, and how to integrate lawful evidence.

### Tier 4 — Human Only / Metadata Research
For sources that do not permit automated access or for which permission is uncertain.

Doré may retain sourced bibliographic/version knowledge and lawful scholarly discussion, but it must not scrape or automate the reader. It may provide a human navigation route when appropriate.

## Required access metadata

Every important witness must eventually declare:

- witness_id
- official/version name
- access tier
- source/provider
- official or authoritative source URL when available
- copyright/license status
- terms URL when applicable
- whether automated access is permitted
- whether full-text storage is permitted
- whether persistent caching is permitted
- quotation restrictions/notes
- canonical-reference routing capability
- provenance requirements

Unknown permission defaults to restrictive behavior, not assumed permission.

## Chinese coverage policy

The Chinese research catalogue is intentionally broader than the first ingestion set. It includes major current and historical witnesses such as:

- 和合本 / Chinese Union Version
- 新標點和合本
- 和合本修訂版
- 呂振中譯本
- 恢復本
- 新譯本
- 現代中文譯本
- 新漢語譯本
- important historical Chinese translations and additional major versions found during survey

Each version is assigned the highest lawful access tier actually supported by evidence. A version does not disappear from Doré's curriculum merely because Tier 1 ingestion is unavailable.

## English coverage policy

The same rule applies to KJV, ASV, WEB/WEBU, RSV, NRSV/NRSVue, NASB, ESV, NIV, NLT, NET, CSB and other important English witnesses. Public-domain/permissive versions may become local corpora; copyrighted versions use licensed/API/external-reader access where authorized.

## Research behavior

When asked to compare a passage, Doré should:

1. resolve the canonical reference;
2. identify relevant original-language and translation witnesses;
3. inspect each witness's access policy;
4. use local corpora where authorized;
5. invoke licensed/API or external-reader sources where authorized;
6. never bypass a human-only restriction;
7. align the lawfully obtained evidence;
8. classify differences;
9. evaluate against original-language/text-critical evidence;
10. cite provenance and distinguish textual evidence, publisher claims, scholarly assessment, and Doré's analysis.

## Architectural consequence

`WitnessAccessPolicy` is part of the Language Core. Connectors/MCP tools are transport mechanisms beneath this policy layer. A connector existing is not itself permission to ingest, cache, or redistribute a witness.
