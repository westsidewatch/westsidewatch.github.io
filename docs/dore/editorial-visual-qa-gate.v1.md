# Doré visual editorial acceptance gate v1

Each compiled image brief now emits a fourth artifact, `visual-review.template.json`, alongside art direction, image prompt and CSS layout contract.

The gate separates **structural contracts** (machine-verifiable) from **visual evidence** (reviewer-verifiable). It never reports face similarity, color pixel accuracy, actual mobile crop or image-text overlap without a rendered image and review evidence.

## Acceptance checks

Identity / reference rights; crop and protected face landmarks; negative space; printmaking texture; section palette; actual HTML/CSS title-image collision; responsive previews at 320, 375, 768 and 1440 CSS px; source accuracy.

Review JSON must supply a status (`pass`, `fail`, `pending`, or narrowly allowed `not-applicable`) and evidence for every claimed pass. `not-applicable` is limited to identity and type collision, and needs a rationale. All checks default to pending. For speaker, columnist or interview subject, a verified reference is required before even editorial readiness can be reported.

```sh
python3 scripts/compile_dore_editorial_brief.py --route /olive/ --scenario speaker --subject 'Verified speaker' --portrait-style face-fragment --material engraving --out local/dore-portrait-proof
# Fill review evidence after image generation and responsive visual inspection.
python3 scripts/review_dore_editorial_art.py --spec local/dore-portrait-proof/art-direction.json --review local/dore-portrait-proof/visual-review.template.json --out local/dore-portrait-proof/qa-report.json
python3 -m unittest discover -s scripts -p 'test_*dore*py'
```

**Note:** `--route` overrides `--scenario` with the page default. For individual speaker or columnist art, use explicit scenario/slot without `--route` until the route adapter supports article-level scenario overrides, or supply appropriate front matter with `--content-file`. This is a known limitation, not silently inferred.

A successful review only sets `ready_for_editorial_approval=true`; `publication_approved` always remains false. Actual publication requires a separate editorial decision and deployment validation. No image generation, face verification, screenshot capture, or CSS rendering is performed by this QA script.
