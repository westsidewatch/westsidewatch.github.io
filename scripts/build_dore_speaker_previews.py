#!/usr/bin/env python3
"""Doré speaker preview design compiler v0.
Deterministic editorial SVG preview + explicit full production prompt and manifest.
No portraits or invented biographical claims. No paid API. Never edits live Olive.
"""
import argparse,json,hashlib,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data/westside-core/entities/sermon-speakers.v1.json'
PALETTE={'paper':'#FFFFFF','ink':'#174B35','secondary':'#47735E'}
MOTIFS=['olive-branches','scripture-pages','stone-arch','mountain-light','courtyard','open-book']
FAMILIES=['asymmetric-editorial','negative-space','vertical-monument','architectural-frame']
def compile_record(record,index):
    slug=record['id'].split(':',1)[1]
    motif=MOTIFS[index%len(MOTIFS)];family=FAMILIES[index%len(FAMILIES)]
    spec={'schema':'dore.speaker-cover.v0','speakerId':record['id'],'slug':slug,'displayName':record['name'],
      'subtitle':(record.get('aliases') or ['OLIVE MOUNTAIN'])[0],
      'status':'PREVIEW_NOT_PUBLISHED','portraitAllowed':False,'portraitAsset':None,
      'section':'olive','canvas':{'width':720,'height':960,'ratio':'3:4'},
      'palette':PALETTE,'motif':motif,'family':family,'ordinal':index+1,
      'typography':{'display':'site-approved Chinese serif','latin':'Bodoni Moda regular','syntheticBold':False},
      'print':{'authority':'vendor/mono-color-skill','techniques':['controlled ink density','paper knockout','fine print linework'],'engraving':'experimental-not-required'},
      'layout':{'safeMargin':48,'nameBaseline':800,'headerBaseline':92,'artBounds':[48,155,624,540]}}
    scenes={
      'olive-branches':'An old olive tree on a stony hillside, gnarled trunk with intricate bark, branches extending asymmetrically into generous white sky, botanical plate detail.',
      'scripture-pages':'An open antique Bible resting on a carved wooden reading stand, pages and wood grain rendered with meticulous fine lines; no readable letters.',
      'stone-arch':'A sunlit limestone archway and worn stone steps in a quiet ancient courtyard, strong architectural perspective and distinct masonry joints.',
      'mountain-light':'Layered Judean limestone hills under a wide white sky, terraced slopes and sparse olive groves, finely hatched geological strata.',
      'courtyard':'A small Mediterranean stone courtyard with a single olive tree and an empty stone bench, archway receding in correct perspective.',
      'open-book':'A weathered open book on a plain wooden table beside an olive branch, paper edges, wood grain and cast shadows in precise engraving.'
    }
    spec['prompt']=(
      'Use a verified, rights-cleared reference photograph for a recognizable speaker portrait when one is supplied. Preserve identity and facial geometry. Otherwise use the non-portrait editorial scene specified below. '
      'Never invent a speaker likeness without a verified reference. No writing, text, letters, signatures or typography. '
      +scenes[motif]+' '
      'Composition: one clear foreground subject with a secondary background plane, strong asymmetric negative space, '
      'legible structural perspective, crisp contour boundaries, close parallel crosshatching with varied spacing to model form. '
      'Traditional copperplate etching on pure white paper with dark olive green ink only. '
      'NO sepia, orange, ochre, tan, beige, gold, red, blue, black, photographic skin tones, blurred photography, '
      'glowing gradient, vignette, soft focus, anonymous invented face, or 3D render. '
      'Keep main visual interest in the upper three quarters, with lower quarter empty white for later type composition. '
      'Image background only; no graphic frame or type. High-resolution sharp printmaking illustration.'
    )
    return spec
def motif_svg(motif):
    # Vector structural illustrations; decorative only, never impersonation.
    if motif in ('stone-arch','architectural-frame','courtyard'):
        return '<path d="M170 650V325Q170 210 360 210Q550 210 550 325V650M222 650V345Q222 265 360 265Q498 265 498 345V650M155 650H565" stroke-width="7"/>'+''.join(f'<path d="M{180+i*19} 645l90 -245" stroke-width=".9"/>' for i in range(18))
    if motif in ('scripture-pages','open-book'):
        return '<path d="M360 650Q230 570 120 625V300Q245 255 360 340Q475 255 600 300V625Q480 570 360 650V340" stroke-width="5"/>'+''.join(f'<path d="M{145 if i%2 else 385} {360+i*22}h170" stroke-width="1.3"/>' for i in range(11))
    if motif=='mountain-light':
        return '<path d="M65 650L270 325L355 460L475 250L660 650Z" stroke-width="5"/>'+''.join(f'<path d="M360 210L{80+i*75} 560" stroke-width=".8"/>' for i in range(8))
    return '<path d="M355 680V300M355 430Q250 280 145 345M355 505Q465 330 590 380M355 585Q240 440 135 510M355 340Q430 230 550 260" stroke-width="5"/>'+''.join(f'<ellipse cx="{180+(i%4)*108}" cy="{315+(i//4)*92}" rx="30" ry="12" transform="rotate(-35 {180+(i%4)*108} {315+(i//4)*92})" stroke-width="1.8"/>' for i in range(12))
def svg(spec):
    ink=spec['palette']['ink'];name=html.escape(spec['displayName']);sub=html.escape(spec['subtitle']);n=spec['ordinal']
    # Deterministic typography is separate from illustration; no synthetic identity portraits.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 960" width="720" height="960" role="img" aria-label="{name} speaker preview">
<rect width="720" height="960" fill="#FFFFFF"/>
<g fill="none" stroke="{ink}" stroke-linejoin="round" stroke-linecap="round">{motif_svg(spec['motif'])}</g>
<path d="M48 735H672M48 885H672" stroke="{ink}" stroke-width="1"/>
<g fill="{ink}"><text x="48" y="91" font-family="Georgia,serif" font-size="31" letter-spacing="1">OLIVE MOUNTAIN</text>
<text x="672" y="91" text-anchor="end" font-family="Georgia,serif" font-size="21">{n:02d}</text>
<text x="48" y="807" font-family="Noto Serif TC,serif" font-size="74">{name}</text>
<text x="48" y="857" font-family="Georgia,serif" font-size="23" letter-spacing="2">{sub}</text>
<text x="48" y="922" font-family="Georgia,serif" font-size="15" letter-spacing="3">SERMONS / PEOPLE</text></g></svg>\n'''
def build(out):
    records=json.loads(SOURCE.read_text(encoding='utf-8'))['records']
    if len(records)!=12:raise ValueError('Expected 12 canonical speakers')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for i,r in enumerate(records):
        s=compile_record(r,i);image=svg(s)
        (out/(s['slug']+'.svg')).write_text(image,encoding='utf-8')
        s['svgSha256']=hashlib.sha256(image.encode()).hexdigest()
        manifest.append(s)
    (out/'manifest.json').write_text(json.dumps({'schema':'dore.speaker-previews.v0','published':False,'records':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    cards=''.join(f'<figure><img src="{html.escape(s["slug"])}.svg" alt="{html.escape(s["displayName"])}"/><figcaption>{html.escape(s["displayName"])}</figcaption></figure>' for s in manifest)
    (out/'index.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Speaker Previews</title><style>body{margin:0;padding:3vw;background:#fff;color:#174b35;font-family:serif}h1{font-weight:400}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:22px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px 0}</style><h1>Olive Mountain / 12 speaker cover proofs</h1><p>Isolated generator previews. Not published speaker portraits.</p><div class="grid">'+cards+'</div></html>',encoding='utf-8')
    print('Generated',len(manifest),'covers at',out)
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='static/dore-design/speaker-generator-v0');a=p.parse_args();build(a.out)
if __name__=='__main__':main()
