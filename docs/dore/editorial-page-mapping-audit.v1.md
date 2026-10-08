# Doré editorial page mapping — audit 2026-10-08

Checked against main: `content/journal/_index.md`, `content/cinema/_index.md`, `content/olive/_index.md`, `content/church/_index.md`, `assets/css/typography-system.css`.

| Surface | Confirmed page | Scenario / first slot | Palette status |
|---|---|---|---|
| Magazine | /journal/ (alias /magazine/) | essay-concept / feature-lead | unresolved; no prompt |
| Cinema | /cinema/ | cinema-program / hero | unresolved; no prompt |
| Olive Mountain | /olive/ | section-hero / hero | green/white approved |
| Living Water West | /church/ | section-hero / hero | unresolved; no prompt |

`/archive/` is provisionally registered but its content page was not verified in this audit. The speculative `/olive-mountain/` alias must not be treated as a verified canonical route. The canonical confirmed Olive Mountain route is `/olive/`.

The shared typography stylesheet declares Bodoni Moda, Chiron Hei and Noto Serif TC, but also contains circular custom-property aliases (`--type-en` and `--ws-type-display-en`; `--type-zh` and `--ws-type-display-zh`). This audit does not change site CSS. The editorial image compiler must use explicit known font family tokens and leave site-wide CSS remediation to a separate change.

The page-map data file records only observed routes and initial editorial purposes; it is **not** an exhaustive scan of all magazine article templates. Different content cards, article leads and author profiles need per-item `dore_scenario`, `dore_slot`, `dore_palette` front matter or a separately verified template adapter.

## Next implementation gate
1. Confirm each section's actual color tokens from its canonical CSS/visual authority; do not invent them.
2. Add approved palettes as named compiler tokens and test for cross-section leakage.
3. Scan article templates for real slot geometry; distinguish desktop and mobile.
4. Generate image+CSS proofs for one real content item per scenario, with actual authorized portrait references where required.
5. Keep draft PR until visual review.
