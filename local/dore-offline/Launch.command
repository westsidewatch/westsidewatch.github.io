#!/bin/bash
set -u
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "需要 Python 3.8 或以上。"; read -r -p "按 Enter 離開"; exit 1
fi
args=()
if [ -d portable-data ]; then args=(--home "$PWD/portable-data"); fi
while true; do
  printf '\nDoré Offline · Westside Watch\n\n1  離線展示\n2  下載／更新主站\n3  完整性檢查\n4  版本管理\n5  外部資源檢查\n6  匯出便攜展示目錄\n0  離開\n\n'
  read -r -p '選擇：' choice || exit 0
  case "$choice" in
    1) python3 offline.py "${args[@]}" serve ;;
    2) read -r -p 'Git 版本（Enter = main）：' ref
       if [ -z "$ref" ]; then ref=main; fi
       python3 offline.py "${args[@]}" update "$ref" ;;
    3) python3 offline.py "${args[@]}" verify ;;
    4) python3 offline.py "${args[@]}" versions
       read -r -p '輸入完整 SHA 切換，Enter 返回：' sha
       if [ -n "$sha" ]; then python3 offline.py "${args[@]}" select "$sha"; fi ;;
    5) python3 offline.py "${args[@]}" audit ;;
    6) read -r -p '輸入新的目標目錄完整路徑：' dest
       if [ -n "$dest" ]; then python3 offline.py "${args[@]}" export "$dest"; fi ;;
    0) exit 0 ;;
    *) echo "請選擇 0–6。" ;;
  esac
done
