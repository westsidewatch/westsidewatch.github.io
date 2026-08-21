#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: scripts/dore-publish.sh <image-path> [target-filename]" >&2
  exit 2
fi

src="$1"
if [ ! -f "$src" ]; then
  echo "File not found: $src" >&2
  exit 1
fi

case "${src##*.}" in
  png|PNG|jpg|JPG|jpeg|JPEG|webp|WEBP|avif|AVIF) ;;
  *) echo "Unsupported image type: $src" >&2; exit 1 ;;
esac

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

dest_dir="static/one/studio"
mkdir -p "$dest_dir"

default_name="$(basename "$src")"
target_name="${2:-$default_name}"

case "$target_name" in
  */*) echo "Target filename must not contain '/': $target_name" >&2; exit 1 ;;
esac

dest="$dest_dir/$target_name"
cp "$src" "$dest"

git add -- "$dest"
if git diff --cached --quiet -- "$dest"; then
  echo "No change: $dest"
  exit 0
fi

git commit -m "Add Doré artwork: $target_name"
git push

echo "Published: $dest"
