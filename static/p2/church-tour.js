/**
 * Westside Watch / P2 — Living Water West virtual church.
 * Independent GitHub-hosted second-layer camera walkthrough.
 * Uses the existing architectural GLB as geometry only; never embeds the
 * growth-maquette application, its renderer, its labels, or ChatGPT Sites.
 */
import {
  t as Group, l as MeshStandardMaterial, M as Mesh,
  y as BoxGeometry, u as CylinderGeometry, p as Vector3,
  G as GLTFLoader, W as WebGLRenderer, S as SRGBColorSpace,
  A as ACESFilmicToneMapping, P as PCFSoftShadowMap,
  a as Scene, H as HemisphereLight, D as DirectionalLight,
  b as PlaneGeometry, N as OrthographicCamera, d as DoubleSide
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
const camera = new OrthographicCamera(-1, 1, 1, -1, 0.07, 220);
function resize() {
  const width = Math.max(1, window.innerWidth);
  const height = Math.max(1, window.innerHeight);
  renderer.setSize(width, height, false);
  const near = camera.near, far = camera.far;
  const vfov = (innerWidth < 650 ? 66 : 58) * Math.PI / 180;
  const top = near * Math.tan(vfov / 2), right = top * (width / height);
  camera.projectionMatrix.makePerspective(-right, right, top, -top, near, far);
  camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
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
  masonry: new MeshStandardMaterial({ color: 0xd3c5b0, roughness: 0.89 }),
  paleStone: new MeshStandardMaterial({ color: 0xe9dfcc, roughness: 0.85 }),
  plaster: new MeshStandardMaterial({ color: 0xe4d9c7, roughness: 0.94 }),
  floor: new MeshStandardMaterial({ color: 0xb8a28a, roughness: 0.86 }),
  courtyard: new MeshStandardMaterial({ color: 0xc6bba5, roughness: 0.9 }),
  roof: new MeshStandardMaterial({ color: 0x5d655f, roughness: 0.83, metalness: 0.06 }),
  glazing: new MeshStandardMaterial({
    color: 0xa2c1c0, roughness: 0.14, metalness: 0.17,
    transparent: true, opacity: 0.28, depthWrite: false, side: DoubleSide
  }),
  mullion: new MeshStandardMaterial({ color: 0x625e51, roughness: 0.49, metalness: 0.52 }),
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
  ivory: new MeshStandardMaterial({ color: 0xe4ddd1, roughness: 0.7 }),
  ground: new MeshStandardMaterial({ color: 0xb4b2a7, roughness: 1 })
};

function chooseFinish(name) {
  const n = name.toLowerCase();
  if (/cross|crucifix/.test(n)) return finishes.cross;
  if (/glass|glazing|window pane|glazed/.test(n)) return finishes.glazing;
  if (/mullion|window frame|metal frame|railing|handrail/.test(n)) return finishes.mullion;
  if (/roof|skylight surround|roof edge/.test(n)) return finishes.roof;
  if (/pew|pulpit|lectern|table|chair|cafe|bookcase|counter/.test(n)) return finishes.pew;
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

// A separate articulated real-space entry leaf, never a fake screen wipe.
// The leaf pivots from its actual south-side door jamb into the building.
const entranceHinge = new Group();
entranceHinge.position.set(8.16, 0.02, 0.23);
const leaf = new Mesh(new BoxGeometry(1.72, 2.65, 0.095), finishes.ivory);
leaf.position.set(0.86, 1.335, 0);
leaf.castShadow = true;
leaf.receiveShadow = true;
entranceHinge.add(leaf);
const doorGlass = new Mesh(new BoxGeometry(0.78, 1.38, 0.102), finishes.glazing);
doorGlass.position.set(0.85, 1.66, 0);
entranceHinge.add(doorGlass);
const handle = new Mesh(new BoxGeometry(0.035, 0.3, 0.055), finishes.mullion);
handle.position.set(1.53, 1.17, 0.085);
entranceHinge.add(handle);
const exteriorSill = new Mesh(new BoxGeometry(1.83, 0.065, 0.32), finishes.floor);
exteriorSill.position.set(9.04, 0.022, 0.23);
scene.add(exteriorSill, entranceHinge);

function hideOriginalSouthLeaf(root) {
  root.updateMatrixWorld(true);
  root.traverse(object => {
    if (!object.isMesh || !/door/i.test(object.name)) return;
    if (!/leaf|panel|entrance|south/i.test(object.name)) return;
    if (!object.geometry.boundingBox) object.geometry.computeBoundingBox();
    const center = object.geometry.boundingBox.getCenter(new Vector3());
    object.localToWorld(center);
    if (Math.abs(center.x - 9) < 2.3 && Math.abs(center.z) < 1.35) {
      object.visible = false;
    }
  });
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
    object.material = chooseFinish(object.name);
    object.castShadow = object.material !== finishes.glazing && object.material !== finishes.leaves;
    object.receiveShadow = true;
    if (object.material === finishes.glazing) object.renderOrder = 2;
  });
  hideOriginalSouthLeaf(building);
  scene.add(building);
}

// The touring camera belongs to the actual 3D world, not the exterior
// maquette orbit camera. All positions are metres in GLB scene coordinates.
const route = [
  { at: 0,  p: [13.7, 5.3, 14.4], look: [9.0, 2.6, -0.1] },
  { at: 6,  p: [10.6, 2.6, 7.4], look: [9.0, 2.0, 0.0] },
  { at: 12, p: [9.0, 1.76, 3.15], look: [9.0, 1.7, -3.8] },
  { at: 19, p: [9.0, 1.76, -2.15], look: [9.0, 1.8, -9.1] },
  { at: 28, p: [9.0, 1.81, -8.9], look: [11.5, 2.2, -10.1] },
  { at: 37, p: [12.55, 1.75, -9.1], look: [15.0, 2.1, -9.8] },
  { at: 45, p: [15.4, 1.80, -10.7], look: [15.1, 2.7, -1.1] },
  { at: 54, p: [13.1, 1.89, -9.5], look: [9.0, 2.1, -10.7] },
  { at: 62, p: [5.9, 1.82, -11.7], look: [2.2, 0.6, -15.1] },
  { at: 70, p: [4.4, 2.55, -14.1], look: [6.5, 1.7, -9.0] },
  { at: 80, p: [9.0, 1.84, -8.2], look: [9.0, 2.0, -2.5] },
  { at: 92, p: [9.0, 1.77, -3.3], look: [9.0, 2.0, 0.8] }
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
  const t = prefersReducedMotion ? 43 : (elapsed % (duration + 5));
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
  entranceHinge.rotation.y = ease((t - 7.4) / 5.2) * 1.47;
  renderer.render(scene, camera);
}

loadArchitecture().then(() => {
  document.body.classList.add("ready");
  requestAnimationFrame(animate);
}).catch(error => {
  console.error("Virtual church model load failed", error);
  document.body.classList.add("failed");
});
