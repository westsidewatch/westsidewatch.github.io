# Doré → ChatGPT visual production handoff

**Goal:** Let Doré make editorial decisions and ChatGPT generate the actual finished image. Do not make Mac mini diffusion, A2A, SVG geometry, Pillow paste-over, or separate local typography compositing prerequisites.

```sh
python3 scripts/build_dore_chatgpt_handoff.py --speaker david-pawson
```

Copy the resulting `local/dore-chatgpt-handoff/david-pawson-chatgpt-brief.md` into a ChatGPT conversation and request image generation. This file contains scene-specific composition, engraving, material, palette, text, quality and acceptance instructions. The first proof is non-portrait unless an approved reference photo is supplied.

When a verified and rights-cleared photograph is attached to the SAME ChatGPT request, use `--verified-reference` to compile an identity-preserving portrait transformation brief. **The flag does not provide the photograph and does not verify rights**; the image must actually be supplied. Do not invent a speaker's appearance.

This handoff requires no API key or paid image backend beyond whatever image-generation access the user already has in ChatGPT. The generated image still requires human visual approval before publication. Retain the older local A2A renderer as optional infrastructure, not as a mandatory production stage.
