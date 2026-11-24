# P2 05 黎明書局｜隔離整合與資料保全紀錄
日期：2026-11-21  
狀態：施工中，**不得合併或正式發布**

## 絕對禁止及工作邊界
- 不使用 ChatGPT Sites，不建立、開啟、修改、部署或轉移任何 Sites 專案。
- 保全分支 `archive/p2-05-preserved-20261121`：只讀，不得修改、刪除、重置或強制推送。
- 原始工程分支 `p2-0105-dawn-library-preview-20261120`：不修改；原有 PR #1403 不合併。
- 只在 `work/p2-05-integration-repair-20261121` 進行隔離施工。
- 不刪除工作資料、任何藏書書目、圖像、插圖、導讀、經文母版、V9 字形或歷史資產。
- 不把工程文案、版本代碼、診斷標記或測試說明顯示在讀者頁面。

## 已保全六項重要檔案
| 檔案 | Git blob SHA |
| --- | --- |
| `static/js/p2-0105-dawn-continuation.js` | `a3c29dbb42a6180ef71a804d8809458c8021c49b` |
| `static/css/p2-0105-dawn-continuation.css` | `43e079f809f8a3fdcbc122d8ec51cbde36f343c2` |
| `static/experiments/p2-0105-dawn-preview.html` | `23e4a49fce03724f7ff7e1889ad5dd90664e8320` |
| `static/dawn-library/p2-editorial-channels.json` | `a0a165b716aaf49e4afc31aeaac123f0e999aaa0` |
| `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` | `1203252e9d2c53da23181467886df9f11564590d` |
| `static/images/p2-dawn-letterpress-engraving-v1.svg` | `32136673a3819636550e82f4976a3369e3b09e2e` |

以上六項在保全分支及原始工程分支逐一比對一致。這是**六項檔案驗證**，不得寫成對整個倉庫的全量驗證。

## 本次隔離修改
1. 建立 `static/css/p2-0105-dawn-integrated.css`，原 CSS `p2-0105-dawn-continuation.css` 仍原樣保留。新檔從既有各階段萃取有效樣式，移除互相覆蓋的舊版列表、R22/R24 配色及試驗性背景線條。
2. 隔離預覽 HTML 指向新整合樣式；P2 01–04、主站正式頁及原工程預覽均未修改。
3. P2 05 的 V9 轉場，使用實際可測量的經文 iframe 幾何位置，而非 CSS 已設成 display:none 的落點元素。保留原 V9 SVG 字形，避免添加覆蓋色片。
4. 第二層封面牆在展開轉場時開始取得已有封面；完整館藏索引只在讀者點擊入口時載入。
5. Scripture Studio 對公共嵌入版的中文、英文印面均取消研究用的 `STUDY · NOT APPROVED` 浮水印。工具本身的研究模式不因此被冒充為已審定。
6. Scripture Studio 原 R24、R23、R32 三個互相覆寫的 05 專屬嵌入樣式，整理成單一 `CONSOLIDATED DAWN LETTERPRESS` 區段；原版經文與排版計算函數保留不變。
7. 已建立獨立 **Draft PR #1411**，由隔離施工分支指向原工程分支；不合併主站或原工程。

## 目前檢查
- JavaScript：可被 Function 語法解析。
- 整合 CSS：花括號成對，字串與註解有完整終止。
- HTML：無重複 ID，正確引用整合 CSS，來源連結保留新分頁。
- Scripture Studio：兩個嵌入印面均不顯示研究浮水印；05 專用嵌入樣式只保留一組，HTML 以 `r38` 更新快取。
- 比對分支：此 Draft PR 只修改五個檔案，沒有刪除既有檔案；以 GitHub compare 回傳為準。
- 原樣式內 `!important` 約 481 處，整合樣式約 358 處；數量降低**不等於設計已驗收**。

## 尚未完成／禁止聲稱通過
- 尚未完成 Cloudflare 實際部署與桌面／手機 Chromium 的畫面回歸驗收。
- 未證實旌旗每一幀、反向滾動及第二層進場沒有色塊閃現或停頓。
- 黎明書局刻線底紋尚缺經藝術審定的成熟來源；**原先程式生成的線紋僅封存，不視作合格母本。**
- 各單書深度導讀尚未覆蓋全部館藏。
- 三晨星、光譜、策展集的主題分類仍需逐書來源查核及正式內容評審。
- 實際的作品、館藏、來源、站內閱讀和返回操作均須逐項驗收。

**發布門檻：** 必須對第二、第三層的真實視窗進行逐畫面檢驗，並核對功能和原始資料；在此以前 PR 必須維持 Draft。
