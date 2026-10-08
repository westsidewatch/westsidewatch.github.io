# Doré magazine image-generation scenario matrix v1

The **same visual grammar** must not mean the same image prompt. The magazine uses three independent decisions:

1. **Scenario**: what editorial work the image performs.
2. **Slot**: where the image lives and how it is cropped/overlaid.
3. **Composition recipe**: the chosen spatial strategy, not an automatic default.

The compiler combines these with subject, verified references, material technique and palette to emit `art-direction.json`, `image-prompt.md`, and `css-layout-contract.md`.

## Scenario library

| Scenario ID | Editorial use | Visual treatment |
| --- | --- | --- |
| `speaker` | Sermon speaker | Identity-safe strong face and garment form |
| `column-author` | Recurring columnist | Stable identity, repeatable signature crop |
| `interview-subject` | Interview | Encounter, off-axis gaze, supported context |
| `witness-testimony` | Testimony | Privacy-sensitive, restrained portrait or symbol |
| `essay-concept` | Opinion/essay | One argument-driven object or metaphor |
| `historical-feature` | Historical feature | Evidence-aware architectural/document fragment |
| `book-publication` | Books and publishing | Object, paper and cutout grammar |
| `cinema-program` | Film programming | Rights-aware cinematic frame or abstract motif |
| `section-hero` | Section opening | Immersive crop and large live-title corridor |
| `archive-thumbnail` | Archive index | Strong reduced silhouette, thumbnail readability |

## Output slots

| Slot | Ratio | Primary concern |
| --- | --- | --- |
| `cover` | 3:4 | Graphic tension with live title |
| `feature-lead` | 4:5 | Story opener |
| `inline` | 3:2 | Reading rhythm and external caption |
| `profile-card` | 4:5 | Reusable person identity |
| `hero` | 16:9 | Desktop/mobile crop and type-safe region |
| `thumbnail` | 1:1 | Recognition at small size |

The ratios are first-pass targets, not claims about current production components. Every output needs real responsive visual review.

## Example commands

```sh
python3 scripts/compile_dore_editorial_brief.py --scenario speaker --slot cover --subject 'David Pawson' --recipe overscale-collision --portrait-style face-fragment --material engraving
python3 scripts/compile_dore_editorial_brief.py --scenario column-author --slot profile-card --subject 'Verified columnist' --recipe quiet-field --portrait-style shoulder-sculpture --material halftone
python3 scripts/compile_dore_editorial_brief.py --scenario interview-subject --slot feature-lead --subject 'Verified interviewee' --recipe two-scale-encounter --portrait-style silhouette-interruption
python3 scripts/compile_dore_editorial_brief.py --scenario historical-feature --slot inline --subject 'Limestone city gate fragment' --recipe monumental-interruption --material engraving
```

Use `--verified-reference` **only if** a verified authorized reference is actually provided with the ChatGPT image-generation request. This flag does not supply the photo, verify permissions or remotely fetch an image. When the reference is absent, the brief must not claim to depict the real person.

## Production policy

- All generated image assets are **text-free**. Chinese and English type, labels, rules and responsive placement are HTML/CSS.
- Color belongs to the current section's design tokens. The current compiler implements the Olive Mountain green/white palette only; other magazine sections must receive their own approved tokens before production.
- The Italian magazine grammar supplies cropping, negative-space, scale and print methods, not a mandatory repeated look.
- For every scenario, review the image **together** with its CSS text composition.
- No automatic publishing, no inferred identity, no invented historical claims, no unverified copyrighted imagery.

## Engineering boundaries

The scenario matrix is an initial extensible registry. It does not yet inspect actual page templates, infer the correct slot from routes, or attach reference assets automatically. This PR must be validated against real magazine pages before treating it as a site-wide production contract.
