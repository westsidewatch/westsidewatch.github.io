#!/usr/bin/env python3
"""Compile a strict Doré-owned mono-color generation contract; no paid API or network."""
import argparse, json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VENDOR=ROOT/"vendor/mono-color-skill"
PALETTES={
 "olive":{"substrate":"#FFFFFF","inks":["#174B35"],"section":"Olive Mountain"},
 "dawn":{"substrate":"#FFFFFF","inks":["#252525"],"section":"Westside Watch"}
}
def compile_prompt(subject,text,section="olive",ratio="3:4",engraving=True):
    if not subject.strip(): raise ValueError("subject required")
    if section not in PALETTES: raise ValueError("unapproved section")
    if ratio not in ("3:4","4:5","1:1","16:9","9:16"): raise ValueError("unapproved ratio")
    if not (VENDOR/"SKILL.md").is_file(): raise FileNotFoundError("upstream skill missing")
    palette=PALETTES[section]
    catalog=json.loads((VENDOR/'design-system/imperfections.json').read_text(encoding='utf-8'))
    seed=int(hashlib.sha256((subject+'|'+text+'|'+section+'|'+ratio).encode()).hexdigest()[:8],16)
    effects=catalog['effects']; selected=[effects[seed%len(effects)],effects[(seed+1)%len(effects)]]
    recipe={
      "schema":"dore.monocolor.recipe.v1","source":"vendor/mono-color-skill/SKILL.md",
      "subject":subject.strip(),"exactText":text,"section":section,"ratio":ratio,
      "substrate":palette["substrate"],"inks":palette["inks"],
      "typography":{"display":"Bodoni Moda regular","chinese":"approved site Chinese font tokens","noSyntheticBold":True},
      "composition":{"focalEvent":"one decisive subject-led event","negativeSpace":"intentional, not filler","layout":"asymmetric editorial, not repeated cards"},
      "printTexture":{"authority":"vendor/mono-color-skill/design-system/imperfections.json","stableSeed":seed,"effects":selected,"technique":"halftone, controlled ink density and exposed-paper highlights"},
      "engraving":{"enabled":engraving,"status":"experimental","source":"rights-cleared Gustave Doré historical engraving","method":"optional research crosshatching, never replaces Mono Color print techniques"},
      "constraints":["Never introduce colors outside approved palette","No gold, black-gold, or native blue links",
       "No invented identity portraits","Keep supplied text exact","Do not imitate any reference cover",
       "Preserve original website immersive hero and responsive scale","Output original editorial composition, not random geometric blocks"],
      "state":"PROMPT_READY_NOT_RENDERED","publishAllowed":False
    }
    prompt=("\\n".join([
      "Create ONE original professional editorial poster, obey every constraint exactly.",
      "SUBJECT: "+recipe["subject"],"EXACT TEXT: "+(text or "[no text]"),
      "CANVAS RATIO: "+ratio,
      "PALETTE: white "+palette["substrate"]+" and only ink "+", ".join(palette["inks"])+". No other ink.",
      "TYPOGRAPHY: Bodoni Moda regular for Latin display; use the site's approved Chinese font tokens for Chinese. No synthetic bold.",
      "COMPOSITION: one subject-driven focal event, deliberate asymmetric balance, active negative space and precise editorial hierarchy. Do not stack arbitrary circles, stripes or rectangles.",
      "PRINT TEXTURE: mechanical halftone, controlled ink density, exposed-paper highlights; apply upstream effects "+json.dumps(selected,ensure_ascii=False)+" with stable seed "+str(seed)+". Do not distort small text.",
      "EXPERIMENTAL ENGRAVING: "+(recipe["engraving"]["method"]+"; use rights-cleared Doré source." if engraving else "disabled."),
      "SAFETY: no synthetic recognizable portraits, no copied historical artwork, no extra words.",
      "QUALITY: make typography legible and correctly spelled; no default blue links; preserve quiet visual rhythm.",
      "DELIVERABLE: render image only after this complete specification is accepted; compare the actual image against every instruction before approval."
    ]))
    return {"recipe":recipe,"generationPrompt":prompt}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--subject",required=True);p.add_argument("--text",default="")
    p.add_argument("--section",choices=sorted(PALETTES),default="olive")
    p.add_argument("--ratio",default="3:4");p.add_argument("--no-engraving",action="store_true")
    p.add_argument("--prompt-only",action="store_true")
    a=p.parse_args()
    result=compile_prompt(a.subject,a.text,a.section,a.ratio,not a.no_engraving)
    print(result["generationPrompt"] if a.prompt_only else json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
