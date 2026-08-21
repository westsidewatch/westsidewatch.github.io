#!/usr/bin/env bash
set -euo pipefail

WORKER_URL="${ONE_STUDIO_UPLOAD_URL:-https://one-studio-upload.westsidewatchca.workers.dev}"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 /path/to/image.png [target-name.png]" >&2
  exit 64
fi

SOURCE="$1"
TARGET_NAME="${2:-$(basename "$SOURCE")}"

if [[ ! -f "$SOURCE" ]]; then
  echo "File not found: $SOURCE" >&2
  exit 66
fi

if [[ -z "${UPLOAD_SECRET:-}" ]]; then
  echo "UPLOAD_SECRET is not set." >&2
  echo "Run: read -s UPLOAD_SECRET; export UPLOAD_SECRET" >&2
  exit 78
fi

case "$TARGET_NAME" in
  *.png|*.PNG|*.jpg|*.JPG|*.jpeg|*.JPEG|*.webp|*.WEBP) ;;
  *)
    echo "Target must end in .png, .jpg, .jpeg or .webp" >&2
    exit 65
    ;;
esac

RESPONSE="$(curl --fail-with-body --silent --show-error \
  -X POST \
  -H "Authorization: Bearer $UPLOAD_SECRET" \
  -F "file=@$SOURCE" \
  -F "filename=$TARGET_NAME" \
  -F "message=Add ONE Studio image: $TARGET_NAME" \
  "$WORKER_URL")"

printf '%s\n' "$RESPONSE"

python3 - "$RESPONSE" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
if payload.get("ok") is not True or payload.get("verified") is not True or not payload.get("commit"):
    raise SystemExit("Upload was not verified by GitHub")
print(f"Verified: {payload['path']}")
print(f"Commit: {payload['commit']}")
PY
