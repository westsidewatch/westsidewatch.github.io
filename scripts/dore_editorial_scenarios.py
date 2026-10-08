"""Magazine editorial use-case profiles. Scenario != visual recipe != output slot."""
SCENARIOS={
 'speaker':{
  'purpose':'Recognizable sermon speaker identity and editorial authority',
  'subject':'Verified person portrait; preserve likeness, expression, age and hairline',
  'story':'Emphasize facial character and rhetorical presence; no invented sacred symbols or biographical props',
  'preferred_recipes':['overscale-collision','monumental-interruption'],
  'preferred_materials':['engraving','halftone'],
  'portrait_required':True,
  'editorial_warning':'No anonymous generated face may be labelled as the named speaker.'
 },
 'column-author':{
  'purpose':'Recurring author identity that can remain recognizable across a series',
  'subject':'Verified author portrait or approved author-controlled illustration',
  'story':'Build a consistent visual signature across articles; vary crop and negative-space pattern rather than changing identity',
  'preferred_recipes':['quiet-field','overscale-collision'],
  'preferred_materials':['halftone','engraving'],
  'portrait_required':True,
  'editorial_warning':'Preserve the same person across all issues; no fabricated author likeness.'
 },
 'interview-subject':{
  'purpose':'An encounter with a real interviewee, not a generic celebrity portrait',
  'subject':'Verified interviewee portrait with identity-critical facial features unobscured',
  'story':'Use off-axis gaze, spatial tension and a single relevant verified contextual object only if editorially supported',
  'preferred_recipes':['two-scale-encounter','quiet-field'],
  'preferred_materials':['halftone','engraving'],
  'portrait_required':True,
  'editorial_warning':'Do not invent gestures, settings, events or possessions that imply unverified facts.'
 },
 'witness-testimony':{
  'purpose':'Respectful first-person narrative image with appropriate privacy',
  'subject':'Verified portrait only when authorized; otherwise anonymous symbolic illustration',
  'story':'Quiet human scale, deliberate whitespace and emotional restraint; avoid melodramatic stock symbolism',
  'preferred_recipes':['quiet-field','two-scale-encounter'],
  'preferred_materials':['engraving','cutout'],
  'portrait_required':False,
  'editorial_warning':'Do not imply a symbolic figure is the actual testimony subject.'
 },
 'essay-concept':{
  'purpose':'Conceptual illustration expressing the central argument of an essay',
  'subject':'One concrete metaphor or object derived from supplied essay, not generic religious decoration',
  'story':'Exploit extreme scale, paper cutout and structural contrast to make an editorial proposition',
  'preferred_recipes':['monumental-interruption','two-scale-encounter'],
  'preferred_materials':['cutout','engraving'],
  'portrait_required':False,
  'editorial_warning':'Do not introduce a claim or event absent from the essay.'
 },
 'historical-feature':{
  'purpose':'Historical long-form editorial art with traceable reference boundaries',
  'subject':'Verified historical place, object or document; no invented documentary accuracy',
  'story':'Make one archaeological or architectural fragment carry the composition; distinguish reconstruction from evidence',
  'preferred_recipes':['monumental-interruption','quiet-field'],
  'preferred_materials':['engraving','halftone'],
  'portrait_required':False,
  'editorial_warning':'Do not present speculative reconstructed details as verified history.'
 },
 'book-publication':{
  'purpose':'Book and publication cover or catalog visual',
  'subject':'Approved book object, symbolic motif or rights-cleared cover asset',
  'story':'Use book silhouette, crop, physical paper and ink density as graphic structure',
  'preferred_recipes':['overscale-collision','quiet-field'],
  'preferred_materials':['cutout','engraving'],
  'portrait_required':False,
  'editorial_warning':'Do not generate fake readable book titles or falsely attribute editions.'
 },
 'cinema-program':{
  'purpose':'Film programming and visual catalog',
  'subject':'Rights-cleared film still or abstract non-infringing scene motif',
  'story':'Frame like a cinematic fragment; use strong off-screen direction and meaningful dark/light separation',
  'preferred_recipes':['monumental-interruption','two-scale-encounter'],
  'preferred_materials':['halftone','cutout'],
  'portrait_required':False,
  'editorial_warning':'Do not invent film frames or misrepresent them as authentic stills.'
 },
 'section-hero':{
  'purpose':'Immersive magazine section opening with space for large live headings',
  'subject':'One large visual form grounded in section identity',
  'story':'High-impact edge crop and deliberate large quiet region; motion and type belong to web layer',
  'preferred_recipes':['overscale-collision','monumental-interruption'],
  'preferred_materials':['engraving','halftone'],
  'portrait_required':False,
  'editorial_warning':'No generated navigation or title lettering.'
 },
 'archive-thumbnail':{
  'purpose':'Dense archive or index image that remains legible at small size',
  'subject':'Single immediately recognizable visual silhouette',
  'story':'Reduce details, keep strong contour and tonal hierarchy; no microtexture that collapses at thumbnail size',
  'preferred_recipes':['quiet-field','monumental-interruption'],
  'preferred_materials':['cutout','halftone'],
  'portrait_required':False,
  'editorial_warning':'Never claim a thumbnail is an authenticated portrait without source.'
 }
}
SLOTS={
 'cover':{'ratio':'3:4','goal':'large editorial cover with live display typography','image_density':'medium','css':'headline may intentionally overlap subject; protect critical face landmarks'},
 'feature-lead':{'ratio':'4:5','goal':'article lead image with clear subject and controlled text overlay','image_density':'medium-high','css':'reserve a clean headline field but do not paste a white title bar'},
 'inline':{'ratio':'3:2','goal':'reading-flow illustration with deliberate visual pause','image_density':'high','css':'no required overlap; caption outside image in HTML'},
 'profile-card':{'ratio':'4:5','goal':'reusable person identity card','image_density':'medium','css':'keep face readable at narrow card widths; name as HTML below or alongside'},
 'hero':{'ratio':'16:9','goal':'full-width immersive section opening','image_density':'low-medium','css':'reserve major title and navigation safe areas for mobile and desktop'},
 'thumbnail':{'ratio':'1:1','goal':'recognizable tiny index image','image_density':'low','css':'never depend on fine print textures for recognition'}
}
def scene_direction(scenario,slot):
 a=SCENARIOS[scenario];b=SLOTS[slot]
 return (
  'EDITORIAL SCENARIO: '+scenario+'. Purpose: '+a['purpose']+
  '. Subject: '+a['subject']+'. Narrative: '+a['story']+
  '. Editorial caution: '+a['editorial_warning']+
  '. OUTPUT SLOT: '+slot+', aspect '+b['ratio']+
  ', goal: '+b['goal']+', image detail density: '+b['image_density']+
  '. CSS relationship: '+b['css']+
  '. These scenario/slot rules override generic decorative motifs; retain selected composition geometry after adapting it to the specified aspect ratio.'
 )
