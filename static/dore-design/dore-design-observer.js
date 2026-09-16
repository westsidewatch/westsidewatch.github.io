/* Doré Design Observer v1
 * Runtime observation adapter for Design Intelligence.
 * Reads rendered DOM/computed style into observational evidence only.
 * It never grants canonical authority or promotion.
 */
(function (global) {
  'use strict';

  const SAMPLE_LIMIT = 180;
  const COMPONENT_SELECTOR = 'header,nav,main,section,article,aside,footer,button,a,input,textarea,select,[role],[class]';
  const STYLE_KEYS = [
    'display','position','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing',
    'color','backgroundColor','borderRadius','borderWidth','boxShadow','gap','rowGap','columnGap',
    'paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft',
    'gridTemplateColumns','gridTemplateRows','justifyContent','alignItems','textAlign','textTransform','opacity','transform','transition'
  ];

  function uniq(values) { return [...new Set(values.filter(Boolean))]; }
  function round(n) { return Math.round(n * 100) / 100; }
  function visible(el) {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
  }
  function styleOf(el) {
    const cs = getComputedStyle(el); const out = {};
    STYLE_KEYS.forEach(k => { if (cs[k]) out[k] = cs[k]; });
    return out;
  }
  function fact(el, i) {
    const r = el.getBoundingClientRect();
    return {
      ref: `dom:${i}`,
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      classes: [...el.classList].slice(0, 8),
      role: el.getAttribute('role'),
      text: (el.innerText || '').trim().replace(/\s+/g,' ').slice(0,120),
      box: {x:round(r.x), y:round(r.y), width:round(r.width), height:round(r.height)},
      style: styleOf(el)
    };
  }
  function claim(statement, refs, confidence) {
    return {statement, confidence: confidence == null ? 0.9 : confidence, evidenceRefs: refs};
  }
  function derive(facts) {
    const refs = facts.map(x => x.ref);
    const displays = facts.map(x => x.style.display);
    const grids = facts.filter(x => x.style.display === 'grid');
    const flex = facts.filter(x => x.style.display === 'flex');
    const radii = uniq(facts.map(x => x.style.borderRadius));
    const fonts = uniq(facts.map(x => x.style.fontFamily));
    const transitions = facts.filter(x => x.style.transition && x.style.transition !== 'all 0s ease 0s');
    const composition = [];
    const component = [];
    const motion = [];
    if (grids.length) composition.push(claim(`Rendered composition uses CSS grid in ${grids.length} observed elements.`, grids.map(x=>x.ref), 1));
    if (flex.length) composition.push(claim(`Rendered composition uses flex layout in ${flex.length} observed elements.`, flex.map(x=>x.ref), 1));
    if (fonts.length) component.push(claim(`Observed typography uses ${fonts.length} computed font-family stacks.`, refs, 1));
    if (radii.length) component.push(claim(`Observed components expose ${radii.length} distinct computed border-radius values.`, refs, 1));
    if (transitions.length) motion.push(claim(`CSS transitions are present on ${transitions.length} observed elements.`, transitions.map(x=>x.ref), 1));
    return {component, composition, motion, displays};
  }
  function observe(options) {
    options = options || {};
    const nodes = [...document.querySelectorAll(options.selector || COMPONENT_SELECTOR)].filter(visible).slice(0, options.limit || SAMPLE_LIMIT);
    const facts = nodes.map(fact);
    const d = derive(facts);
    const locator = options.locator || location.href;
    return {
      schema: 'dore.design-observation-evidence.v1',
      id: options.id || `observation.runtime.${Date.now()}`,
      source: {kind:'url', locator, capturedAt:new Date().toISOString(), viewport:{width:innerWidth,height:innerHeight}},
      observations: {
        visualFacts: {elements:facts, document:{title:document.title, lang:document.documentElement.lang || null}},
        componentGrammar: d.component,
        compositionGrammar: d.composition,
        editorialGrammar: [],
        motionGrammar: d.motion,
        responsiveBehavior: [],
        inferredRationale: []
      },
      provenance: {evidenceRefs:[locator, ...facts.map(x=>x.ref)], method:['dom','css','computed-style','render'], notes:['Runtime observer records rendered evidence; semantic rationale requires a later evidence-backed inference pass.']},
      authority: {class:'observational-evidence', mayPromoteCanonical:false, requiresBeautifulGate:true, historicalAuthority:false},
      exports: {designMd:true, cssVariables:true, tailwind:true, dtcgTokens:true}
    };
  }
  global.DoreDesignObserver = Object.freeze({version:'1.0.0', observe});
})(window);
