# P2 04 / 橄欖山 V4.3｜歷史鋼版畫 SVG 藝術母版

*2026-11-06 · PR #1385 · Draft isolated artmaster, not a publication or motion approval*

## 解決的核心錯誤

V1–V3.2 將一張橄欖枝原稿程序化複製到全頁，數量很多、但大多被十二張講員海報遮住；V4/V4.1 縮到兩側導致碎枝；V4.2 重畫的遠城是概念化建築輪廓，不能呈現真正的橄欖山。本版**禁止再用重複公式生成植物**：以完整、可查來源的 1881–1884 年原始鋼版畫直接向量化，從源頭帶入真正的橄欖樹、谷地、梯田、城市、石牆和遠景。

## 主體、來源、授權

- **John Douglas Woodward（1846–1924）／Charles Cousen（1819–1889）**，*Jerusalem from the Mount of Olives*，1881–1884，*Picturesque Palestine, Sinai and Egypt*。此畫有真實的橄欖山景觀：前景古橄欖樹與農人、谷地、牆和耶路撒冷城。
- [NYPL 原作權威登錄（Image ID 80257）](https://old-digitalcollections.nypl.org/items/510d47d9-5d9b-a3d9-e040-e00a18064a99)；[Wikimedia Commons 原始 3928×2703 掃描與公版登錄](https://commons.wikimedia.org/wiki/File:Jerusalem_from_the_Mount_of_Olives_(NYPL_b10607452-80257).jpg)。NYPL 原文將美國公版與其他司法管轄區權利區分；Wikimedia 註明歷史原作與機械掃描的公版依據。畫家卒於 1924 年；不能把這張圖片謊稱成今日另行原創的線描藝術。
- 固定來源 SHA1：`8097a8aa1e5c1ee4ef0bcd126578b73d89229f04`，來源驗證與尺寸檢查失敗即停止生產。

## 真正可重建的原生 SVG 母版

- `scripts/build-olive-mountain-master-v43.py`：從公版掃描截取兩種不同的原始版畫構圖，經明度與輪廓保留處理，用 Potrace 在離線程序生成兩層不同墨階的**原生 SVG path**，無外部圖像 URL、`<image>`、base64 內嵌 JPEG、SVG 動畫或新的頁面執行時 JS。保留來源，不能聲稱逐線手工重刻。
- 桌面橫式 `static/images/p2-realms/v15/04-olive-woodward-cousen-desktop-intaglio-v43.svg`；手機獨立重新取景 `static/images/p2-realms/v15/04-olive-woodward-cousen-mobile-intaglio-v43.svg`。兩者都是編輯裁取原作，不是鏡像或重複橄欖枝。
- `static/experiments/olive-mountain-art-foundation-v43.html`：新母本放在**十二張已核准作品的完全可見安全區之外**，保留 A 中央軸線、B 非對稱刊頭；十二張原 3:4 PNG、`OliveSpeakerBaseline.mount` 的 Shadow DOM 英文字、OS 橄欖綠／晨光金／紙色皆不變。試驗是較高的獨立母版畫幅，沒有把 P2 的一屏滾動時序改成長頁。
- 舊 V13/V14/V42 留作研究與回退，不重寫它們。不改 01–03、ONE、P2 04 原動效、海報內容或主站。

## 品質門檻與限制

- `tests/olive-mountain-art-foundation-v43.cjs`：1648／1440／800／390 四個寬度，A/B、原十二張凍結英文、3:4、不覆蓋海報、按寬度正確選擇不同原生 SVG 的檢查。
- `.github/workflows/p2-0104-olive-preview.yml`：從公版原始掃描進行可重現的 SVG 建置；只在同倉庫 Draft PR commit SVG 產物、驗證、生成隔離 Chromium 截圖，再於隔離 Cloudflare 預覽部署。**即使流程綠燈，仍須目視核驗刻線保真、手機裁切、層次、閱讀與效能。**
- **藝術母版不等於已接入生長引擎。** 不應宣稱 V43 有真正可逆成長曲線動畫；必須另行按手冊 §6 及 MERSI §12 審核真正的部署構圖，再連接既有原生刻線機械。

## 預覽與證據

- [V4.3 隔離藝術預覽](https://p2-0104-1385.westsidewatch-github-io.pages.dev/experiments/olive-mountain-art-foundation-v43.html)
- [1648 B 原版海報＋歷史鋼版畫實拍](https://p2-0104-1385.westsidewatch-github-io.pages.dev/experiments/p2-0104-proofs/1648-olive-v43-static-folio.png)
- [390 B 獨立手機取景實拍](https://p2-0104-1385.westsidewatch-github-io.pages.dev/experiments/p2-0104-proofs/390-olive-v43-static-folio.png)

**當前狀態**：歷史版畫原生 SVG 母本和靜態藝術版已產出；CI 最終證據及人工創意驗收以實拍與測試結果為準。PR #1385 保持 Draft，禁止提前合併。 
