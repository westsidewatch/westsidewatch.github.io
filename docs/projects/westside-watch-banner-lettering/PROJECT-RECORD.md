# WESTSIDE WATCH 英文旌旗字體｜獨立工程記錄

建立：2026-11-17。狀態：Draft／字形與動效母本研究，**未通過藝術驗收，未接入正式 P2**。

## 1. 項目使命與兩階段邊界

**階段 A（當前 P2 需求）：** 製作固定文字 `WESTSIDE WATCH` 的原創超寬、極粗、高張力 SVG 字形，供 P2 第一層橄欖山刊頭點擊後的「雙經文方塊 × 七重疊」轉場使用。**旌旗展開＝兩方塊與英文大字連動的七重疊全過程**；不能誤解成字母自身須單獨演完完整旗幟動畫，也不能讓裝飾波浪取代既有 Codrops 轉場。完成階段 A 不需要造出整套字庫。

**階段 B（未來獨立品牌字體）：** 在階段 A 完成並驗收後，再將九種原創字形擴展成 Westside Watch 自有英文旌旗字體，研究完整拉丁字母、數字、標點、字距與字偶距、不同尺寸母本、動態主軸及可用字體格式。不得為了 B 阻塞 A，不得聲稱目前九個字形已是可安裝字體。

## 2. 最高設計原則

「**靜如山岳，動如旌旗。**」參見 `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` §13。

- 中文大「西望」更傾向山岳／大地根基／聖殿石材；現有第二版仍過於柔軟，需提升承重、重心與石質張力。
- 英文大 `WESTSIDE WATCH` 更傾向被風**繃緊、高舉**的得勝旌旗，**不是柔軟布條或氣球字體**；厚重、扁橫、不可任意拉伸。
- 旗面張力可由少數平滑、連續的局部曲線呈現；不做每字切口、不做整排軟波浪。完整迎風展開由**字形、兩個正方塊及七重色彩**共同實現。
- 出埃及記 17:15（耶和華尼西）是意義核心；不靠剪貼十字架或旗幟圖示表達神學。

## 3. 目前版本與資產

| 狀態 | 資產 | 評定 |
|---|---|---|
| 已批准方向，待細修 | `static/images/westside-watch-lettering-v4-transparent.svg` | 原創超寬實心字形；階段 A 母本，不代表獲獎品質 |
| 排版校樣 | `static/images/westside-watch-standard-v4-editorial.svg` | 靜態標準校樣 |
| 拒用 | `static/images/westside-watch-lettering-v5-xiwang-transparent.svg` | 錯誤的局部尖銳切口；保留研究痕跡，禁止接入 P2 |
| 衍生研究，未批准 | `static/images/westside-watch-standard-v6-taut-study.svg` | 字形未變，曲線呈現在外部張力線上；**不能取代七重疊** |
| 中文研究，未批准 | `static/images/xiwang-mountain-study-v1.svg` | 使用正式 P2 二版輪廓的無破壞衍生研究；須經石材承重藝術評估，禁止覆寫正式「西望」 |
| 中文已批准原件 | `static/images/xiwang-poster-a-night-blue-approved-p2.svg` | 不得直接改壞或覆寫 |

九種不同英文字母為 W/E/S/T/I/D/A/C/H；固定文字共十三個字母。源 SVG 必須保留路徑可編輯與透明背景的核心母本。

## 4. 已選參考的正確角色

- **字形骨架：** Druk Wide Super（極寬與極重）、PP Monument Extended Black（紀念碑承重）、Sharp Grotesk Black Wide（光學修正與曲線張力）。僅作造型研究，作品須為自繪路徑，不直接複製或散發商業字體。
- **完整識別系統：** EuroPride 2018 — Loud & Proud 的「字體、旗幟色彩、容器與互動」一體化方法；**不照搬氣球形狀**。
- **動效技術：** 原先已選 Codrops 雙方塊成熟機制及 GSAP／七重疊，按 P2 現有入口接入；拒絕並列、互不相干的兩套動畫。
- **曲線工藝：** Glyphs Drawing Good Paths／Harmonization；SVG 節點、切線連續、內外輪廓重量與字腔須光學驗收。

## 5. 階段 A 的交付與驗收

1. 保留 V4 超寬厚重輪廓，製作少量細修候選，實際渲染比較；先過靜態字形審美與可讀性關。
2. 雙經文方塊為**正方形**、經文排版依既有 Scripture Studio 規範；方塊穿行時帶動七重疊在英文內外構成完整旌旗展開，不得另加獨立花俏動畫。
3. 橄欖山**刊頭點擊**觸發第一層→第二層；普通滾動仍通往後續 P2 第一層，不劫持滾輪、不新增平行第二層。
4. 最後停在目標版塊 Design OS 顏色；手機／桌面／反向返回／reduced-motion 可用。
5. 01–03、已批准「西望」母本、十二張講員海報和既有英文排版全部保護；Draft 真實瀏覽器通過前不能合併或宣稱達獎項標準。

## 6. 階段 B 預留

獨立字形矩陣、Glyphs／UFO 相容輪廓、完整字距／字偶距、靜態與動態字體格式、字體授權及發佈策略均待 A 驗收後另定。不得在 A 階段以未完成的字庫替換原創 SVG。

## 7. 目前實際狀態

2026-11-17：建立獨立記錄並新增兩份**尚未批准**的中英靜態衍生校樣；**尚未完成**雙方塊／七重疊一體化動畫、真實瀏覽器藝術驗收、正式上線。下一步對兩份 SVG 做嚴格比較和幾何修正，再進入 P2 轉場接入。

### 2026-11-17 追加校樣（仍未批准）

- `static/images/westside-watch-lettering-v7-taut-curves.svg`：從 V4 自繪字形直接重繪 E／T／H 的局部水平輪廓，以小幅 Bézier 曲率呈現緊繃旗面。字高、超寬比例、粗筆畫及字腔保留。這是階段 A 的新候選，不是已完成七重疊動畫。
- `static/images/westside-watch-v7-curves-proof.svg`：V7 的排版校樣。
- `static/images/xiwang-mountain-study-v1.svg`：沿用已批准「西望」外輪廓，試驗厚度、石材陰影與落地線。**藝術自評不足：仍未真正修正原字形的柔軟筆勢，不能當作聖殿基石版本完成品。**
- `static/images/westside-watch-standard-v6-taut-study.svg`：僅外部曲線試稿，證實外部曲線與字形分離，不可作為最終旌旗解決方案。

### 2026-11-17 字形修正 V8／山岳 V2

- 英文 `static/images/westside-watch-lettering-v8-balanced.svg`、排版 `static/images/westside-watch-v8-balanced-proof.svg`：I 上緣加入與 E／T 相同的輕微凸曲，WATCH 的 A／T／C／H 光學側距收緊，與 WESTSIDE 的視覺密度一致；保持超寬／極粗。已渲染校樣，尚未完成 P2 真實轉場藝術驗收。
- 中文 `static/images/xiwang-mountain-v2-structural-foot.svg`：撤回失敗的整塊直角重建；只修「望」下部過圓的右端輪廓及承重轉折，原有筆畫連續。**仍待進一步去除『像腿』的視覺聯想、提升聖殿基石感，不能聲稱完成。**
