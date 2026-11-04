# 《西望》B 純 SVG 生產工具鏈｜真實執行與多輪多雷探索紀錄

**2026-11-03 · status: B art direction BLOCKED / native vector output VERIFIED / deployment NOT approved.**
上級權威：[WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md) → [Toolchain](XIWANG-POSTER-TOOLCHAIN-EXECUTION.md) → [Poster Atlas](P2-XIWANG-POSTER-GENERATION-RESOURCE-ATLAS-20261103.md)。本紀錄不建立第二套 Design OS，不更動正式封面、P2 Runtime、Church、Emmaus、首頁 sevenfold，也不合併主站。

## 1. 從工具收藏到實際調用：本輪真的執行了什麼

| 工具/流程 | 執行狀態 | 實際結果／風險 |
| --- | --- | --- |
| [mono-color-skill](https://github.com/yanliudesign/mono-color-skill) v1.2.0 | **read and applied as art-direction guidance**, not installed as a drawing engine | 一個焦點、印版有主次、紙色有理由、結構性留白；其「最多兩墨」預設**不能**抹除 B 七個 OS 色的使用者指示。MIT 僅限程式/Skill，`examples/` 圖案不適用 MIT。 |
| [fontTools](https://github.com/fonttools/fonttools) | **executed** | 從當前環境的 Noto Sans CJK TC Bold（OFL 1.1；字型檔**未**複製進專案）提取「西」「望」複合輪廓/內白；以七組不同光學寬高與 counter adjustments 為種子。**不是已完成全新手繪字骨**。 |
| [Shapely](https://github.com/shapely/shapely) | **executed** | 對 glyph contour 做 even-odd boolean、region/Voronoi 空間分區、**真實 LineString∩字形 Region** 裁切；不靠一張背景紋理或 browser clipPath 偽裝字內刻線。 |
| [SVGWrite](https://github.com/mozman/svgwrite) | **executed** | 每條已裁切線段寫入 editable SVG `<path>`；七個 `data-word-layer`、七個 OS 色彩角色與七種 `data-line-family`，無嵌入圖片。 |
| [Inkscape](https://inkscape.org) 1.4 | **executed** | B4–B9 多輪 SVG 渲染，以及 B7 在 1648、768、390、320px 尺寸的 PNG proofs。 |
| Chromium / Playwright | **attempted, blocked** | 本環境阻止 `file:` 與 `http://127.0.0.1` 頁面，回傳 `ERR_BLOCKED_BY_ADMINISTRATOR`；不能冒稱本輪瀏覽器與完整 P2 捲動驗收。 |
| skia-pathops、d3-shape/d3-contour、penfill、vpype、SVGO、SVG.js | **researched / not executed in this environment** | 不假裝調用、也不為了「用了更多庫」重寫可工作的 SVG。下一輪可以對比它們與已能執行的 Shapely／Inkscape。 |

**已交付 repo：**
- [原生 B7 SVG，與 P2 Runtime 隔離](../../static/experiments/xiwang-printplate-b7.svg)
- [可重建 Python 生成器](../../scripts/xiwang/build-engraved-b.py)
- [系統工具前置與 build 命令](../../scripts/xiwang/poster-toolchain.mjs)
- [依賴清單](../../scripts/xiwang/requirements-printplate.txt)
- [隔離預覽 HTML](../../static/experiments/xiwang-printplate-b7.html)

## 2. 真實可執行生產指令

在 GitHub Draft checkout 中，安裝免費本地建置依賴（**不要部署成前端 runtime**）：

```bash
python3 -m pip install -r scripts/xiwang/requirements-printplate.txt
# 在 macOS 設定你實際安裝且有授權的繁體中文 Noto CJK TTC 或 OTF 路徑；不需下載任何付費字體
export XI_WANG_CJK_FONT='/actual/path/to/NotoSansCJK-Bold.ttc'
export XI_WANG_CJK_FONT_INDEX='3' # 本地 TTC 的 TC face；OTF 不需
node scripts/xiwang/poster-toolchain.mjs plan b
node scripts/xiwang/poster-toolchain.mjs build b ./xiwang-poster-output
```

這條新 `build b` 會實際執行 fontTools + Shapely + SVGWrite，成功後用可用的 Inkscape 輸出 PNG 證據；**只影響指定輸出目錄**。沒有字型或缺少依賴時會停止並報錯，而不是生成假的效果圖。B7 檔案不是 Final，`verify` 要求的完整 browser QA/人工藝術驗收未通過；不可拿成功的 node/inkscape exit code 取代。

## 3. 六輪可見比較與淘汰原因

| 版本 | 獨立視覺機制 | 視覺驗收 |
| --- | --- | --- |
| B4 | 七組全域刻線重合，七色都占較大面積 | **Reject**：字形識別太弱、像彩色雜訊 |
| B5 | Voronoi 字形局部分區，深墨主線 + 各區色彩 | **Reject**：大片字形只剩淡底、筆畫支離 |
| B6 | 深墨活字 + 字內反白刻線 | **Reject**：一半仍是普通黑字，其他區域過量 |
| **B7** | 連續印刷底層細線 + 七種獨立區域刻線，極少 OS 彩色亮點，紙色回到 OS | **Best engineering candidate, NOT art approved**：縮圖可識別「西望」，但字骨仍依賴 Noto 種子，線場缺少使用者所給參考的獨特強張力 |
| B8 | 改用 Noto Serif 字骨 + 曲線更明顯 | **Reject**：視覺過於傳統，和 A/B 區別減弱 |
| B9 | 取消大面積實心底，提升各區線密度 | **Reject**：上下密度不均，字體消散為紋理碎塊 |

**B7 SVG 自動證據：** SHA-256 `8ddac22a904fd7dce399f9df1d8d2088dfc0f4e15884cb3d7f2fe07b03f730c5`；7 個 `data-word-layer`、1275 個 path、0 個嵌入 `image`、0 個 rotate transform；Inkscape 已匯出 1648／768／390／320 四種 1:1 圖片。第二次獨立重新執行後 SHA256 一致。**這些是工程證據，不是官方獎項分數。**

## 4. 仍未符合得獎級標準：下一輪不得再做同類微調

**藝術阻斷 A — 字骨設計仍不夠獨特。** 不能因為 line intersection 真實就把 Noto 源字形稱為原創。下一輪先在 Inkscape／KAGE／Kumiko 等真正筆骨/輪廓工具上，分別重設「西」的承重與內白、「望」的上中下構件層次，再用可編輯 path 取代種子輪廓；保持兩字瞬間可讀。

**藝術阻斷 B — 七層現在僅局部可見，不夠像七組互相生成整體版面的字。** 不是繼續加 7 種顏色，而是探索 *不同字組尺度及套印位置仍共享一個中心與主次* 的構圖。必須對比至少三個真 SVG 構圖機制：集中精準套版、局部錯版交疊、字形大小變奏；每組都正立（0°）、線場真裁切字內、不做七排字條。

**藝術阻斷 C — 高級印刷海報還需實際對開驗證。** 下一輪應將 B 新母本與 P2 官方右 5:8 封面在真正 1648/768/390/320 及 200% zoom 中對照，測主次/留白/一致性；暫不改現有 runtime，也不合併 main。UI 有實際截圖才能評估是否通過單一 OS 10 維的 15/20 *探索門檻*，再由人工藝術決策確認。

## 5. 繼續多雷探索的停止條件

停止條件不是「找到更多 GitHub 專案」或「SVG 有內容」，而是 **有來源的成熟案例 → 真正調用工具 → 可重建原生字形與刻線 → P2 對開真畫面 → 使用者/人工藝術驗收**。任何一關未通過，應記錄失敗原因後嘗試*不同*的構圖/字骨機制；重複做相同線場、換色或套效果不算新的一輪。此文件只記本次已完成的實際階段，不承諾後台無人操作的持續執行。
