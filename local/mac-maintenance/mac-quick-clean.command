#!/bin/bash
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

banner(){ printf '\n============================================================\n%s\n============================================================\n' "$1"; }
size_kb(){ du -sk "$1" 2>/dev/null | awk '{print $1+0}'; }
fmt_kb(){ awk -v k="${1:-0}" 'BEGIN{if(k>=1048576)printf "%.2f GB",k/1048576;else if(k>=1024)printf "%.1f MB",k/1024;else printf "%d KB",k}'; }
safe_clear_dir(){ local d="$1"; [ -d "$d" ] || return 0; find "$d" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + 2>/dev/null || true; }

banner "Mac Quick Clean — SAFE MODE"
echo "This tool only removes rebuildable user caches/logs/temp files."
echo "Protected: Documents, Desktop, Downloads, Photos, Mail, browser profiles, Keychain, ~/.dore data/memory/archive, Git repositories, Ollama models."

BEFORE_FREE=$(df -k "$HOME" | awk 'NR==2{print $4}')
echo "Disk before: $(df -h "$HOME" | awk 'NR==2{print $4}') free"

banner "Memory / swap before"
memory_pressure 2>/dev/null | tail -5 || true
sysctl vm.swapusage 2>/dev/null || true
if command -v ollama >/dev/null 2>&1; then
  echo; echo "Loaded Ollama models:"; ollama ps 2>/dev/null || true
fi

banner "Cleaning safe user caches"
TARGETS=(
  "$HOME/Library/Caches/com.apple.Safari/WebKitCache"
  "$HOME/Library/Caches/com.apple.helpd"
  "$HOME/Library/Caches/com.apple.iconservices"
  "$HOME/Library/Caches/pip"
  "$HOME/Library/Caches/Homebrew"
  "$HOME/.cache/pip"
  "$HOME/.npm/_cacache"
)
for d in "${TARGETS[@]}"; do
  [ -d "$d" ] || continue
  k=$(size_kb "$d")
  printf '  %-55s %10s\n' "$d" "$(fmt_kb "$k")"
  safe_clear_dir "$d"
done

# Old user logs only; never touch Doré logs here.
find "$HOME/Library/Logs" -type f -mtime +14 -not -path "$HOME/Library/Logs/DiagnosticReports/*" -delete 2>/dev/null || true
find "$HOME/Library/Logs/DiagnosticReports" -type f -mtime +30 -delete 2>/dev/null || true

# User temp directory: only stale files older than 7 days.
TMPROOT=$(getconf DARWIN_USER_TEMP_DIR 2>/dev/null || true)
if [ -n "$TMPROOT" ] && [ -d "$TMPROOT" ]; then
  find "$TMPROOT" -type f -mtime +7 -delete 2>/dev/null || true
  find "$TMPROOT" -depth -type d -empty -mtime +7 -delete 2>/dev/null || true
fi

banner "Doré health — READ ONLY"
if curl -fsS --max-time 3 http://127.0.0.1:8788/health >/tmp/dore-quick-health.$$ 2>/dev/null; then
  cat /tmp/dore-quick-health.$$; echo
else
  echo "Doré Local is not responding on 127.0.0.1:8788 (nothing was changed)."
fi
rm -f /tmp/dore-quick-health.$$

banner "After"
AFTER_FREE=$(df -k "$HOME" | awk 'NR==2{print $4}')
GAIN=$((AFTER_FREE-BEFORE_FREE))
[ "$GAIN" -lt 0 ] && GAIN=0
echo "Disk after : $(df -h "$HOME" | awk 'NR==2{print $4}') free"
echo "Freed      : $(fmt_kb "$GAIN")"
echo
memory_pressure 2>/dev/null | tail -5 || true
sysctl vm.swapusage 2>/dev/null || true

echo
echo "Quick Clean finished. No Doré memory or personal files were deleted."
read -r -p "Press Enter to close..." _
