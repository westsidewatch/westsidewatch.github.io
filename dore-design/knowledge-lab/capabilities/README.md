# Doré Capability Discovery

This is an enhancement layer for Doré's existing Search and AI Conversation, not a replacement product.

## Boundary

- Existing `/dore/dore-search.js` remains the native Bible/search execution owner.
- Existing Doré AI Conversation remains untouched.
- Registry metadata describes capabilities objectively; it does not copy implementation.
- Planned capabilities are deferred and cannot be selected as executable until promoted after evidence.
- Providers must remain free/local-first under the current project policy.

## First acceptance

The first experiment deliberately registers only capabilities Doré already owns as executable. CI proves the existing Search functions remain present and that the registry points back to the native implementation.

Only after this passes should `library.books` receive its first executable adapter. That adapter is the bridge into Dawn Library work.
