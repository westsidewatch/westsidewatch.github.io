import { isCorePhase } from './city-lifecycle-projection.js';
import { mountJerusalemThreeScene } from './three-scene.js';
import { HistoricalTimeEngine } from './historical-time-engine.js';
import { RuinTransformationEngine } from './ruin-transformation-engine.js';
import { loadTemporalCityIntegration } from './temporal-city-integration.js';
import { auditProductionReadiness } from './production-readiness.js';
import { auditProductionCompletion } from './production-completion-audit.js';
const stage = document.querySelector('.j3k-stage'),
  mount = document.querySelector('[data-three-stage]'),
  badge = document.querySelector('.j3k-terrain-badge');
window.__JERUSALEM3000__ = {
  status: 'booting',
  three: false,
  timeline: false,
  evidence: false,
  timeEngine: false,
  ruinEngine: false,
  temporalCity: false,
  inheritance: false,
  inheritanceError: null,
  productionReady: false,
  complete: false,
  error: null,
};
try {
  const response = await fetch('./data/continuous-build-timeline.json', {
    cache: 'no-store',
  });
  if (!response.ok) throw new Error(`timeline ${response.status}`);
  const timeline = await response.json(),
    phases = timeline.phases;
  if (!Array.isArray(phases) || phases.length !== 18)
    throw new Error('timeline must contain 18 canonical phases');
  const time = new HistoricalTimeEngine(phases),
    ruin = new RuinTransformationEngine(phases),
    temporalCity = await loadTemporalCityIntegration(phases);
  if (!time.reversibleCheck())
    throw new Error('historical time engine failed reversibility check');
  if (!ruin.reversibleCheck())
    throw new Error('ruin transformation engine failed reversibility check');
  window.__JERUSALEM3000__.timeline = true;
  window.__JERUSALEM3000__.timeEngine = true;
  window.__JERUSALEM3000__.ruinEngine = true;
  window.__JERUSALEM3000__.temporalCity = true;
  const slider = document.querySelector('.j3k-scrubber'),
    play = document.querySelector('.j3k-play'),
    date = document.querySelector('.j3k-phase-date'),
    eraEn = document.querySelector('.j3k-era-en'),
    eraZh = document.querySelector('.j3k-caption h2'),
    note = document.querySelector('.j3k-era-note');
  const markers = [...document.querySelectorAll('.j3k-markers button')],
    strip = document.querySelector('.j3k-phase-strip');
  phases.forEach(() => strip.append(document.createElement('i')));
  const ticks = [...strip.children];
  const three = mountJerusalemThreeScene(mount, {
    onReady(info) {
      window.__JERUSALEM3000__.three = true;
      window.__JERUSALEM3000__.evidence = true;
      window.__JERUSALEM3000__.evidenceObjects = info;
      stage.dataset.threeRuntime = 'ready';
      badge.textContent = `THREE.JS · ORBIT READY · ${info.renderableObjects} EVIDENCE OBJECTS`;
    },
  });
  await three.ready;
  let inheritance = null,
    inheritedPhase = '';
  try {
    const module = await import('./phase2-inheritance-runtime.js');
    inheritance = module.createInheritanceLayer(three.root);
    window.__JERUSALEM3000__.inheritance = true;
    stage.dataset.inheritance = 'ready';
  } catch (error) {
    console.error('[Jerusalem 3000 inheritance]', error);
    window.__JERUSALEM3000__.inheritance = false;
    window.__JERUSALEM3000__.inheritanceError = String(error?.stack || error);
    stage.dataset.inheritance = 'disabled';
  }
  function update(v) {
    const state = time.sample(v),
      p = state.phase,
      herodian = time.herodianVisibility(v),
      transformation = ruin.sample(v),
      cityObjects = temporalCity.sample(state.position),
      citySummary = temporalCity.summary(state.position),
      localProgress = Math.max(0, Math.min(1, state.position - state.index));
    three.setBuildProgress(
      isCorePhase(p.id) ? 1 : Math.max(herodian, transformation.standing),
    );
    three.setRuinProgress(transformation.ruin);
    three.setTemporalCityState?.(cityObjects, state.position, p.id);
    if (inheritance) {
      try {
        inheritance.setVisible(!isCorePhase(p.id));
        if (!isCorePhase(p.id)) {
          if (inheritedPhase !== p.id) {
            inheritance.setPhase(p.id, localProgress);
            inheritedPhase = p.id;
          } else inheritance.setProgress(p.id, localProgress);
        }
      } catch (error) {
        console.error('[Jerusalem 3000 inheritance update]', error);
        window.__JERUSALEM3000__.inheritance = false;
        window.__JERUSALEM3000__.inheritanceError = String(
          error?.stack || error,
        );
        stage.dataset.inheritance = 'disabled';
        try {
          inheritance.dispose?.();
        } catch {}
        inheritance = null;
      }
    }
    window.__JERUSALEM3000__.historicalTime = {
      position: state.position,
      phase: p.id,
      continuity: state.cityContinuity,
      herodianVisibility: herodian,
      destruction: transformation.destruction,
      standing: transformation.standing,
      ruin: transformation.ruin,
      transformationPhase: transformation.phase,
    };
    window.__JERUSALEM3000__.temporalCityState = {
      phase: p.id,
      objects: cityObjects,
      summary: citySummary,
    };
    window.__JERUSALEM3000__.inheritanceState = {
      phase: p.id,
      active: !isCorePhase(p.id) && !!inheritance?.runtime,
      progress: localProgress,
    };
    date.textContent = p.dateLabel;
    eraEn.textContent = (p.state || '').toUpperCase() + ' · ' + p.dateLabel;
    eraZh.textContent = p.label;
    note.textContent = p.note;
    ticks.forEach((x, i) => {
      x.classList.toggle('is-past', i < state.index);
      x.classList.toggle('is-current', i === state.index);
    });
    markers.forEach((x) =>
      x.classList.toggle('is-active', Number(x.dataset.phase) === state.index),
    );
    stage.dataset.operation = p.state;
    stage.dataset.phase = p.id;
    stage.dataset.transformation = transformation.phase;
    stage.dataset.temporalObjects = String(
      cityObjects.filter((object) => object.visible || object.ruined).length,
    );
    stage.dataset.inheritance =
      !isCorePhase(p.id) && inheritance?.runtime
        ? 'active'
        : window.__JERUSALEM3000__.inheritance
          ? 'ready'
          : 'disabled';
  }
  let raf = 0,
    last = 0;
  function stop() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    last = 0;
    play.textContent = '▶ 建城';
    play.setAttribute('aria-pressed', 'false');
  }
  function frame(t) {
    if (!last) last = t;
    let v = Number(slider.value) + ((t - last) / 1000) * 0.65;
    last = t;
    if (v >= time.max) {
      v = time.max;
      stop();
    }
    slider.value = v;
    update(v);
    if (raf) raf = requestAnimationFrame(frame);
  }
  function start() {
    if (raf) return;
    play.textContent = 'Ⅱ 暫停';
    play.setAttribute('aria-pressed', 'true');
    raf = requestAnimationFrame(frame);
  }
  slider.addEventListener('input', () => {
    stop();
    update(Number(slider.value));
  });
  play.addEventListener('click', () => (raf ? stop() : start()));
  markers.forEach((b) =>
    b.addEventListener('click', () => {
      stop();
      slider.value = b.dataset.phase;
      update(Number(b.dataset.phase));
    }),
  );
  const evidenceToggle = document.querySelector('.j3k-evidence-toggle'),
    panel = document.querySelector('.j3k-evidence-panel');
  evidenceToggle.addEventListener('click', () => {
    const open = panel.hasAttribute('hidden');
    panel.toggleAttribute('hidden', !open);
    evidenceToggle.setAttribute('aria-expanded', String(open));
  });
  const evidenceModes = [...document.querySelectorAll('[data-evidence-mode]')];
  evidenceModes.forEach((button) =>
    button.addEventListener('click', () => {
      const mode = button.dataset.evidenceMode;
      three.setEvidenceMode(mode);
      stage.dataset.evidenceMode = mode;
      evidenceModes.forEach((item) =>
        item.classList.toggle('is-active', item === button),
      );
      window.__JERUSALEM3000__.evidenceMode = mode;
    }),
  );
  const route = document.querySelector('.j3k-route-toggle');
  route.addEventListener('click', () => {
    const on = !stage.classList.contains('route-on');
    stage.classList.toggle('route-on', on);
    route.setAttribute('aria-pressed', String(on));
    if (on) {
      stop();
      slider.value = 8;
      update(8);
    }
  });
  three.setEvidenceMode('all');
  stage.dataset.evidenceMode = 'all';
  window.__JERUSALEM3000__.evidenceMode = 'all';
  update(0);
  window.__JERUSALEM3000__.status = 'ready';
  const production = auditProductionReadiness(window.__JERUSALEM3000__);
  window.__JERUSALEM3000__.production = production;
  window.__JERUSALEM3000__.productionReady = production.ok;
  stage.dataset.productionReady = String(production.ok);
  const completion = auditProductionCompletion(
    window.__JERUSALEM3000__,
    timeline,
  );
  window.__JERUSALEM3000__.completion = completion;
  window.__JERUSALEM3000__.complete = completion.ok;
  stage.dataset.complete = String(completion.ok);
  badge.textContent = `JERUSALEM 3000 · TEMPORAL CITY · ${production.evidenceObjects || 0} EVIDENCE OBJECTS · ${production.constructionPieces || 0} PIECES`;
  window.addEventListener(
    'pagehide',
    () => {
      try {
        inheritance?.dispose?.();
      } catch {}
    },
    { once: true },
  );
} catch (error) {
  console.error('[Jerusalem 3000 core runtime]', error);
  window.__JERUSALEM3000__.status = 'error';
  window.__JERUSALEM3000__.productionReady = false;
  window.__JERUSALEM3000__.complete = false;
  window.__JERUSALEM3000__.error = String(error?.stack || error);
  stage.dataset.threeRuntime = 'error';
  stage.dataset.productionReady = 'false';
  stage.dataset.complete = 'false';
  badge.textContent = '3D CORE RUNTIME ERROR';
  if (!window.__JERUSALEM3000__.three)
    mount.innerHTML =
      '<div class="j3k-runtime-error">Three.js core runtime failed to start. Check console.</div>';
}
