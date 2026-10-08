#!/usr/bin/env python3
"""Compile an explicit Italian editorial image+CSS layout brief without paid services."""
import argparse,json
from pathlib import Path
from dore_editorial_portrait_recipes import PORTRAIT_RECIPES, portrait_direction
from dore_editorial_scenarios import SCENARIOS,SLOTS,scene_direction

RECIPES={
 'overscale-collision':{
  'idea':'Overscale subject collides with a giant live vertical headline',
  'subject_box':[-10,15,115,115],'type_box':[0,0,22,100],
  'negative_space':[22,3,55,32],'crossing_box':[0,65,22,100],
  'crop_edges':['right','bottom'],'mobile_subject_box':[20,8,120,105],
  'art_direction':'Make the main subject larger than the frame. Cut it off at the right and bottom. Preserve upper-left paper white. Allow the lower-left subject to enter the future CSS headline lane.'
 },
 'quiet-field':{
  'idea':'A solitary sharply rendered fragment against dominant active paper',
  'subject_box':[67,35,105,90],'type_box':[7,8,56,65],
  'negative_space':[7,4,65,80],'crossing_box':[45,55,72,75],
  'crop_edges':['right'],'mobile_subject_box':[50,30,112,94],
  'art_direction':'Keep more than half the composition visually quiet. Compress one subject against the right crop. No ornamental fillers or generic scenery.'
 },
 'monumental-interruption':{
  'idea':'One monumental fragment severed by the page boundary',
  'subject_box':[-20,-25,75,120],'type_box':[70,5,100,95],
  'negative_space':[75,8,100,82],'crossing_box':[67,65,82,88],
  'crop_edges':['top','bottom','left'],'mobile_subject_box':[-5,-15,95,115],
  'art_direction':'Show a single oversized structural form crossing the top and bottom crop; do not show the entire facade or centered monument.'
 },
 'two-scale-encounter':{
  'idea':'Extreme near/far scale conflict separated by deliberate whitespace',
  'subject_box':[-20,25,58,115],'secondary_box':[72,42,90,63],
  'type_box':[38,10,72,60],'negative_space':[45,5,80,40],
  'crossing_box':[40,58,60,78],'crop_edges':['left','bottom'],
  'mobile_subject_box':[-10,25,85,110],
  'art_direction':'Place an oversized foreground form against a tiny distant subject. Leave the space between them unfilled. Avoid conventional landscape depth.'
 }
}
PALETTES={'olive-mountain':{'paper':'#FFFFFF','image_ink':'#174B35','secondary_ink':'#47735E','type_ink':'#174B35'}}
def compile_brief(args):
 recipe=RECIPES[args.recipe]
 portrait_style=getattr(args,'portrait_style','none')
 scenario=getattr(args,'scenario','essay-concept')
 slot=getattr(args,'slot','cover')
 scene=scene_direction(scenario,slot)
 portrait_note=portrait_direction(args.subject,portrait_style,args.verified_reference) if portrait_style!='none' else ''
 palette=PALETTES[args.palette]
 spec={'version':1,'subject':args.subject,'recipe':args.recipe,'composition':recipe,
       'palette':palette,'material':args.material,'verified_reference':args.verified_reference,
       'scenario':scenario,'slot':slot,'slot_spec':SLOTS[slot],'scenario_spec':SCENARIOS[scenario], 'portrait_style':portrait_style,'portrait_reference_required':portrait_style!='none','output':'text-free illustration only','publication_approved':False}
 identity=('A verified and authorized visual reference will be supplied in the SAME image-generation request; preserve its identity without inventing features.' if args.verified_reference else 'No verified visual reference is supplied. Do not claim an invented face represents a named person; use a symbolic or non-portrait subject.')
 material={'halftone':'Use physically credible variable-size offset halftone dots, dense in shadow, sparse in light, with white paper knockouts and crisp solid-ink shapes.',
 'engraving':'Use precise directional contour hatching and crosshatching following material form; white paper provides highlights. No blurred pseudo-engraving.',
 'cutout':'Use sharply cut silhouettes with limited ink roles and precise edge rhythm; no decorative gradients.'}[args.material]
 prompt=f"""Generate ONE sophisticated text-free editorial illustration. Target aspect ratio: {SLOTS[slot]['ratio']}.
SUBJECT: {args.subject}
{scene}
IDENTITY: {identity}
VISUAL PROPOSITION: {recipe['idea']}.
PORTRAIT-SPECIFIC DIRECTION: {portrait_note}
GEOMETRY (normalized image coordinates, 0–100; allow boxes to extend beyond canvas):
Main subject box: {recipe['subject_box']}.
Future live CSS text box: {recipe['type_box']}.
Future deliberate text/image crossing zone: {recipe['crossing_box']}.
Contiguous negative-space region: {recipe['negative_space']}.
Crop subject at these canvas boundaries: {', '.join(recipe['crop_edges'])}.
COMPOSITION DIRECTIVE: {recipe['art_direction']}
Do not shrink the subject to fit. Negative space is an intentional visual shape, not a pasted-on title bar.
MATERIAL: {material}
INK ROLES: White paper {palette['paper']} is active negative space and highlights. Primary image ink {palette['image_ink']} controls the darkest contours and masses. Secondary {palette['secondary_ink']} is optional and restricted to sparse midtones. Do not use any other hue, aged-paper tint, or universal color filter.
TYPE CONTRACT: Image contains absolutely NO text, glyphs, logos, numerals, labels or decorative rules. CSS will later draw the editorial headline in the specified text box, on top of the image at the crossing zone. Preserve the visual subject's identity-bearing features outside that crossing zone.
SCENARIO-SPECIFIC SAFETY: A named real person's recognizable portrait requires a verified and authorized reference image supplied with the generation request. Never fabricate their face; if absent, generate only a non-identifying visual proof. Respect the subject-specific cautions above.
MOBILE: Keep focal features recognizable in a narrow crop approximated by {recipe['mobile_subject_box']}; the CSS layout may reposition text.
REJECT: centered stock illustration, generic poster, photo with a white footer bar, invented speaker face, ornamental filler, muddy gradients, poor edge detail, illegible embedded text, unrelated color, and symmetrical framing.
DELIVERABLE: one complete high-resolution illustration asset, no typography, for separate responsive CSS composition. Do not publish automatically.
"""
 css=f"""# Live CSS composition contract
- Canvas: portrait 3:4, normalized percentage coordinates.
- Recipe: {args.recipe}; idea: {recipe['idea']}
- Scenario: {scenario}; output slot: {slot}, aspect ratio: {SLOTS[slot]['ratio']}.
- Slot layout policy: {SLOTS[slot]['css']}
- Headline box: {recipe['type_box']} [left, top, right, bottom].
- Crossing box: {recipe['crossing_box']}; type above image in this region.
- Negative-space region: {recipe['negative_space']}.
- Site typography: English Bodoni Moda Regular 400, Chinese display Chiron Hei; Chinese reading Noto Serif TC.
- Render all text as accessible HTML/CSS, never in generated image.
- Recompute title scale, rotation, collision and subject crop for mobile; check at 320, 375, 768 and 1440 CSS pixels.
- Forbid clipping critical facial landmarks; require visual editorial review before publication.
"""
 return spec,prompt,css
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--subject',required=True)
 p.add_argument('--recipe',choices=RECIPES,default='overscale-collision')
 p.add_argument('--material',choices=['halftone','engraving','cutout'],default='halftone')
 p.add_argument('--palette',choices=PALETTES,default='olive-mountain')
 p.add_argument('--verified-reference',action='store_true')
 p.add_argument('--portrait-style',choices=['none']+list(PORTRAIT_RECIPES),default='none')
 p.add_argument('--scenario',choices=SCENARIOS,default='essay-concept')
 p.add_argument('--slot',choices=SLOTS,default='cover')
 p.add_argument('--route',help='Resolve editorial scenario, slot and palette from a known site route')
 p.add_argument('--content-file',help='Optional Hugo front matter for route-specific design metadata')
 p.add_argument('--out',default='local/dore-editorial-brief')
 args=p.parse_args()
 if args.route:
  from resolve_dore_editorial_page import resolve,parse_frontmatter
  resolved=resolve(args.route,parse_frontmatter(args.content_file) if args.content_file else None)
  args.scenario=resolved['scenario'];args.slot=resolved['slot'];args.palette=resolved['palette']
 spec,prompt,css=compile_brief(args)
 if args.route:spec['page_resolution']=resolved
 out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 for filename,data in [('art-direction.json',json.dumps(spec,ensure_ascii=False,indent=2)+'\n'),('image-prompt.md',prompt),('css-layout-contract.md',css)]:
  (out/filename).write_text(data,encoding='utf-8')
 print(out)
if __name__=='__main__':main()
