#!/usr/bin/env bash
# Complete upstream EGM source + official Codex activation for Westside Design OS.
# No silent installation, API call, or model execution unless explicitly asked.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
UPSTREAM=".tools/elephant-goldfish-model"
usage() {
  cat <<'USAGE'
Usage: bash scripts/egm-setup.sh --prepare|--check|--install-codex
  --prepare       Initialize the complete pinned EGM Git submodule.
  --check         Offline check of pinned source contents; no installation.
  --install-codex Prepare source, then run the official Codex plugin commands.
                  This affects only the machine that runs the command.
USAGE
}
check_source() {
  local pinned actual
  if ! git ls-tree HEAD -- "$UPSTREAM" | grep -q '^160000 commit '; then
    echo "ERROR: pinned EGM gitlink is missing in repository HEAD" >&2
    return 1
  fi
  pinned="$(git ls-tree HEAD -- "$UPSTREAM" | awk '{print $3}')"
  if [[ ! -d "$UPSTREAM/.git" && ! -f "$UPSTREAM/.git" ]]; then
    echo "NOT INITIALIZED: run bash scripts/egm-setup.sh --prepare" >&2
    return 1
  fi
  actual="$(git -C "$UPSTREAM" rev-parse HEAD)"
  if [[ "$actual" != "$pinned" ]]; then
    echo "ERROR: EGM checkout does not match parent repository pin" >&2
    return 1
  fi
  for part in plugin.json LICENSE skills/egm_review/SKILL.md agents/design_critic.md resources/document_standards/feature-spec-standard.md; do
    if [[ ! -f "$UPSTREAM/$part" ]]; then
      echo "ERROR: EGM component missing: $part" >&2
      return 1
    fi
  done
  echo "EGM SOURCE VERIFIED: $actual (complete plugin; not proof of activation)"
}
case "${1:---help}" in
  --prepare)
    git submodule update --init -- "$UPSTREAM"
    check_source
    ;;
  --check)
    check_source
    ;;
  --install-codex)
    if ! command -v codex >/dev/null 2>&1; then
      echo "ERROR: Codex CLI is not installed on this machine." >&2
      exit 1
    fi
    git submodule update --init -- "$UPSTREAM"
    check_source
    echo "Installing upstream EGM plugin into THIS local Codex environment..."
    codex plugin marketplace add google/elephant-goldfish-model
    codex plugin add egm@egm
    echo "Codex activation requested. Restart Codex; marketplace plugin version may differ from pinned source."
    ;;
  -h|--help) usage;;
  *) usage >&2; exit 2;;
esac
