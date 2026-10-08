"""Italian editorial portrait art-direction recipes.

Portrait identity comes from a supplied verified reference, never from text alone.
The model generates the art layer only; HTML/CSS owns typography.
"""
PORTRAIT_RECIPES={
 'face-fragment':{
  'title':'Overscale facial fragment',
  'direction':'Enlarge the head beyond normal portrait scale. Let hair, one ear or the outer cheek exit the top or lateral crop. Keep BOTH eyes, nose and mouth sufficiently visible to preserve likeness. The jaw and shoulder become bold abstract shapes. Leave one continuous white field on the opposite side. No decorative background.',
  'identity_safe':'eyes, nose, mouth, characteristic facial proportions',
  'crop':'hair or outer cheek; never crop away the entire eye line'
 },
 'shoulder-sculpture':{
  'title':'Sculptural shoulder and collar',
  'direction':'Use an off-axis three-quarter portrait. Oversize the collar and shoulder until they become a diagonal ink mass entering the CSS title corridor. Keep the face clear and smaller relative to the striking garment geometry. Use paper-white cutouts inside the garment mass to create a graphic silhouette.',
  'identity_safe':'full face, hairline and expression',
  'crop':'outer shoulder, garment and lower torso'
 },
 'silhouette-interruption':{
  'title':'Interrupted profile silhouette',
  'direction':'Build the image around the person’s verified profile contour. Crop the torso hard against one vertical edge; keep the facial profile fully legible. Alternate solid olive shapes and precise halftone/engraved interior details. White paper should interrupt the ink masses in deliberate geometric channels.',
  'identity_safe':'forehead, nose bridge, lips, chin and hairstyle',
  'crop':'back of head only if profile remains recognizable; shoulder and torso'
 },
 'two-scale-portrait':{
  'title':'Close portrait versus small contextual object',
  'direction':'Make the verified face a monumental close-up, cropped along the top and one side. Add at most ONE small subject-relevant object in the distance, with a large unprinted field between scales. Never default to a city skyline, olive branch or decorative frame. Context must be grounded in editorial subject matter.',
  'identity_safe':'eyes, nose, mouth, proportions',
  'crop':'hair and outer garment, not central facial landmarks'
 }
}
def portrait_direction(name,recipe,verified):
 p=PORTRAIT_RECIPES[recipe]
 if not verified:
  return ('PORTRAIT REFERENCE GATE: no verified reference is attached. This is a portrait design specification, '
          'NOT authorization to invent a face for '+name+'. Hold the identity-bearing render until a verified reference '
          'is provided; produce a non-identifying composition proof only.')
 return ('PORTRAIT ART DIRECTION: '+p['title']+'. '+p['direction']+
         ' Preserve identity-critical features: '+p['identity_safe']+
         '. Allowed crop: '+p['crop']+
         '. Transform the actual verified photograph into editorial printed art; do not change age, facial proportions, '
         'hairline or expression. The image contains no text. Use the site-approved ink palette.')
