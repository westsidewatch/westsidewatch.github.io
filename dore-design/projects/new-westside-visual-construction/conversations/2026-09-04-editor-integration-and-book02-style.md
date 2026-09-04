# Conversation Archive — Editor Integration and Book 02 Style

Date: 2026-09-04
Project: Westside Publishing Program / Book 01 / Book 02
Record type: user-visible project dialogue excerpt

## User

我希望這兩個立項，能結合編輯器，比如聖靈也會做設計嗎，可以隨時展示隨時調整視覺發表意見，對於視覺上的書，預覽出來才能算草稿，因為本來就是設計書。第二本，天國語言極簡史，在編輯器裡，是可以多方改動的，比如我也可以直接在編輯器上接著寫書，多雷和你也可以寫，但我寫的部分，要有個AI不能改的權限，不然我就白寫了。當然放在編輯器裡，等於本地還有備份。最後，我希望你去研究「萬曆十五年」這本書的語言風格，並根據這本書的語風，建立「天國語言」這本書的完善語言風格，比如少副詞，多形容詞，冷靜的描述還是什麼特點，不要讓人看出是AI寫的。

## Resulting canonical decisions

1. Shared publishing editor architecture established at `dore-design/publishing/EDITORIAL-STUDIO-ARCHITECTURE.md`.
2. Book 01 visual-draft rule: **No preview, no draft.** Visual proposals count as drafts only when editable in Doré Design and inspectable via same-source HTML Preview/Export.
3. Book 02 requires a Longform Manuscript Studio where the user can continue writing directly.
4. Human-authored text defaults to protected source. AI cannot overwrite/delete/normalize/translate-in-place or unlock protected user text. AI edits must be suggestions/diffs until explicit user acceptance.
5. Local atomic saves, revision history, manuscript snapshots and protected-block checksums are required.
6. Book 02 language system now has a descriptive-first style guide at `dore-design/publishing/books/BOOK-02-LANGUAGE-STYLE-GUIDE.md`.
7. The style direction learns transferable methods from 《萬曆十五年》 without copying Huang Renyu's distinctive phrasing: concrete events before abstractions, large structures emerging from small details, analytical distance, restrained irony, and readable narrative joined to serious argument.
8. Book 02's own existing voice remains primary: scene → detail → lexical hinge → biblical/theological arc → reflection; short paragraphs, restrained modifiers, precise nouns/verbs, limited rhetorical questions, and cool-surface/warm-depth narrative temperature.
9. Engineering implementation tracked in GitHub issue #280, with protected-user-text hash invariants and editor-level acceptance evidence.
