#!/bin/bash
set -e
cd "$(dirname "$0")"
case "$(uname -m)" in
  x86_64) arch=amd64 ;;
  arm64) arch=arm64 ;;
  *) echo "Unsupported Mac architecture"; exit 1 ;;
esac
if [ ! -x "runtime/dore-offline-$arch" ]; then
  echo "Missing runtime. Export again on the preparation Mac."
  exit 1
fi
exec "runtime/dore-offline-$arch" -home "$PWD/portable-data"
