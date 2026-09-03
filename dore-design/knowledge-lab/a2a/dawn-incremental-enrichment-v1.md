# Dawn Incremental Enrichment 1.0

The second enrichment starts from consumed KnowledgeAsset and source identities. It returns only qualified deltas; changing an asset ID cannot make a consumed source new.

Qualification requires stable identity, URL, authority, source family, rights policy and observed provenance status. Sources remain reference-only unless an individual asset license separately permits reuse.

Acceptance gates:

- baseline working set is 32;
- intersection between consumed IDs and returned IDs is empty;
- at least eight new qualified references;
- provenance and rights fields are complete;
- at least six source families;
- a third identical enrichment returns zero;
- Storybook reaches at least 40 and only then becomes PASS.
