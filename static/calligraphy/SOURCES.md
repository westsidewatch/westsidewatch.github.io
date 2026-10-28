# Calligraphy collection sources

Only expose a selectable collection after its source and exact index key have been verified.

## Shared GLEAN method / 拾字方法

- [《西望》碑學／帖學、宮殿匾額／殿柱楹聯與榜書的大字研究](https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/calligraphy/XIWANG-STELE-PLAQUE-BANGSHU-ARCHITECTURAL-LETTERING-20261028.md)

- [《西望》07／09 舊小字原帖史料索引（現非刊名主選池）](https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/calligraphy/XIWANG-07-09-ORIGINAL-SOURCE-BOARD-20261028.md)
- [碑帖真跡集字 → SVG → AI 缺字補全（共同研究方法）](https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/calligraphy/GLYPH-SOURCE-TO-SVG-AI-FALLBACK.md)
- Design authority: [Chinese Logo Lab](https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/calligraphy/LOGO-RESEARCH-DESIGN-CENTER.md)
- Use existing verified glyph sources first. Crop and verify the original work; keep ImageMagick + Potrace active. VTracer is a comparison candidate; AI generation remains a **labeled, rights-reviewed fallback**, not an installed production provider.
- No historical-looking glyph, font or AI output is selectable as a verified master without source, pixel proof, optical review and rights clearance.

## Verified

- 米芾 行書 — `neil-zt/calligraphy-community`, exact collection key: `米芾 行書`.
- 王羲之 集字聖教序 行書 — `neil-zt/calligraphy-community`, exact collection key: `王羲之 集字聖教序 行書`.

## Not yet exposed

- 文徵明 行書 — no verified directly usable collection has been connected yet. Do not expose an empty selector.

The upstream `zhuojg/chinese-calligraphy-dataset` is the original Apache-2.0 dataset behind calligraphy-community and contains 138,499 images by 19 calligraphers / 7,328 characters, but a writer/style pair must still be verified before being presented in the UI.
