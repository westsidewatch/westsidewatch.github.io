#!/usr/bin/env python3
"""Compile Doré speaker art direction into ChatGPT-ready, self-contained briefs.
No renderer, API, paid dependency, or publication action.
"""
import argparse,json
from pathlib import Path
from build_dore_speaker_previews import SOURCE,compile_record
SCENES={
 'olive-branches':('Ancient olive tree and terraced limestone hillside','A single twisted trunk anchors the lower left; the crown crosses the upper third; sparse distant terraces recede toward the right. Bark, foliage and dry stone are described by distinct line grammars.'),
 'scripture-pages':('Open Bible on a wooden lectern','The book is seen from slightly above; pages form a luminous diagonal; a restrained stone interior recedes behind it. No invented legible verse.'),
 'stone-arch':('Weathered limestone arch and stairs','Off-center arch on the left, steps receding into a quiet courtyard; distinct block joints and directional shadow hatching.'),
 'mountain-light':('Judean limestone mountain landscape','Asymmetric layered ridges; foreground geology rendered in short contour hatches, distant slopes with progressively finer line density.'),
 'courtyard':('Ancient courtyard and olive tree','A narrow colonnade recedes behind one olive tree; stone bench and worn paving convey scale without figures.'),
 'open-book':('Antique open book and olive sprig','Book occupies the foreground diagonal, with page-edge relief and carved table texture; calm white space above.')
}
def brief(spec,has_reference):
 subject,composition=SCENES[spec['motif']]
 name=spec['displayName']
 identity=(
 f'A VERIFIED reference photograph of {name} is supplied with this request. Use it as the sole identity source. Preserve the subject\'s facial geometry, age cues, hairline, expression and proportions; transform the verified photograph into finely engraved olive-ink linework. Do not invent or beautify a different face. Position the recognizable face within the upper 65% with breathable negative space.'
 if has_reference else
 f'No verified reference photograph for {name} is attached. Do not fabricate a recognizable likeness or substitute a stranger\'s face. Use the editorial still-life scene described below as the cover image. This is a temporary non-portrait proof, not a permanent ban on portraits.'
 )
 return f"""# DORÉ / OLIVE MOUNTAIN — CHATGPT IMAGE GENERATION BRIEF
Project: Westside Watch / Olive Mountain
Subject: {name}
Status: design proof only; NOT approved for publication
Deliverable: ONE finished 3:4 portrait magazine cover, ideally 1440 × 1920 pixels or higher.

## 1. Creative authority
You are executing a finished art-director specification, not inventing a new brand. Produce an actual high-quality image, not SVG placeholder geometry, a mockup photographed on a desk, or an explanation of what you would generate. The target is a credible Italian editorial magazine cover with the physical sophistication of a carefully printed engraved illustration.

## 2. Identity and visual subject
{identity}
Editorial scene alternative: {subject}.
Exact scene direction: {composition}
Subject matter is Christian sermon editorial content. No unrelated religious iconography or spiritualist motifs. Do not add unsupported biographical facts or sermon titles.

## 3. Art direction and spatial composition
Canvas 3:4, upright. Use a confident asymmetrical editorial composition, not centered clip art. Establish a clear foreground, secondary midground and restrained background. One strong focal point visible even as a small thumbnail. Preserve a clean title zone with enough actual negative space for type. Allow the illustration to breathe; do not place a rectangular photo in a generic card. At least 48px-equivalent edge safety on a 720px design width.
Top 10%: quiet masthead with generous breathing room.
Middle 12–72%: principal illustration; vary line density to guide attention.
Bottom 75–95%: integrated typographic title area, composed as part of the cover rather than a white bar pasted across the picture.
Bottom 5%: unobtrusive edition line.
No overlapping text, no clipped characters, no arbitrary dividers.

## 4. Engraving and physical printing
Use detailed etched/copperplate engraving language: precise contour lines, short directional hatches following form, deliberate crosshatching only in deeper shadows, and untouched white paper for light. Distinguish wood grain, stone grain, foliage, hair and fabric with material-specific linework. Rich tonal hierarchy must come from controlled ink density and paper knockout, not photographic blur, muddy gradients, synthetic grain or crude halftone dots. Avoid pseudo-engraving filters, thick cartoon outlines, crude green circles, flat stock vector graphics and generic symmetrical ornament.

## 5. Strict palette
White paper #FFFFFF, deep olive ink #174B35; optional supporting olive #47735E only if needed. No gold, black-gold, sepia, tan, beige, ochre, orange, blue, magenta or default blue hyperlinks. The final picture should read as green ink on clean white paper, including any rendered face.

## 6. Typography — final cover, not an overlay proof
Main name: 「{name}」 exactly, in one coherent Chinese text group. Do not split characters across lines unless a deliberate, legible editorial break is approved. Ensure sufficient glyph spacing and no collision with English.
Masthead: OLIVE MOUNTAIN
Small edition line: SERMONS / PEOPLE
Use a refined Chinese serif compatible with the site's approved typography and restrained Bodoni Moda Regular-like Latin letterforms; no faux bold, no decorative swashes. Prefer typographic clarity over ornament. Do not invent any additional headings, numbers, logos or quotations. If precise Chinese rendering is unreliable, keep a clear reserved title area and return the artwork for a separate typography pass rather than generating broken Chinese characters.

## 7. Negative constraints
No anonymous fake speaker portraits, no identity swapping, no face melting, no distorted eyes or hands, no blurry faces, no low-resolution painting, no orange flesh-tone image, no cheap poster templates, no blocky geometry, no noisy AI text, no illegible Chinese, no random religious symbols, no watermark.

## 8. Acceptance criteria
A. Recognizable likeness ONLY when a verified reference is actually supplied; otherwise no claimed portrait identity.
B. Crisp linework and coherent materials at full resolution and thumbnail size.
C. Olive-and-white print palette throughout.
D. Chinese title legible, correctly grouped, without overlap.
E. Visually convincing editorial hierarchy and no hard white paste-over strip.
F. This is a design proof; do not publish or silently substitute assets.

## 9. Output instruction
Generate the image now. Make one deliberate, finished composition. If a supplied portrait reference is absent, execute the still-life alternative without asking the user to fabricate a likeness. Return the image for visual review.
"""
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--speaker',default='david-pawson')
 p.add_argument('--out',default='local/dore-chatgpt-handoff')
 p.add_argument('--verified-reference',action='store_true',help='Set only when a verified, rights-cleared photo is actually attached in the ChatGPT request')
 a=p.parse_args()
 records=json.loads(SOURCE.read_text(encoding='utf-8'))['records']
 found=[(i,r) for i,r in enumerate(records) if r['id']=='speaker:'+a.speaker]
 if not found:raise SystemExit('Unknown speaker')
 i,r=found[0];spec=compile_record(r,i)
 dest=Path(a.out);dest.mkdir(parents=True,exist_ok=True)
 path=dest/(a.speaker+'-chatgpt-brief.md')
 path.write_text(brief(spec,a.verified_reference),encoding='utf-8')
 print(path)
if __name__=='__main__':main()
