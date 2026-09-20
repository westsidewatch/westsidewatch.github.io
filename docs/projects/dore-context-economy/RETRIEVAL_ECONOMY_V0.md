# Retrieval Economy v0

Status: implemented

Codex must not begin a UI task with an unbounded repository walk. The surface/target is resolved first; only explicit candidate files enter local retrieval.

v0 is deliberately dependency-free and free:
- lexical query terms;
- Python AST symbols;
- cheap JS/TS symbol hints;
- bounded excerpts;
- ranked results;
- no implicit whole-repository scan.

This is the first executable retrieval gate, not the final search engine. Mature open-source semantic retrieval may be attached behind this interface after benchmark evidence shows it improves savings or recall. It does not receive authority.

Expansion rule: if the bounded result is insufficient, request the next explicit candidate set and record the expansion in benchmark metrics. Whole-repository search is the last fallback, never the default.

Quality rule: retrieval economy may reduce context, never visual authority, correctness, or required verification.
