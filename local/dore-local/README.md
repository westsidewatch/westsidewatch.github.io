# Doré Local Node — Mac mini

Target: Apple Silicon Mac mini (M4, 16 GB unified memory).

## Architecture

Doré Local is a local runtime node of the same Doré identity, not a second Doré.

- `data/dore.sqlite3` — local canonical working database
- `archive/` — local immutable/raw memory archive
- `archive/design-evidence/` — immutable design evidence archive
- Ollama — replaceable local inference + embedding provider
- `dore_local.py` — local-only Doré API bound to 127.0.0.1
- `design_memory.py` — deterministic scope, truth-state and consolidation primitives
- Cloudflare remains the public edge; Workers AI is not required by Doré Local Memory Core.

## Current model profile

- Conversation/reasoning source: `DORE_LOCAL_MODEL` (bootstrap default: `gemma4:e4b`)
- Embedding source: optional `DORE_LOCAL_EMBED_MODEL`; no embedding model is auto-selected or provisioned when this is unset

Historical model names previously documented here are retired provenance, not current configuration authority. The model layer remains replaceable; memory IDs, provenance and Doré identity are independent of the selected model.

## Design Working Memory

Current integration: `d1-d3-integrated-v1`.

`/chat` now preserves conversation-level project/scope/design context. Once a conversation enters a confirmed Westside design context, later related technical/design turns inherit that scope rather than needing to re-prove brand membership.

Design-mode user turns are stored both as ordinary Doré messages and immutable design evidence. The design view separates current decisions/final/verified knowledge from exploration, references/evidence and rejected/corrected history before it is supplied to the local model.

Explicit evidence can be written through `POST /design/evidence` with `content`, `truth_state`, `project_id`, optional `conversation_id`, `scope`, `source_ref`, and `supersedes`. Supported truth states are defined in `design_memory.py`.

The consolidated current view can be read through `POST /design/view` with `project_id`.

This is a working-memory layer, not Penpot capability certification. D4 visual readback and Search-to-Penpot execution remain required before Doré can be marked Penpot design capable.

## Security boundary

The local API binds to `127.0.0.1` only by default. Do not expose port 8788 or Ollama port 11434 directly to the public internet.

## Bootstrap

Run `bash local/dore-local/bootstrap-macos.sh` from the repository root. The script checks Apple Silicon/macOS, verifies Python and Ollama, creates the local directories/database, creates the Design Working Memory tables, and pulls the selected local reasoning model. It provisions an embedding model only when `DORE_LOCAL_EMBED_MODEL` is explicitly supplied.

For an already-bootstrapped machine, `dore_local.py` also creates the new Design Working Memory tables at startup, so a destructive database rebuild is not required.

## Acceptance

Run from `local/dore-local`:

```bash
python3 test_design_memory.py
```

Expected deterministic core result:

```text
DORE_DESIGN_MEMORY_D1_D2_D3_CORE_PASS
```
