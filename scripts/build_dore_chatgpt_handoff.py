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
CROP_SYSTEM={
 'asymmetric-editorial':('Editorial off-axis portrait crop','Primary subject may cross the left or top image boundary; crop decisively rather than shrinking it to fit. Place the visual center at x≈34%, y≈42%; keep x≈65–94% comparatively quiet. Let the cropped foreground be a deliberate editorial gesture.'),
 'negative-space':('Large architectural negative-space field','Subject occupies roughly 48–60% of the picture, with 30–40% continuous quiet paper or sparsely etched atmosphere. Negative space is a designed shape, not an accidental blank white bar.'),
 'vertical-monument':('Monumental vertical crop','A tall architectural or organic element runs beyond the top crop; cut at least one secondary edge with intention. Emphasize a single vertical axis and contrast it against generous lateral whitespace.'),
 'architectural-frame':('Partial frame and interrupted geometry','Use an arch, doorway or tree canopy as an incomplete frame, visibly cropped by one image edge. Do not enclose everything in a centered symmetrical border; preserve off-axis depth and editorial tension.')
}
COLOR_APPLICATION=(
 'Treat color as printed material and spatial hierarchy, not a universal filter. '
 'Deep olive #174B35 carries the foreground structural contours and the darkest crosshatched shadows. '
 'Secondary olive #47735E is optional and only for selected midground marks, never a broad wash. '
 'White #FFFFFF is an active paper knockout: it forms highlights, air, breathing room and the light-facing side of forms. '
 'Create depth through density, scale and spacing of green marks, not by adding brown/gray/sepia or generic photographic gradients. '
 'Keep some regions almost untouched white while concentrating the darkest olive in one deliberate focal mass. '
 'No continuous beige paper tint, no gold highlights, no black strokes, no monochrome photographic green tint.'
)
\nEDITORIAL_DIRECTOR={
 'asymmetric-editorial':(
  'EXTREME OFF-CANVAS CROP / 01',
  'Make the subject occupy 130–160% of the frame width, so the image edge physically cuts through the subject. Only one striking fragment is visible; do not show a complete conventional bust or whole object. Put the principal mass in the lower-left 55%, leaving a huge uninterrupted upper-right white field. No background city, tree canopy or decorative framing unless essential to the main subject.',
  'The asymmetry should feel intentionally unfinished, with visual tension between overscale detail and white space.'
 ),
 'negative-space':(
  'EDITORIAL SILENCE / 02',
  'Allocate 55–65% of the image to almost untouched white. Compress a sharply detailed subject into a narrow vertical strip along the right edge, cropped off-canvas. A few detached contour lines may bridge the empty field, but do not fill it with scenic detail.',
  'One image element must carry the entire narrative; absence is a positive compositional shape.'
 ),
 'vertical-monument':(
  'MONUMENTAL FRAGMENT / 03',
  'Use an extreme low-angle crop of one sculptural element; the form enters from below and disappears above the frame. Its shadow occupies a single deep olive wedge. Keep the left third white. Do not add a conventional horizon or symmetrical background.',
  'The design is a collision between one oversized vertical mass and precise open paper.'
 ),
 'architectural-frame':(
  'INTERRUPTED FRAME / 04',
  'A giant partial stone arch enters from the upper left and is severed by the canvas. Show only 40–55% of its outline; through it reveal a small, distant scene positioned unusually low and right. Preserve a large clean field between the two scales.',
  'Architecture acts as editorial cropping machinery, not as decorative scenery.'
 )
}
\ndef brief(spec,has_reference):
 subject,composition=SCENES[spec['motif']]\n crop_name,crop_direction=CROP_SYSTEM[spec['family']]\n concept,blocking,tension=EDITORIAL_DIRECTOR[spec['family']]
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
Deliverable: ONE text-free 3:4 editorial ILLUSTRATION ASSET, ideally 1440 × 1920 pixels or higher. The website renders all typography via HTML/CSS.

## 1. Creative authority
You are executing a finished art-director specification, not inventing a new brand. Produce an actual high-quality image, not SVG placeholder geometry, a mockup photographed on a desk, or an explanation of what you would generate. The target is a credible Italian editorial magazine cover with the physical sophistication of a carefully printed engraved illustration.

## 2. Identity and visual subject
{identity}
Editorial scene alternative (use only if it supports the mandatory crop concept): {subject}.
Exact scene direction: {composition}
Subject matter is Christian sermon editorial content. No unrelated religious iconography or spiritualist motifs. Do not add unsupported biographical facts or sermon titles.

## 2A. Non-negotiable editorial concept / layout blocking
Concept: {concept}
Shot and crop instruction: {blocking}
Intended visual tension: {tension}
This is NOT a historical illustration commission. Do not use the safe composition of a centered portrait with a picturesque background, an olive branch in the corner, or a scenic skyline. Reject the previous repeated portrait-left/city-right/tree-top arrangement. Produce a visually surprising magazine image asset, not a commemorative church poster. The composition should still work after CSS typography is added.
Prioritize this spatial blocking over decorative subject matter; remove secondary objects rather than diluting the layout.

## 3. Art direction and spatial composition
Canvas 3:4, upright. Use a confident asymmetrical editorial composition, not centered clip art. Establish a clear foreground, secondary midground and restrained background. One strong focal point visible even as a small thumbnail. Preserve a clean title zone with enough actual negative space for type. Allow the illustration to breathe; do not place a rectangular photo in a generic card. At least 48px-equivalent edge safety on a 720px design width.
Top 10%: quiet image detail or negative space; the masthead is rendered later by CSS.
Middle 12–72%: principal illustration; vary line density to guide attention.
Bottom 75–95%: preserve natural image negative space suitable for an HTML/CSS title overlay, not a baked-in blank rectangle.
Bottom 5%: image continuation or paper white; the edition line is rendered later by CSS.
No overlapping text, no clipped characters, no arbitrary dividers.

## 3A. Doré editorial cropping and negative-space grammar
Composition family: {spec['family']} — {crop_name}.
Exact crop directive: {crop_direction}
The image is NOT an illustration centered within a fixed box. Permit meaningful edge cropping, foreground scale shifts, interruptions and asymmetrical tension. Design for the eventual CSS text overlay: reserve a calm area with enough local contrast but do not create a fake white title panel. The HTML layer will decide exact type positions and responsive line breaks.
For mobile crop safety, the main subject must remain readable when the center 80% of the image width is shown; important facial landmarks (if a verified portrait is provided) must not be clipped. Keep the image compelling both full-bleed and in a narrower card.

## 3B. Color as material and visual hierarchy
{COLOR_APPLICATION}
Use a deliberate color-density map: 65–75% visually light paper or lightly etched atmosphere; 15–25% mid-density olive markwork; 5–12% concentrated deep-olive focal darks. These are art-direction targets, not a demand for flat pixel fills. Shadows should reveal etched lines and white channels even in dense regions.
The artwork must have no default brown/yellow aged-paper background. Avoid covering the entire picture with olive tint. Let the white paper itself carry light and editorial space.

## 4. Engraving and physical printing
Use detailed etched/copperplate engraving language: precise contour lines, short directional hatches following form, deliberate crosshatching only in deeper shadows, and untouched white paper for light. Distinguish wood grain, stone grain, foliage, hair and fabric with material-specific linework. Rich tonal hierarchy must come from controlled ink density and paper knockout, not photographic blur, muddy gradients, synthetic grain or crude halftone dots. Avoid pseudo-engraving filters, thick cartoon outlines, crude green circles, flat stock vector graphics and generic symmetrical ornament.

## 5. Strict palette
White paper #FFFFFF, deep olive ink #174B35; optional supporting olive #47735E only if needed. No gold, black-gold, sepia, tan, beige, ochre, orange, blue, magenta or default blue hyperlinks. The final picture should read as green ink on clean white paper, including any rendered face.

## 6. Strict separation: image asset versus HTML/CSS typography
Generate NO typography of any kind: NO Chinese characters, NO Latin letters, NO numerals, NO headings, NO logo, NO captions, NO dividers, NO watermark. All text, including the Chinese speaker name, English name, masthead, labels and decorative rules, belongs to the website's HTML/CSS overlay. The image must remain useful with no lettering at all.
Site typography authority for the separate CSS layer: English Bodoni Moda Regular 400; Chinese display Chiron Hei (昭源黑體); Chinese long-form reading Noto Serif TC. Do not draw, imitate or rasterize any of these fonts into the image.
Do not produce a poster with an empty white title card glued onto the lower portion. Keep a coherent full-frame illustration with intentional natural negative space that can support responsive text placement.

## 7. Negative constraints
No anonymous fake speaker portraits, no identity swapping, no face melting, no distorted eyes or hands, no blurry faces, no low-resolution painting, no orange flesh-tone image, no cheap poster templates, no blocky geometry, no generated writing of any language, no random religious symbols, no watermark.

## 8. Acceptance criteria
A. Recognizable likeness ONLY when a verified reference is actually supplied; otherwise no claimed portrait identity.
B. Crisp linework and coherent materials at full resolution and thumbnail size.
C. Olive-and-white print palette throughout.
D. Zero text or typographic marks in the generated image; all lettering is delegated to HTML/CSS.
E. Purposeful asymmetric crop, meaningful continuous negative space, controlled olive ink density, and no hard white paste-over strip.
F. This is a design proof; do not publish or silently substitute assets.

## 9. Output instruction
Generate only the text-free illustration now. Make one deliberate, finished composition. If a supplied portrait reference is absent, execute the still-life alternative without asking the user to fabricate a likeness. Return the image for visual review.
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
