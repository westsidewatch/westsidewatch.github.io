#!/bin/bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$REPO/local/mac-maintenance"
DESKTOP="$HOME/Desktop"
mkdir -p "$DESKTOP"
install -m 755 "$SRC/mac-quick-clean.command" "$DESKTOP/Mac Quick Clean.command"
install -m 755 "$SRC/mac-deep-clean.command" "$DESKTOP/Mac Deep Clean.command"
xattr -d com.apple.quarantine "$DESKTOP/Mac Quick Clean.command" 2>/dev/null || true
xattr -d com.apple.quarantine "$DESKTOP/Mac Deep Clean.command" 2>/dev/null || true
printf 'INSTALLED:\n  %s\n  %s\n' "$DESKTOP/Mac Quick Clean.command" "$DESKTOP/Mac Deep Clean.command"
echo 'MAC_MAINTENANCE_DESKTOP_INSTALL_PASS'
