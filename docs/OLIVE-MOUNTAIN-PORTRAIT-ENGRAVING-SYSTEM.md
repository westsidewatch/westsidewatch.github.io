# 橄欖山人物版畫系統
OLIVE MOUNTAIN · PORTRAIT ENGRAVING SYSTEM · V1.0

本規範是 Westside Design OS 下橄欖山人物資產的製作規範，不建立平行的字體、色彩或 CSS 管理系統。人物肖像為主體，多雷式刻線塑造體積，單色印刷統一視覺，留白供網站 CSS 排版。

## 色彩與權威
| 用途 | 名稱 | 值 |
|---|---|---|
| 原紙 | Living Paper | #FAF9F5 |
| 唯一圖像墨色 | Olive Branch | #738A5A |
| CSS 正文 | Ink | #252525 |

來源：`docs/WESTSIDE-COLOR-AUTHORITY.md`、`static/css/westside-color-authority.css`（--ws-paper / --ws-olive / --ws-ink）。以上是生成資產的印刷配方；頁面仍透過 Design OS 語義 token 取色，不新增局部 CSS 色彩權威。CSS 的 --ws-engraving 混色角色不作為人物圖的第二墨色。

皮膚、頭髮、衣服、手、眼睛、麥克風與背景全部以同一橄欖綠墨色的覆蓋率、線距、排線疏密表現；紙面提供亮部。原照片的局部色相不保留。

## 參考與身份
真人參考照負責相貌、年齡、髮型、神情與姿勢。現有大衛鮑森圖 `/images/olive/david-pawson-editorial.png` 只作系列刻線、紙感、編輯品質參考，不複製姿勢、背景、光環或裝飾。
由確認真人照片衍生的版畫是 editorial illustration，不是來源照片，也不得標記為 verified source portrait。保留來源、衍生方式與身份核對紀錄；不以真人姓名憑空生成身份肖像。

## 每人四項變量
| 變量 | 填寫內容 |
|---|---|
| PERSON NAME | 講員英文名稱 |
| REFERENCE PHOTO | 已確認真人照及來源 |
| POSE / EXPRESSION | 原照自然姿勢與神情 |
| ENVIRONMENTAL MOTIF | 與人物有關的獨立環境元素 |

## 統一英文主提示詞
```text
OLIVE MOUNTAIN — Portrait Engraving Master Prompt V1.0

Create a refined, museum-quality editorial portrait illustration for OLIVE MOUNTAIN, the Christian teaching and sermon archive of Westside Watch.

Subject: [PERSON NAME]
Primary reference: [REFERENCE PHOTO]
Pose / expression: [POSE / EXPRESSION]

Use the attached real portrait photograph to preserve recognizable facial features, age, hairstyle, expression, and personal likeness. Use the existing David Pawson editorial portrait from Olive Mountain as a reference for the publication's visual language, engraving refinement, paper atmosphere, and overall editorial quality. Do not reproduce its exact composition.

ITALIAN MAGAZINE EDITORIAL STYLE
Italian magazine editorial style: refined Italian cultural magazine art direction, confident asymmetric composition, deliberate portrait cropping, generous negative space, quiet visual hierarchy, and an elegant relationship between image and future typography. Express this through composition and spatial rhythm, not added ornament or luxury advertising clichés. Keep all typography outside the artwork for CSS layout. Preserve the single olive-green ink, Doré engraving technique, recognizable likeness, and right-side typography-safe paper area.

VISUAL TECHNIQUE
Render the entire scene as a highly sophisticated nineteenth-century wood engraving, informed by the technical language of Gustave Doré's original engravings and the controlled ink-separation principles of contemporary monocolor editorial printmaking.
Use fine burin-like parallel hatching, precise cross-hatching, tapered engraved strokes, variable line spacing, stippling, and restrained halftone screening.
Construct the subject's face, hands, clothing, and surrounding objects through engraved line density, not painted colors, gradients, airbrushing, or photographic filters.
Facial features must remain natural, recognizable, dignified, and expressive. Use delicate marks around the eyes and mouth. Avoid excessive wrinkles, harsh black shadows, exaggerated anatomy, or artificial facial reconstruction.
Engraving must have convincing physical depth and sculptural volume, with a clear hierarchy between the detailed subject, secondary environmental lines, and almost invisible paper texture.

STRICT COLOR SYSTEM
Use exactly one monochromatic printing ink: Olive Branch Green #738A5A.
Use Natural Living Paper substrate #FAF9F5.
Produce all shadows, highlights, and midtones by changing the coverage, spacing, and density of the same green ink. The paper itself supplies the highlights.
The portrait, skin, hair, clothing, accessories, and environment must share the same ink color. No locally colored clothing, natural skin tones, pink, magenta, blue, gold, sepia, black ink, or independent accent hues.
Preserve genuine unprinted paper areas. Do not cover the entire image with a green color overlay.

EDITORIAL COMPOSITION
Create a vertical 3:4 composition.
Place the recognizable person in the left or lower-left portion of the composition, with an elegant, natural three-quarter or seated portrait arrangement appropriate to the reference image.
Keep the person sufficiently large to retain recognizable facial features but do not allow the subject to dominate the whole canvas.
Reserve approximately 35–45% of the canvas as open, quiet paper, with the principal typography-safe region on the right side. The region must have very low visual detail, strong tonal consistency, and enough uninterrupted space for large English display typography and smaller Traditional Chinese typography to be added separately with CSS.
The image must remain visually complete without text while supporting responsive web typography.
Let engraved detail progressively dissolve into natural unprinted paper toward the typography-safe zone. Avoid hard-edged split panels or artificial blank rectangles.
Keep critical facial features and hands away from expected typography areas and mobile cropping boundaries.

INDIVIDUAL VISUAL IDENTITY
Use one subtle, distinctive environmental motif connected to the subject's historical context, ministry, or character:
[ENVIRONMENTAL MOTIF]
The motif should remain secondary to the portrait, occupying no more than a restrained part of the engraved background.
Avoid generic religious iconography. Do not automatically add halos, crosses, Jerusalem skylines, open Bibles, stained-glass windows, golden circles, or ornamental borders.
Each person must have an individual composition while remaining unmistakably part of the same Olive Mountain collection.

PRINTING CHARACTER
The final result should resemble an exceptionally well-printed limited-edition editorial engraving on fine, softly textured archival paper.
Subtle mechanical halftone transitions, extremely fine engraved marks, and restrained print irregularities may be visible at close inspection.
Keep the image clear, elegant, quiet, and publication-ready. Avoid excessive distressing, muddy tonal masses, photographic collage, painterly brushstrokes, heavy poster graphics, and decorative clutter.

ABSOLUTE EXCLUSIONS
No text. No letters. No Chinese characters. No numbers. No captions. No logos. No watermark. No signatures. No typography generated inside the image.
No multicolor treatment. No colored skin or clothing. No gold-and-black palette. No halos behind the head. No generic sermon-poster styling.
Final artwork only, flat and borderless, without a mockup or frame. High-resolution vertical composition suitable for responsive website display and CSS typography overlay.
```

## 江秀琴：首個測試樣本補充詞
```text
Subject: Jiang Xiuqin (江秀琴).
Preserve her short dark hairstyle, warm joyful smile, natural facial proportions, and speaking posture from the supplied reference photo.
Render the microphone and Mandarin-collar brocade jacket entirely in monochromatic Olive Branch Green engraving. The original magenta clothing must have no magenta color.
Use understated botanical linework and soft architectural shadows as the distinctive secondary motif. Keep the right side open and unprinted for CSS typography.
Do not add any text or religious emblems.
```
上述姿勢、服裝等須與實際提供的真人照一致；缺少參考照時不執行身份生成。

## 義大利雜誌風格
固定關鍵詞：Italian magazine editorial style / refined Italian cultural magazine art direction。以有意識的人物裁切、非對稱構圖、大面積留白及安靜的視覺層級表達；遵守既有單色印刷、刻線與右側安全區，不添加奢華廣告裝飾或圖內文字。

## 網站排版
桌面右側留白供既有 Design OS 的 Bodoni Moda 英文、中文姓名和資料排版。手機允許圖像與文字上下重排。文字安全區刻線降至接近零，不以半透明遮罩補救失敗原圖。不得把姓名、標題或資料烘焙進圖像。

## 五項驗收
| 項目 | 通過條件 |
|---|---|
| 真人辨識度 | 與已確認真人照比對，相貌、年齡、髮型和神情自然一致 |
| 單色一致性 | 僅橄欖綠墨與紙面；無局部色相、黑墨、金色或全圖染色 |
| 刻線層次 | 臉部細刻、衣物次級排線、背景疏線；靠線密度塑造體積 |
| CSS 安全區 | 3:4；35–45% 安靜紙面；右側可排字；桌面與手機不遮臉手 |
| 人物背景獨特性 | 單一克制且與人物相關的元素，不複製鮑森構圖或套通用宗教海報 |

任何一項不合格即退回重新生成，不以 CSS 修補圖像缺陷。每次記錄參考照、鮑森視覺比對、桌面／手機預覽與五項結果。未完成比對不可宣稱驗收通過。

## 參考
- https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md
- https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/WESTSIDE-COLOR-AUTHORITY.md
- https://github.com/westsidewatch/westsidewatch.github.io/blob/main/static/dore-design/magazine-profile.olive-speaker.v1.json

mono-color 僅吸收印刷分版、原紙留白、刻線疏密與系列差異化；不繼承海報文字、預設配色、雙色、手寫符號、字圖碰撞要求。本規範落地不等於江秀琴圖已生成或鮑森視覺驗收已完成。
