# P2 04 · 橄欖山 V4.4 原生 SVG 母版修正與實拍驗收
*2026-11-06 · PR #1385 Draft · 04 未上線*

## 從使用者 2048×1152 實拍發現的根本問題

V4.3 雖然 12 張海報、英文字形與 3:4 安全區通過 Chromium，但下方版畫是完整深色陰影由 Potrace 轉成大量實金色；`mask-size: contain` 加上直角的固定容器，使整段地形呈現孤立、邊界截然的金色矩形。這是母版構圖及向量色階處理錯誤，不是調光效就能修復，也不能稱為獲獎級完成。

## V4.4 實際改動

- `scripts/build-olive-mountain-master-v44.py`：保持 Woodward／Cousen 1881–84 公共領域鋼版原作與 SHA1 驗證，改由原始像素局部亮度差分（burin）及真正的原作灰階鄰域邊界抽取原生 SVG 路徑，**不再直接追蹤整片深色陰影**。桌面獨立畫幅、手機獨立取景；不重複拷貝枝葉，不以線稿手繪假冒歷史原版。
- ink-cap：桌面原畫刀痕 9.2%／邊緣 5.2%；手機刀痕 10.4%／邊緣 6.0%；超過 19% 的整體原生 ink coverage 會中止程序。純線稿，無 `<image>`、JPEG data URI、額外 runtime JS 或新的背景配色。
- 原生 SVG：`static/images/p2-realms/v15/04-olive-woodward-cousen-desktop-intaglio-v44.svg` 和 `04-olive-woodward-cousen-mobile-intaglio-v44.svg`。
- `static/experiments/olive-mountain-art-foundation-v44.html`：移除直角上下邊框與矩形印版容器視覺；**僅透過 CSS 透明度遮罩**將刻線自然淡出到 OS 橄欖綠，仍由 OS 晨光金著色；不是添加另一種綠色或色塊。保護 `OliveSpeakerBaseline.mount` 12 幅 3:4 真實合成海報和原英文字形，03→04 動效及 P2 主站完全不動。
- 對原有中心刊頭 A 和非對稱義大利編輯式刊頭 B 提供真正相同內容、不同排版的比較。

## 驗收

- [Chromium 測試與隔離部署 #42313263045](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/42313263045)：成功。1648／1440／800／390px × A/B 共 8 個靜態實拍驗證，原始海報 3:4、英文字、藝術安全區、來源 SVG、墨量上限、非矩形自然遮罩全通過。
- [V4.4 編輯靜態預覽](https://p2-0104-1385.westsidewatch-github-io.pages.dev/experiments/olive-mountain-art-foundation-v44.html)
- [B · 1648 實拍](https://p2-0104-1385.westsidewatch-github-io.pages.dev/experiments/p2-0104-proofs/1648-olive-v44-static-folio.png)
- [B · 390 實拍](https://p2-0104-1385.westsidewatch-github-io.pages.dev/experiments/p2-0104-proofs/390-olive-v44-static-folio.png)

## 編輯視覺結論與技術邊界

V4.4 明確排除了 V4.3 的「一整塊金色矩形」錯誤，歷史橄欖樹輪廓、城牆、遠景現在可同時成為透明、低層次的版畫底紋；手機有獨立裁切，海報仍是第一層主角。V4.4 經實拍清楚優於 V4.3，但底紋與 P2 真正的單屏 MERSI 五幕過場仍未完成綜合藝術驗收。此版是靜態母本，非「可逆生長動效已接入」或「可合併上線」的憑據。下一階段只能在得到創意驗收後，才考慮接到現有 04 scroll engine。舊 V4.3 原檔不刪，保留失誤證據。

**始終保持 Draft，不合併 main、不替換 01–03、不修改十二張海報。**
