# 橄欖山 V79 — Museum Folio 翻卡與 Botanical 中密度構圖

日期：2026-11-08
階段：**Draft 檢驗中**；不得合併 main。

## 需求與本輪決策

使用者指出 V77 翻卡速度仍太急、不夠順暢；作為視覺探索的橄欖枝 AI 圖像第二版又太稀疏。參照 §9「多雷探索」V78 紀錄與 §11「滾多少走多少、停手即停、反向即回」，選擇 **A · Museum Folio + 原生 CSS 3D**；**不安裝 Lenis / Motion / GSAP**，不新增第二進度控制器。

## 施工實物與關鍵差異

- `static/js/p2-0104-olive-continuation.js`：保持 `pairStart=11.95`、11 次左右交替，將十二人索引 `indexStart` 從 20.20 延到 23.00；最後 `indexEnd=24.10`、`end=24.50`。每個換人事件的滾動長度從 0.75vh 到約 1.005vh，增加 **34%**。
- 每一次翻牌的 entering 姿態從 `ease((beat-.04)/.44)` 改為 `ease((beat-.03)/.48)`，退場從 `ease((beat-.55)/.40)` 改為 `ease((beat-.53)/.44)`；翻牌自身的有效行程相應增長約 **46–47%**。兩段間保留輕微的穩定呼吸，不新增時間慣性。
- `turnFace` 只向實體外殼寫 `rotateY`；透視尺度固定在整個 `pair` 容器，避免每幀以不同維度重組 `perspective(px) rotateY`。保留完整 3:4 講員原圖及姓名 Shadow DOM 在同一剛性卡體。
- `position()` 透過 WeakMap 比對四個已註冊尺寸，未變的 `left/top/width/height` 不重複寫入；翻卡只有角度變化時才重寫 `transform`。保留唯一 RAF 的 scroll dispatcher。
- 延長 CSS 卡片舞台 `#p2-olive-track` 至 2600svh，預覽滑桿、跳轉控制及 1648／390／320 瀏覽器測試全部同步更新。

## Botanical / 中等偏豐富

- 不是把先前 AI 的紙張圖直接當背景：新增六幅原生可編輯 `static/images/p2-realms/v15/v79-botanical-field/04-olive-field-v79-{1..6}.svg`。
- 六幅沿用 **Walter Crane 公共領域歷史橄欖枝原始路徑**，保持 Design OS 橄欖綠底、Morning / Pale / Warm Gold 刻線，不製造新色票；以 6 個區別方位、尺度和透明度形成上枝、冠層、左沿、腰間、下枝、下方側枝。
- 原 V60 的六階段生長保留，但從強烈重疊的局部集中改為寬鬆的外緣配置。全十二人時植紋總透明度從 V77 的約 0.26 提高到約 0.435，再以每張母本 0.49–0.82 的透明度細分，避免少到空白或繁到搶海報。
- 五項不可破壞：講員正面完整、陰影 DOM 字型完整、分布在各張卡背面的 SVG 不動、Terrain 真實地理母本不動、02/03 及主站不動。

## 對比與驗收

- 原快翻與新 Museum Folio 分段：保留 V78 隔離校樣作 A/B 證據；不把 demo 頁直接替換 P2。
- 硬測試：慢速進入與停手、單一小幅度 10/30/60px 滾動、反向角度可復原、六張刻線背景逐層生長、320/390/1648、12 張原版字體、最後 CTA、無可見色塊切線、reduce-motion。
- **未取得實際最新 Chromium 截圖和被證實的部署，不能宣稱得獎完成或上線。** GitHub Actions 內部 PASS 只證明工程契約，仍須比較真實視覺畫面。

## 外部技術來源

V78 多雷探索詳細研究與開源授權見 [V78 研究記錄](V78-FLIP-DORÉ-EXPLORATION-2026-11-08.md)。優先採用瀏覽器原生 CSS 3D 和已有的唯一 MERSI scroll owner；參考 MERSI 和 Codrops 案例，不複製別人網站的視覺成品。
