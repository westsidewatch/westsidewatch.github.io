# Doré Capability Discovery v0.1

This is an enhancement layer around Doré's existing Search and AI Conversation, not a replacement product.

- Existing `/dore/dore-search.js` remains the native Bible Search execution owner.
- Existing Doré AI Conversation remains untouched.
- Registry metadata describes capabilities; it does not copy implementations.
- Planned capabilities are deferred and cannot execute until promoted after evidence.
- Providers must remain free/local-first and preserve provenance.

Method record: inspect existing capability -> research mature patterns -> reject conflicting architecture -> define minimal hypothesis -> isolate -> accept -> promote.

Next gate: CI plus Doré canonical local PASS. Only then implement the first executable `library.books` adapter for Dawn Library.
