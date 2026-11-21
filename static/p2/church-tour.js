/**
 * Westside Watch / P2 — Living Water West virtual church.
 * Independent GitHub-hosted second-layer camera walkthrough.
 * Uses the existing architectural GLB as geometry only; never embeds the
 * growth-maquette application, its renderer, its labels, or ChatGPT Sites.
 */
import {
  t as Group, l as MeshStandardMaterial, M as Mesh,
  y as BoxGeometry, p as Vector3,
  G as GLTFLoader, W as WebGLRenderer, S as SRGBColorSpace,
  A as ACESFilmicToneMapping, P as PCFSoftShadowMap,
  a as Scene, H as HemisphereLight, D as DirectionalLight,
  b as PlaneGeometry, o as PerspectiveCamera, d as DoubleSide
} from "../p2-maquette/assets/GLTFLoader-j388d5bW.js";

const canvas = document.querySelector("#church-canvas");
const prefersReducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const scene = new Scene();
const renderer = new WebGLRenderer({
  canvas, antialias: true, powerPreference: "high-performance", alpha: false
});
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.7));
renderer.outputColorSpace = SRGBColorSpace;
renderer.toneMapping = ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.27;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = PCFSoftShadowMap;
renderer.setClearColor(0xd7d8cf, 1);

// Perspective projection, using the locally bundled Three.js camera.
// Projection is explicitly recalculated on resize rather than depending
// on the maquette's orthographic-camera settings.
const camera = new PerspectiveCamera(59, 1, 0.055, 170);
function resize() {
  const width = Math.max(1, window.innerWidth);
  const height = Math.max(1, window.innerHeight);
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.fov = width < 650 ? 70 : 59;
  camera.updateProjectionMatrix();
}
window.addEventListener("resize", resize, { passive: true });
resize();

scene.add(new HemisphereLight(0xdde8ed, 0x958374, 2.25));
const sun = new DirectionalLight(0xffeccb, 3.4);
sun.position.set(4, 21, 10);
sun.target.position.set(9, 0, -8);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, {
  left: -29, right: 29, top: 29, bottom: -29, near: 0.1, far: 85
});
sun.shadow.normalBias = 0.025;
sun.shadow.radius = 3;
scene.add(sun, sun.target);
const ambientFill = new DirectionalLight(0xc8dce7, 1.1);
ambientFill.position.set(19, 12, -24);
scene.add(ambientFill);
const sanctuaryLight = new DirectionalLight(0xffe3b1, 1.8);
sanctuaryLight.position.set(15.5, 5.1, -1.3);
sanctuaryLight.target.position.set(15, 1.4, -10);
scene.add(sanctuaryLight, sanctuaryLight.target);

const finishes = {
  masonry: new MeshStandardMaterial({ color: 0xcad0c8, roughness: 0.89 }),
  paleStone: new MeshStandardMaterial({ color: 0xe3e5dc, roughness: 0.85 }),
  plaster: new MeshStandardMaterial({ color: 0xe9eae5, roughness: 0.94 }),
  floor: new MeshStandardMaterial({ color: 0xcac2b5, roughness: 0.86 }),
  courtyard: new MeshStandardMaterial({ color: 0xd0cec2, roughness: 0.9 }),
  roof: new MeshStandardMaterial({ color: 0xc4c9c2, roughness: 0.83, metalness: 0.04, side: DoubleSide }),
  glazing: new MeshStandardMaterial({
    color: 0xc3d6d7, roughness: 0.14, metalness: 0.17,
    transparent: true, opacity: 0.22, depthWrite: false, side: DoubleSide
  }),
  mullion: new MeshStandardMaterial({ color: 0x707772, roughness: 0.49, metalness: 0.52 }),
  timber: new MeshStandardMaterial({ color: 0x927254, roughness: 0.75 }),
  joinery: new MeshStandardMaterial({ color: 0x765943, roughness: 0.71 }),
  pew: new MeshStandardMaterial({ color: 0x79593f, roughness: 0.69 }),
  cross: new MeshStandardMaterial({
    color: 0xe6c58c, emissive: 0xb27d38, emissiveIntensity: 0.47,
    roughness: 0.34, metalness: 0.38
  }),
  leaves: new MeshStandardMaterial({
    color: 0x707f62, roughness: 1, side: DoubleSide
  }),
  earth: new MeshStandardMaterial({ color: 0x81927c, roughness: 1 }),
  metal: new MeshStandardMaterial({ color: 0x696e69, roughness: 0.49, metalness: 0.66 }),
  ivory: new MeshStandardMaterial({ color: 0xf2f1eb, roughness: 0.7 }),
  ground: new MeshStandardMaterial({ color: 0xc5c8c0, roughness: 1 })
};

// GLTFLoader sanitizes source node labels into animation-safe identifiers
// (spaces become underscores). Match against normalized source names.
function modelName(value) {
  return String(value).toLowerCase().replace(/[_\\s·.–—]+/g, " ").trim();
}
function chooseFinish(name) {
  const n = modelName(name);
  // SOUTH CROSS WALL consists of four SOLID quadrants surrounding a void.
  // Never make those large wall solids emissive gold.
  if (/south cross wall|solid quadrant/.test(n)) return finishes.plaster;
  if (/cross|crucifix/.test(n)) return finishes.cross;
  if (/glass|glazing|window pane|glazed/.test(n)) return finishes.glazing;
  if (/mullion|window frame|metal frame|railing|handrail/.test(n)) return finishes.mullion;
  if (/roof|skylight surround|roof edge/.test(n)) return finishes.roof;
  if (/pew|pulpit|lectern|table|chair|cafe|bookcase|counter/.test(n)) return finishes.pew;
  if (/tall single white pivot door/.test(n)) return finishes.ivory;
  if (/entrance.*door|door.*entrance|door leaf|door panel/.test(n)) return finishes.joinery;
  if (/door|jamb|threshold|lintel/.test(n)) return finishes.ivory;
  if (/maple|tree|foliage|leaf|shrub|plant/.test(n)) return finishes.leaves;
  if (/ground|grass|soil|site vegetation/.test(n)) return finishes.earth;
  if (/board|plinth|base slab|foundation plate/.test(n)) return finishes.ground;
  if (/courtyard|terrace|step|stair|landing|promenade/.test(n)) return finishes.courtyard;
  if (/floor|paving|tile/.test(n)) return finishes.floor;
  if (/wood|timber|slat|beam/.test(n)) return finishes.timber;
  if (/column|support|metalwork/.test(n)) return finishes.metal;
  if (/outer wall|external wall|perimeter|stone/.test(n)) return finishes.masonry;
  if (/wall|partition|facade|façade|screen|ceiling/.test(n)) return finishes.plaster;
  return finishes.paleStone;
}

// Surrounding ground is separate from the first-layer "white model" base.
const grounds = new Mesh(new PlaneGeometry(240, 240), finishes.ground);
grounds.rotation.x = -Math.PI / 2;
grounds.position.set(9, -0.42, -9);
grounds.receiveShadow = true;
scene.add(grounds);
const approach = new Mesh(new BoxGeometry(2.6, 0.046, 13), finishes.courtyard);
approach.position.set(9, -0.17, 7.25);
approach.receiveShadow = true;
scene.add(approach);

// Physical architectural doors: pivot and slide ORIGINAL GLB meshes.
// The former build incorrectly placed a fake short door in front of the
// intact 4.2-metre south entrance, creating conflicting geometry.
const entranceHinge = new Group();
entranceHinge.position.set(8.16, 0, 0);
const innerSouthSlider = new Group();
const eastChapelSlider = new Group();
const rearSanctuaryHinge = new Group();
rearSanctuaryHinge.position.set(12, 0, -15.25);
const northCourtSlider = new Group();
let doorsAttached = false;

function connectArchitecturalDoors(building) {
  const mesh = name => {
    let result = null;
    building.traverse(object => {
      if (!result && object.isMesh && modelName(object.name).startsWith(modelName(name))) result = object;
    });
    if (!result) throw new Error("GLB missing original building door: " + name);
    return result;
  };
  scene.add(entranceHinge, innerSouthSlider, eastChapelSlider,
            rearSanctuaryHinge, northCourtSlider);
  scene.updateMatrixWorld(true);
  entranceHinge.attach(mesh("TALL SINGLE WHITE PIVOT DOOR"));
  innerSouthSlider.attach(mesh("D SOUTH COURT inner glass vestibule door"));
  eastChapelSlider.attach(mesh("C EAST CHAPEL large sliding glass door"));
  rearSanctuaryHinge.attach(mesh("SANCTUARY MAIN PUBLIC DOOR"));
  northCourtSlider.attach(mesh("A NORTH COURT double-wide glass door"));
  doorsAttached = true;
}

async function loadArchitecture() {
  if (typeof DecompressionStream !== "function") {
    throw new Error("Compressed GLB transport is unsupported");
  }
  const chunks = await Promise.all([0, 1, 2].map(async index => {
    const res = await fetch("/p2-maquette/model-v34." + index + ".part");
    if (!res.ok) throw new Error("Missing architectural model segment " + index);
    return new Uint8Array(await res.arrayBuffer());
  }));
  const merged = new Uint8Array(chunks.reduce((sum, chunk) => sum + chunk.length, 0));
  let offset = 0;
  for (const chunk of chunks) { merged.set(chunk, offset); offset += chunk.length; }
  const binary = await new Response(
    new Blob([merged]).stream().pipeThrough(new DecompressionStream("gzip"))
  ).arrayBuffer();
  const gltf = await new Promise((resolve, reject) => {
    new GLTFLoader().parse(binary, "/", resolve, reject);
  });
  const building = gltf.scene;
  building.traverse(object => {
    if (!object.isMesh) return;
    if (/^Model frame|study silhouette|construction guide|debug marker/i.test(object.name)) {
      object.visible = false;
      return;
    }
    object.material = chooseFinish(object.name);
    object.castShadow = object.material !== finishes.glazing && object.material !== finishes.leaves;
    object.receiveShadow = true;
    if (object.material === finishes.glazing) object.renderOrder = 2;
  });
  scene.add(building);
  connectArchitecturalDoors(building);
}

// The touring camera belongs to the actual 3D world, not the exterior
// maquette orbit camera. All positions are metres in GLB scene coordinates.
// Coordinate-verified route, following the actual openings.
// Entrance x8.16..10.54 z0; south inner glass z-6;
// courtyard x6..12 z-6..-12; east sliding door x12 z-7.5..-10.5;
// rear sanctuary door x12 z-15.25..-14.15; north court glass z-12.
const route = [
  { at: 0, p: [10.5, 2.20, 11.2], look: [9.35, 3.1, 0] },
  { at: 6, p: [9.35, 1.85, 5.0], look: [9.35, 2.4, 0] },
  { at: 11, p: [9.35, 1.82, 1.4], look: [9.35, 1.9, -4] },
  { at: 15, p: [9.35, 1.82, -1.6], look: [9.35, 1.83, -6.2] },
  { at: 20, p: [9.00, 1.82, -4.8], look: [9.00, 2.1, -8] },
  { at: 26, p: [9.00, 1.82, -8.9], look: [9.00, 2.8, -11.4] },
  { at: 31, p: [9.00, 1.82, -8.9], look: [12.7, 2.3, -8.9] },
  { at: 37, p: [11.6, 1.82, -9.0], look: [15.0, 2.1, -9.0] },
  { at: 42, p: [14.2, 1.82, -9.1], look: [15.0, 2.2, -4.0] },
  { at: 52, p: [15.0, 1.82, -9.1], look: [15.0, 3.8, -0.1] },
  { at: 60, p: [14.2, 1.82, -10.2], look: [12.1, 1.9, -14.8] },
  { at: 68, p: [12.5, 1.82, -14.7], look: [11.4, 1.85, -14.7] },
  { at: 74, p: [11.6, 1.82, -14.6], look: [9.3, 1.7, -13.5] },
  { at: 81, p: [9.1, 1.83, -13.5], look: [9.0, 1.9, -10] },
  { at: 89, p: [9.0, 1.82, -9.0], look: [9.0, 2.0, -5.3] }
];

function clamp01(t) { return Math.min(1, Math.max(0, t)); }
function ease(t) {
  const v = clamp01(t);
  return v * v * (3 - 2 * v);
}
function mix(a, b, t) { return a + (b - a) * t; }
function positionAlongRoute(seconds) {
  const t = Math.min(route[route.length - 1].at, Math.max(0, seconds));
  let index = 0;
  while (index < route.length - 2 && t > route[index + 1].at) index++;
  const a = route[index], b = route[index + 1];
  const u = ease((t - a.at) / Math.max(0.01, b.at - a.at));
  return {
    p: a.p.map((value, i) => mix(value, b.p[i], u)),
    look: a.look.map((value, i) => mix(value, b.look[i], u))
  };
}

let elapsed = 0, previousFrame = 0, isVisible = !document.hidden;
let pointerDown = false, pointerX = 0, pointerY = 0;
let yawOffset = 0, pitchOffset = 0;
canvas.addEventListener("pointerdown", event => {
  pointerDown = true; pointerX = event.clientX; pointerY = event.clientY;
  try { canvas.setPointerCapture(event.pointerId); } catch (_) {}
});
canvas.addEventListener("pointermove", event => {
  if (!pointerDown) return;
  yawOffset = Math.max(-0.72, Math.min(0.72, yawOffset + (event.clientX - pointerX) * 0.0025));
  pitchOffset = Math.max(-0.26, Math.min(0.26, pitchOffset + (event.clientY - pointerY) * 0.0017));
  pointerX = event.clientX; pointerY = event.clientY;
});
canvas.addEventListener("pointerup", () => { pointerDown = false; });
canvas.addEventListener("pointercancel", () => { pointerDown = false; });
document.addEventListener("visibilitychange", () => { isVisible = !document.hidden; previousFrame = 0; });

const lookAtVector = new Vector3();
function animate(now) {
  requestAnimationFrame(animate);
  if (!isVisible) { previousFrame = now; return; }
  const dt = previousFrame ? Math.min(0.045, Math.max(0, (now - previousFrame) / 1000)) : 0;
  previousFrame = now;
  if (!prefersReducedMotion) elapsed += dt;
  const duration = route[route.length - 1].at;
  // Brief pause at the last view; return to exterior on the next cycle.
  // A deterministic visual QA position, without adding any on-screen text.
  const params = new URLSearchParams(location.search);
  const proof = params.get("proofFrame");
  const t = proof !== null && Number.isFinite(Number(proof))
    ? Math.min(duration, Math.max(0, Number(proof)))
    : (prefersReducedMotion ? 42 : elapsed % (duration + 6));
  const sample = positionAlongRoute(t);
  camera.position.set(sample.p[0], sample.p[1], sample.p[2]);
  lookAtVector.set(sample.look[0], sample.look[1], sample.look[2]);
  const distance = camera.position.distanceTo(lookAtVector);
  lookAtVector.x += Math.sin(yawOffset) * Math.min(7, distance * 0.6);
  lookAtVector.y -= pitchOffset * Math.min(5, distance * 0.5);
  camera.lookAt(lookAtVector);
  if (!pointerDown) {
    yawOffset *= Math.pow(0.89, dt * 60);
    pitchOffset *= Math.pow(0.89, dt * 60);
  }
  if (doorsAttached) {
    entranceHinge.rotation.y = 1.5 * ease((t - 6) / 6.5);
    innerSouthSlider.position.x = -2.14 * ease((t - 14) / 5);
    eastChapelSlider.position.z = 3.16 * ease((t - 30) / 6);
    rearSanctuaryHinge.rotation.y = 1.43 * ease((t - 58) / 8);
    northCourtSlider.position.x = 2.15 * ease((t - 76) / 7);
  }
  renderer.render(scene, camera);
}

loadArchitecture().then(() => {
  document.body.classList.add("ready");
  requestAnimationFrame(animate);
}).catch(error => {
  console.error("Virtual church model load failed", error);
  document.body.classList.add("failed");
});
