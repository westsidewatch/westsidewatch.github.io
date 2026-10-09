# ChatGPT 普通對話 → GitHub 圖片寫入備忘錄

日期：2026-10-08
倉庫：`westsidewatch/westsidewatch.github.io`

## 已實際跑通的路徑

在**普通 ChatGPT 對話（非 Work 模式）**中，使用已連接的 GitHub Connector，完成一張小型 PNG 的二進位提交：

1. 從 ChatGPT 對話檔案庫列出既有的 ChatGPT 生成圖片；以 `files__materialize` 將生成圖片原始檔案複製到工作容器。
2. GitHub Connector 的 `mcp__GitHub__create_blob` 接受 `encoding: "base64"`，可建立圖片 Git Blob。
3. 使用 `mcp__GitHub__create_tree` 將 Blob 指向倉庫內的圖片路徑。
4. 使用 `mcp__GitHub__create_commit` 建立 Commit，再以 `mcp__GitHub__create_branch` 建立獨立驗證分支。
5. 從 GitHub Git Tree API 讀回檔案條目，確認路徑、Blob SHA 和大小。

## 驗證憑據

- 測試分支：`experiment/chatgpt-image-blob-proof-20261008`
- Commit：`b2bff17dcb482a856395f37c0ed0a9a644cbd306`
- Tree：`ad59c5dada41a06b2062b88647c0cf4e7c51014a`
- Blob：`eef0dca26d34ca0b6f4d4872cecff2157778185d`
- 路徑：`assets/image-upload-probe-20261008.png`
- Git Tree 回讀大小：**69 bytes**
- `main` 未因這次圖片驗證而修改。
- Commit：https://github.com/westsidewatch/westsidewatch.github.io/commit/b2bff17dcb482a856395f37c0ed0a9a644cbd306

**範圍限制：**實際成功提交的是 69-byte、1×1 像素 PNG 測試檔，不是原尺寸生成圖。對話檔案庫內曾成功取得一張約 2.7 MB 的生成圖片，但**未**將該原尺寸圖片上傳至 GitHub；數 MB 圖片在工具資料傳遞上的上限仍未驗證。GitHub Fetch 對二進位 Contents URL 會拒絕（只接受 UTF-8），故回讀使用 Git Tree 元資料，而非宣稱已用 Fetch 完整下載 PNG。

## 後續執行規範

- 不得再斷言普通 ChatGPT 對話沒有 GitHub 二進位寫入工具；先盤點 `create_blob` / `create_tree` / `create_commit` / `update_ref`。
- 先取得生成圖片原始 bytes，轉 Base64，提交 Blob、Tree、Commit，再更新目標分支。寫入正式站前應確認路徑及分支。
- Git Blob 建立成功**不等於**網站已部署；須確認分支更新、GitHub Pages 部署及實際資產可讀取。
- 不必為圖片上傳預設引入 Cloudflare R2、A2A、Mac mini、本地製圖服務或額外付費工具。
- 如遇較大圖片傳輸限制，應報告具體失敗環節，不得把未驗證的限制說成產品收費政策。
- 既有另一條路徑：`tools/github-image-uploader/README.md` 記錄 Cloudflare Worker 上傳服務；它是可選方案，並非本次成功路徑。

## 教訓

先查驗已連接工具的**全部**能力，再設計替代工程。不得只檢查 `create_file` / `update_file`（UTF-8）就斷言 GitHub 不支援圖片。這次確認普通對話可以使用 Git Data API 提交小型 PNG，但尚未證明原尺寸生成圖片的完整交付。
