# Doré Local Node — Mac mini

Target: Apple Silicon Mac mini (M4, 16 GB unified memory).

## Architecture

Doré Local is a local runtime node of the same Doré identity, not a second Doré.

- `data/dore.sqlite3` — local canonical working database
- `archive/` — local immutable/raw memory archive
- Ollama — replaceable local inference + embedding provider
- `server.py` — local-only Doré API bound to 127.0.0.1
- Cloudflare remains the public edge; Workers AI is not required by Doré Local Memory Core.

## First model profile

- Conversation/reasoning: `qwen3:8b`
- Embedding: `qwen3-embedding:0.6b`

The model layer is replaceable. Memory IDs, provenance and Doré identity are independent of the model.

## Security boundary

The local API binds to `127.0.0.1` only by default. Do not expose port 8788 or Ollama port 11434 directly to the public internet.

## Bootstrap

Run `bash local/dore-local/bootstrap-macos.sh` from the repository root. The script checks Apple Silicon/macOS, verifies Python and Ollama, creates the local directories/database, and pulls the selected local models.
