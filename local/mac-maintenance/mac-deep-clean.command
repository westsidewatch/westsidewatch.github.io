#!/bin/bash
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
banner(){ printf '\n============================================================\n%s\n============================================================\n' "$1"; }
fmt(){ awk -v k="${1:-0}" 'BEGIN{if(k>=1048576)printf "%.2f GB",k/1048576;else if(k>=1024)printf "%.1f MB",k/1024;else printf "%d KB",k}'; }

banner "Mac Deep Clean — AUDIT FIRST"
echo "Deep Clean does NOT automatically delete personal files, Doré memory, Git repos, or Ollama models."
echo "It audits large/rebuildable storage and safely clears selected development caches."
BEFORE=$(df -k "$HOME" | awk 'NR==2{print $4}')

banner "Largest folders in your home (report only)"
du -sk "$HOME"/* "$HOME"/.[!.]* 2>/dev/null | sort -nr | head -20 | while read -r k p; do printf '%10s  %s\n' "$(fmt "$k")" "$p"; done

banner "Development caches"
for d in "$HOME/Library/Caches/Homebrew" "$HOME/.npm/_cacache" "$HOME/.cache/pip" "$HOME/Library/Caches/pip"; do
  [ -d "$d" ] || continue
  k=$(du -sk "$d" 2>/dev/null | awk '{print $1+0}')
  printf 'Clearing %-50s %10s\n' "$d" "$(fmt "$k")"
  find "$d" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + 2>/dev/null || true
done

if command -v brew >/dev/null 2>&1; then
  echo "Running Homebrew cleanup..."
  brew cleanup --prune=all 2>/dev/null || true
fi

banner "Ollama audit — REPORT ONLY"
if command -v ollama >/dev/null 2>&1; then
  echo "Installed models:"; ollama list 2>/dev/null || true
  echo; echo "Loaded models:"; ollama ps 2>/dev/null || true
  echo; echo "No model is automatically removed."
else
  echo "Ollama not installed."
fi

banner "Doré protected area — REPORT ONLY"
if [ -d "$HOME/.dore" ]; then
  du -sh "$HOME/.dore" 2>/dev/null || true
  echo "Protected paths include ~/.dore/data, ~/.dore/archive, ~/.dore/imports and memory databases."
fi
curl -fsS --max-time 3 http://127.0.0.1:8788/health 2>/dev/null || echo "Doré Local not responding (nothing changed)."
echo

banner "Large files over 1 GB — REPORT ONLY"
find "$HOME" -type f -size +1G \
  -not -path "$HOME/Library/Photos/*" \
  -not -path "$HOME/Pictures/Photos Library.photoslibrary/*" \
  -not -path "$HOME/.dore/*" \
  -print 2>/dev/null | head -40

echo
banner "Memory / swap"
memory_pressure 2>/dev/null | tail -5 || true
sysctl vm.swapusage 2>/dev/null || true

AFTER=$(df -k "$HOME" | awk 'NR==2{print $4}')
GAIN=$((AFTER-BEFORE)); [ "$GAIN" -lt 0 ] && GAIN=0
banner "Deep Clean finished"
echo "Disk free: $(df -h "$HOME" | awk 'NR==2{print $4}')"
echo "Automatically freed from safe caches: $(fmt "$GAIN")"
echo "Large files and Ollama models above were REPORT ONLY."
read -r -p "Press Enter to close..." _
