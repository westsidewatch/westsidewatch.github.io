# Doré Motion — Engineering Memo / 多雷動態版畫工程備忘錄

Status: LONG-TERM CORE R&D ASSET · PLANNED / INCREMENTAL DELIVERY
Recorded: 2026-10-15
Repository: westsidewatch/westsidewatch.github.io
Working branch: design/church-editorial-layout-preview-20261014

## 定位
Doré Motion 是本站長期累積的動態版畫視覺生產引擎，不是單一網頁特效，也不是現階段電影製作工程。每一階段均須產生可獨立驗收、可部署、可重用的成果。全站共用既有 Design OS 管理，不另設字體、色彩或 CSS 權威系統；版塊可獨立配置。

## 工程優先順序

### 01 — Living Water Flow（第一個可上線目標）
將已驗收的 v2 呼吸式水面加入連續方向性流動，保留原有呼吸、構圖與刻線。獨立 Flow Lab 試作；確認無白邊、斷線、硬接縫、布料式扭曲，完成響應式、效能、reduced-motion 與人工視覺驗收後再部署。
保護：
- static/experiments/sevenfold-first-to-second.html
- baseline c489901abec92e62f9c4ab33963d8bb5ce01a566
- static/experiments/assets/living-water-contour-engraving-v10.svg
未驗收前不得覆蓋原版。

### 02 — Engraving Ocean 3D
保留原 Continuous Field Lab 意外形成的立體波濤作參照；分別量測局部刻線交角、曲率、重疊範圍、相位、密度與遮擋。對照 Seamless Sea 與 Overlap Surface 的失敗案例。先做獨立角度實驗，再視需要借鑑 Gerstner/FFT 成熟海浪模型。此階段不得阻礙第一階段上線。

### 03 — Doré Motion Engraving System（目前第三項正式工程）
這是全站長期研發資產，包含三條互通產線：
A. 七個版塊可獨立設定的動態刻線底紋；
B. 多雷聖經原作的靜態動效化，優先服務 ONE 和以馬忤斯；
C. 《西望》雜誌插圖、封面與裝飾，以及可旋轉、可打光、可輸出的 3D 版畫小物件。
首批驗證：一張聖經插圖、一款刻線底紋、一件 3D 版畫小物件；驗收後逐步部署與批量化。

## 多雷原作動態化資產庫
長期目標為 200+ 張原作的可重用動態資產庫；數量是規劃目標，不代表已核實或已完成。先盤點現有素材及授權，再以風景／人物／建築三類試作。每張原作保留不可變版本；使用場景 ID、經文、來源／權利、景深層、遮罩、光源、鏡頭、安全區、動效預設、效能、reduced-motion、版本和驗收狀態的標準化紀錄。避免每張獨立手寫一套動畫。保留可供未來電影使用的場景、鏡頭與遮罩資料，但不宣稱二維分層等於完整三維建模。

## 雜誌與 3D 物件
可重用的刻線材質／方向場／光影與相機參數，生產橄欖枝、油燈、書卷、錢幣、陶罐、石柱、鑰匙、號角等視覺物件。根據實際渲染能力輸出網頁動畫、影像或向量，不虛稱所有輸出均為 SVG。納入 Design OS 的版式、色彩、字體和安全區約束。

## 04 — Doré Cinematic Engine（長期預備，暫不啟動）
《十字架的影子》及聖經故事影像可承接以上場景資料、分層、鏡頭和風格資產，但人物表演、逐鏡連續性、完整三維重建及電影成本仍屬未解決難題。不得以電影的未知需求阻礙網站的可交付成果；不修改現有電影工程或創作手冊。

## 開源研究及限制
- ai-sci-computing/hatching：曲率方向場、三維表面刻線、WebGL2/WASM；可旋轉靜態模型，但不是現成角色動畫。README 限個人／學術／研究使用，商用須書面許可，不可當 MIT 代碼直接納入正式產品。
- jbouny/fft-ocean、Skittss/FFTOcean、squall01337/abyssal-ocean、reed-soul/SeedOcean：海浪幾何候選，採用前逐項核實實作與授權。
- CreativeInquiry/ApparentRidges、mightyhorst/threejs-hand-sketching、philogb/LIC：三維輪廓、刻線與流場候選，尚待技術與授權驗證。

## 工程治理
- 單一共用能力，按版塊獨立調參；不增設平行設計系統。
- 保留所有通過驗收的原版；實驗只進獨立 Lab。
- 原始圖像、3D 模型及來源／授權紀錄不可破壞。
- 版本化動效預設、參數、視覺基準與失敗案例。
- 每次交付要有可觀察成果、測試和明確驗收，不以 commit 代替視覺完成。
- 優先考慮流暢度、手機適配、降低動態效果及無障礙。
- 本備忘錄是工程索引與方向紀錄，不表示上述功能已完成或部署。

## 專題研究檔
- docs/dore/motion/LIVING-WATER-FLOW-ROADMAP-2026-10-15.md
- docs/dore/motion/ENGRAVING-OCEAN-3D-RESEARCH-2026-10-15.md
- docs/dore/graphics/3D-SURFACE-HATCHING-RESEARCH-2026-10-15.md
- docs/dore/motion/DORE-BIBLE-ILLUSTRATION-MOTION-PROGRAM-2026-10-15.md
- docs/dore/motion/DORE-EDITORIAL-ENGRAVING-ASSET-ENGINE-2026-10-15.md
- docs/dore/film/MOTION-RESEARCH-FUTURE-DEPENDENCIES-2026-10-15.md
