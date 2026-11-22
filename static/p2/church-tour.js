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
  a as Scene, H as HemisphereLight, D as DirectionalLight, f as SpotLight, c as ShaderMaterial,
  b as PlaneGeometry, o as PerspectiveCamera, d as DoubleSide,
  e as CanvasTexture
} from "../p2-maquette/assets/GLTFLoader-j388d5bW.js";

const canvas = document.querySelector("#church-canvas");
const prefersReducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const scene = new Scene();
const renderer = new WebGLRenderer({
  canvas, antialias: true, powerPreference: "high-performance", alpha: false
});
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
renderer.outputColorSpace = SRGBColorSpace;
renderer.toneMapping = ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.94;
renderer.shadowMap.enabled = true;
// PCFSoft ignores shadow.radius: use standard PCF with a measured
// filter width for real penumbra, as specified by Three.js LightShadow.
renderer.shadowMap.type = 1; // Three.js PCFShadowMap
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

// Lightweight architectural daylight rig: open-sky diffuse illumination,
// one moving solar key, two shadowless room-bounce fills. No extra render pass.
const skyFill = new HemisphereLight(0xeaf1ff, 0xb4afa4, 1.18);
scene.add(skyFill);
const sun = new DirectionalLight(0xfff0db, 1.7);
sun.position.set(4, 21, 10);
sun.target.position.set(9, 0, -8);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, {
  left: -19, right: 19, top: 19, bottom: -19, near: 0.1, far: 85
});
sun.shadow.normalBias = 0.015;
sun.shadow.bias = -0.0002;
sun.shadow.radius = 3.25;
scene.add(sun, sun.target);
const ambientFill = new DirectionalLight(0xddeaff, 0.44);
ambientFill.position.set(19, 12, -24);
scene.add(ambientFill);
// Warm secondary reflected light from the opposite side of the courtyard.
// Shadowless bounce preserves readable interior whites without fake beams.
const bounceFill = new DirectionalLight(0xffead7, 0.28);
bounceFill.position.set(-13, 8, 12);
scene.add(bounceFill);
const sanctuaryLight = new DirectionalLight(0xfff1e4, 0.12);
sanctuaryLight.position.set(15.5, 5.1, -1.3);
sanctuaryLight.target.position.set(15, 1.4, -10);
scene.add(sanctuaryLight, sanctuaryLight.target);

/* CROSS LIGHT R14: original Blender V23 South Cross wall coordinates.
 * Real aperture is centered at x=15, height=3.65m with a 0.23m slit.
 * Earlier variants placed a second fake cross ~1.07m BELOW the true opening.
 * Keep the real aperture unchanged and apply only aligned soft light.
 */
const crossAperture={x:15,y:3.65,z:-.19,height:7.3,width:6.0};
function crossLightMask(kind){
  const size=384, canvas=document.createElement("canvas");canvas.width=canvas.height=size;
  const ctx=canvas.getContext("2d"),img=ctx.createImageData(size,size);
  const g=(v,r)=>Math.exp(-Math.pow(v/r,2));
  for(let y=0;y<size;y++)for(let x=0;x<size;x++){
    const u=(x+.5)/size-.5,v=(y+.5)/size-.5;
    let a;
    if(kind==="cross"){
      a=.48*Math.max(g(u,.047)*g(v,.43),g(v,.045)*g(u,.40))
        +.26*g(u,.115)*g(v,.17)+.26*g(u,.245)*g(v,.32);
    }else if(kind==="floor"){
      a=.42*g(u,.085)*g(v-.03,.47)+.27*g(v+.06,.086)*g(u,.37)
        +.31*g(u,.30)*g(v,.40);
    }else a=.52*g(u-.025,.20)*g(v,.26)+.48*g(u,.34)*g(v,.34);
    const n=(y*size+x)*4,k=Math.round(255*Math.min(1,a));
    img.data[n]=img.data[n+1]=img.data[n+2]=k;img.data[n+3]=255;
  }
  ctx.putImageData(img,0,0);
  return new CanvasTexture(canvas);
}
function luminousSurface(mask,opacity,glow){
  return new MeshStandardMaterial({
    color:0x080806,emissive:0xffe9c9,emissiveIntensity:glow,
    alphaMap:mask,transparent:true,opacity,roughness:1,
    metalness:0,depthWrite:false,depthTest:true,side:DoubleSide,
    blending:2 // THREE.AdditiveBlending; physically light adds, never greys white walls
  });
}
const apertureGlow=new Mesh(
  new PlaneGeometry(crossAperture.width+0.35,crossAperture.height+0.25),
  luminousSurface(crossLightMask("cross"),.20,.95)
);
apertureGlow.position.set(crossAperture.x,crossAperture.y,crossAperture.z);apertureGlow.name="Cross aperture diffuse radiance";
apertureGlow.renderOrder=3;scene.add(apertureGlow);
const crossFloorLight=new Mesh(new PlaneGeometry(4.2,9.4),luminousSurface(crossLightMask("floor"),.28,.82));
crossFloorLight.rotation.x=-Math.PI/2;crossFloorLight.position.set(15,.085,-5.0);
crossFloorLight.name="Sanctuary sunlight floor bounce";crossFloorLight.renderOrder=3;
scene.add(crossFloorLight);
// Analytic scattering, not three opaque transparent light cards. The
// fragment mask decays to zero at every boundary; soft procedural dust moves
// slowly without image-sequence flicker or third-party heavy postprocessing.
const crossAirMaterial=new ShaderMaterial({
  transparent:true,depthWrite:false,depthTest:true,blending:2,side:DoubleSide,
  uniforms:{
    uLight:{value:0},
    uTime:{value:0},
    uTint:{value:new Vector3(1.0,.81,.64)}
  },
  vertexShader:`
    varying vec2 vUv;
    void main(){
      vUv=uv;
      gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);
    }`,
  fragmentShader:`
    precision highp float;
    varying vec2 vUv;
    uniform float uLight;
    uniform float uTime;
    uniform vec3 uTint;
    float gaussian(float x,float r){return exp(-pow(x/r,2.0));}
    void main(){
      // vUv.y=0 is the REAL CROSS, vUv.y=1 reaches the floor.
      // A beam spreads as it travels and its energy attenuates with depth.
      vec2 p=vUv-.5;
      float spread=.115+.20*vUv.y;
      float core=gaussian(p.x,spread*.60);
      float halo=gaussian(p.x,spread*1.55);
      float axial=smoothstep(.01,.14,vUv.y)
                  *(1.0-smoothstep(.74,1.0,vUv.y))*exp(-1.08*vUv.y);
      float side=smoothstep(0.0,.12,vUv.x)*smoothstep(0.0,.12,1.0-vUv.x);
      float motes=1.0+.045*sin(vUv.x*19.0+uTime*.07)*sin(vUv.y*17.0-uTime*.06);
      float density=(.37*core+.63*halo)*axial*side*motes;
      gl_FragColor=vec4(uTint,density*uLight);
    }`
});
const crossAirVolumes=[],crossRayAngles=[0,1.05,-1.05];
const crossRayOrigin=new Vector3(crossAperture.x,crossAperture.y,crossAperture.z-.25);
const crossRayTarget=new Vector3(),crossRayDirection=new Vector3();
const crossRayUnit=new Vector3(),crossRayMidpoint=new Vector3();
const localBeamAxis=new Vector3(0,1,0);
for(const turn of crossRayAngles){
  // Geometry's local +Y maps from actual cross to actual sunlit floor point.
  const ray=new Mesh(new PlaneGeometry(4.2,10),crossAirMaterial);
  ray.renderOrder=3;
  ray.name="Cross sun-tracked volumetric scattering";
  ray.userData.rotationalSlice=turn;
  scene.add(ray);crossAirVolumes.push(ray);
}
// Two actual PBR light sources, using the same locally bundled Three.js.
// Key: broad cone following sunlight from the genuine aperture toward pews.
// Bounce: reflected warmth from the floor returns to plaster and altar.
// Both are shadowless; the real directional sun keeps its geometric shadows.
const crossPortalKey=new SpotLight(0xffe8c8,0,14,0.76,0.88,2);
crossPortalKey.position.set(crossAperture.x,crossAperture.y,crossAperture.z-.24);
crossPortalKey.target.position.set(15,0,-5.0);
crossPortalKey.castShadow=false;
scene.add(crossPortalKey,crossPortalKey.target);
const crossWallBounce=new SpotLight(0xfff2e2,0,10,0.89,0.94,2);
crossWallBounce.position.set(15,.24,-5.0);
crossWallBounce.target.position.set(15,2.4,-1.45);
crossWallBounce.castShadow=false;
scene.add(crossWallBounce,crossWallBounce.target);
// R23 FINALE: Light FROM the Lord's house, through the REAL SOUTH CROSS,
// toward the arriving viewer. Independent of the inward daytime sun.
const finaleInteriorLamp=new SpotLight(0xffddb1,0,13,.78,.89,2);
finaleInteriorLamp.position.set(15,3.35,-1.9);
finaleInteriorLamp.target.position.set(15,3.65,.6);
finaleInteriorLamp.castShadow=false;
scene.add(finaleInteriorLamp,finaleInteriorLamp.target);
const finaleExteriorLamp=new SpotLight(0xffc98f,0,14,.68,.9,2);
finaleExteriorLamp.position.set(15,3.65,.15);
finaleExteriorLamp.target.position.set(15,2.8,7.2);
finaleExteriorLamp.castShadow=false;
scene.add(finaleExteriorLamp,finaleExteriorLamp.target);
// Warm light reflected by the actual WHITE FACADE: without this real
// PBR wash the cross looked like a harsh, isolated white neon sticker.
const finaleFacadeBounce=new SpotLight(0xffc58e,0,12,1.02,.92,2);
finaleFacadeBounce.position.set(15.1,3.55,4.4);
finaleFacadeBounce.target.position.set(15.0,3.25,-.12);
finaleFacadeBounce.castShadow=false;
scene.add(finaleFacadeBounce,finaleFacadeBounce.target);
const finaleGroundPool=new Mesh(
  new PlaneGeometry(7.8,8.6),
  luminousSurface(crossLightMask("air"),0,.93)
);
finaleGroundPool.material.emissive.setHex(0xffba78);
finaleGroundPool.rotation.x=-Math.PI/2;
finaleGroundPool.position.set(15,-.379,4.0);
finaleGroundPool.renderOrder=3;
finaleGroundPool.name="Exterior crosslight pool beyond the threshold";
scene.add(finaleGroundPool);
// Cross aperture backing is slightly behind the opening; the very faint
// exterior scattering plane is just outside the south facade.
const finaleCrossCore=new Mesh(
  new PlaneGeometry(6.35,7.55),
  luminousSurface(crossLightMask("cross"),0,1.12)
);
finaleCrossCore.material.emissive.setHex(0xffd4a0);
finaleCrossCore.position.set(15,3.65,-.26);
finaleCrossCore.renderOrder=3;finaleCrossCore.name="Cross interior tungsten luminance";
scene.add(finaleCrossCore);
const finaleCrossHalo=new Mesh(
  new PlaneGeometry(6.35,7.55),
  luminousSurface(crossLightMask("cross"),0,.58)
);
finaleCrossHalo.material.emissive.setHex(0xffbb81);
finaleCrossHalo.position.set(15,3.65,.075);
finaleCrossHalo.renderOrder=4;finaleCrossHalo.name="Cross exterior feathered glow";
scene.add(finaleCrossHalo);
const finaleAirMaterial=crossAirMaterial.clone();
finaleAirMaterial.uniforms.uTint.value.set(1,.70,.44);
const finaleRays=[];
const finaleOrigin=new Vector3(15,3.65,.19);
const finaleTarget=new Vector3(15,2.65,8.6);
const finaleDirection=new Vector3().subVectors(finaleTarget,finaleOrigin);
const finaleAxis=new Vector3().copy(finaleDirection).normalize();
for(const turn of [0,1.08,-1.08]){
  const ray=new Mesh(new PlaneGeometry(4.1,10),finaleAirMaterial);
  ray.position.copy(finaleOrigin).addScaledVector(finaleDirection,.5);
  ray.quaternion.setFromUnitVectors(localBeamAxis,finaleAxis);
  ray.rotateY(turn);
  ray.scale.y=finaleDirection.length()/10;
  ray.name="Cross outward evening scattering";ray.renderOrder=3;
  scene.add(ray);finaleRays.push(ray);
}
// A tiny SRGB procedural twilight gradient, not a black night or an
// imported HDRI. Updated only in the final transition, preserving old scenes.
const finalSkyCanvas=document.createElement("canvas");
finalSkyCanvas.width=8;finalSkyCanvas.height=192;
const finalSkyContext=finalSkyCanvas.getContext("2d");
const finalSkyTexture=new CanvasTexture(finalSkyCanvas);
finalSkyTexture.colorSpace=SRGBColorSpace;
let lastSkySample=-1;
const oldSky=[215,216,207];
function eveningSky(t){
  const blend=ease((t-232)/16);
  if(t<232){scene.background=null;return blend;}
  scene.background=finalSkyTexture;
  const sample=Math.floor(blend*150);
  if(sample!==lastSkySample){
    const lerp=(a,b)=>Math.round(a+(b-a)*blend);
    const grad=finalSkyContext.createLinearGradient(0,0,0,192);
    const endColors=[[70,84,108],[111,122,139],[172,160,151]];
    const mixColor=c=>"rgb("+c.map((value,i)=>lerp(oldSky[i],value)).join(",")+")";
    grad.addColorStop(0,mixColor(endColors[0]));
    grad.addColorStop(.6,mixColor(endColors[1]));
    grad.addColorStop(1,mixColor(endColors[2]));
    finalSkyContext.fillStyle=grad;
    finalSkyContext.fillRect(0,0,8,192);
    finalSkyTexture.needsUpdate=true;lastSkySample=sample;
  }
  return blend;
}
window.__churchFinaleAudit={active:false,twilight:0,crossCore:0,interiorLamp:0,exteriorLamp:0,outwardBeam:0};
window.__churchLightAudit={
  aperture:true,floor:true,sheets:crossAirVolumes.length,additive:true,
  crossCenter:[crossAperture.x,crossAperture.y,crossAperture.z],
  bounceSources:2,volumeShader:true,beamTracksSun:true,adaptiveExposure:true,
  outwardFinale:true,facadeWarmth:true,version:"R24"
};

// Stable procedural finishes stored as source code in GitHub; no CDN assets.
function createSurface(kind) {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 256;
  const context = canvas.getContext("2d");
  const image = context.createImageData(256, 256);
  const d = image.data;
  for (let y=0;y<256;y++) for(let x=0;x<256;x++){
    const j=(y*256+x)*4;
    const hash=Math.sin((x+2)*127.1+(y+11)*311.7)*43758.5453;
    const noise=hash-Math.floor(hash)-.5;
    const vein=Math.sin(y*.27+Math.sin(x*.031)*5)*.5;
    const scatter=Math.sin(x*.14+y*.17)*Math.cos(y*.22);
    const value=kind==="wood"?225+vein*18+noise*12:
                kind==="stone"?235+scatter*5+noise*11:241+scatter*3+noise*8;
    d[j]=value;
    d[j+1]=value-(kind==="wood"?11:0);
    d[j+2]=value-(kind==="wood"?23:2);
    d[j+3]=255;
  }
  context.putImageData(image,0,0);
  const texture=new CanvasTexture(canvas);
  texture.colorSpace=SRGBColorSpace;
  texture.wrapS=texture.wrapT=1000; // THREE.RepeatWrapping
  texture.repeat.set(kind==="wood"?2:3,kind==="wood"?2:3);
  texture.anisotropy=4;
  return texture;
}
const surfaceMaps={
  stone:createSurface("stone"),plaster:createSurface("plaster"),
  wood:createSurface("wood")
};

const finishes = {
  masonry: new MeshStandardMaterial({ map: surfaceMaps.stone, bumpMap: surfaceMaps.stone, bumpScale: 0.018, color: 0xcad0c8, roughness: 0.89 }),
  paleStone: new MeshStandardMaterial({ map: surfaceMaps.stone, bumpMap: surfaceMaps.stone, bumpScale: 0.014, color: 0xe3e5dc, roughness: 0.85 }),
  plaster: new MeshStandardMaterial({ map: surfaceMaps.plaster, bumpMap: surfaceMaps.plaster, bumpScale: 0.012, color: 0xe9eae5, roughness: 0.94 }),
  floor: new MeshStandardMaterial({ map: surfaceMaps.stone, bumpMap: surfaceMaps.stone, bumpScale: 0.012, color: 0xcac2b5, roughness: 0.86 }),
  courtyard: new MeshStandardMaterial({ map: surfaceMaps.stone, bumpMap: surfaceMaps.stone, bumpScale: 0.016, color: 0xd0cec2, roughness: 0.9 }),
  roof: new MeshStandardMaterial({ map: surfaceMaps.stone, color: 0xc4c9c2, roughness: 0.83, metalness: 0.04, side: DoubleSide }),
  glazing: new MeshStandardMaterial({
    color: 0xc3d6d7, roughness: 0.14, metalness: 0.17,
    transparent: true, opacity: 0.22, depthWrite: false, side: DoubleSide,
    forceSinglePass: true
  }),
  mullion: new MeshStandardMaterial({ color: 0x707772, roughness: 0.49, metalness: 0.52 }),
  timber: new MeshStandardMaterial({ map: surfaceMaps.wood, color: 0x927254, roughness: 0.75 }),
  joinery: new MeshStandardMaterial({ map: surfaceMaps.wood, color: 0x765943, roughness: 0.71 }),
  pew: new MeshStandardMaterial({ map: surfaceMaps.wood, color: 0x79593f, roughness: 0.69 }),
  cross: new MeshStandardMaterial({
    color: 0xe6c58c, emissive: 0xb27d38, emissiveIntensity: 0.47,
    roughness: 0.34, metalness: 0.38
  }),
  leaves: new MeshStandardMaterial({ color: 0x707f62, roughness: 1, side: DoubleSide }),
  earth: new MeshStandardMaterial({ color: 0x81927c, roughness: 1 }),
  metal: new MeshStandardMaterial({ color: 0x696e69, roughness: 0.49, metalness: 0.66 }),
  ivory: new MeshStandardMaterial({ color: 0xf2f1eb, roughness: 0.7 }),
  ground: new MeshStandardMaterial({ color: 0xc5c8c0, roughness: 1 })
};

// GLTFLoader sanitizes source node labels into animation-safe identifiers
// (spaces become underscores). Match against normalized source names.
function modelName(value) {
  return String(value).toLowerCase().replace(/[_\s·.–—]+/g, " ").trim();
}
// Architectural paint: the approved building is white on both sides.
// Preserve independent translucent glazing and the original maple bark/leaves.
const whiteArchitecture = new MeshStandardMaterial({
  color:0xf5f5f1, roughness:0.91, metalness:0, side:DoubleSide,
  polygonOffset:true, polygonOffsetFactor:0.5, polygonOffsetUnits:1
});
const whiteFloor = new MeshStandardMaterial({
  color:0xebebe7, roughness:0.94, metalness:0, side:DoubleSide,
  polygonOffset:true, polygonOffsetFactor:1.8, polygonOffsetUnits:1
});
function chooseFinish(name, sourceMaterial) {
  const n=modelName(name);
  if (/maple cc0/.test(n)) return sourceMaterial;
  if (/glass|glazing|glazed|window pane|skylight/i.test(n)) {
    const m=finishes.glazing.clone();
    m.forceSinglePass=true;
    m.polygonOffset=true; m.polygonOffsetFactor=-1; m.polygonOffsetUnits=-1;
    return m;
  }
  if (/mullion|window frame|metal frame|railing|handrail/i.test(n)) return finishes.mullion;
  if (/leaf|foliage|shrub|plant|grass|soil/i.test(n)) return finishes.earth;
  if (/floor|paving|tile|courtyard|terrace|step|stair|landing|promenade|piazza|plaza|forum|cafe|coffee/i.test(n))
    return whiteFloor;
  return whiteArchitecture;
}

// Surrounding ground is separate from the first-layer "white model" base.
// EXTERIOR ONLY: a single 240m ground plane previously covered the
// -2.10m C-shaped sunken forum and concealed its original GLB treads.
// Four strips leave the 18x18m architectural footprint completely open.
// Stop the 240m ground strips from cutting the high-angle skyline.
// Limit terrain to a modest perimeter around the real 18m church.
const siteGround = [
  [-6,-9,12,54], [24,-9,12,54],
  [9,9,18,18], [9,-27,18,18]
];
for(const [x,z,width,depth] of siteGround){
  const ground=new Mesh(new PlaneGeometry(width,depth), finishes.ground);
  ground.rotation.x=-Math.PI/2;
  ground.position.set(x,-0.42,z);
  ground.receiveShadow=true;
  scene.add(ground);
}
// Removed the artificial overlaid entrance slab: it conflicted with the original GLB paving.

// Physical architectural doors: pivot and slide ORIGINAL GLB meshes.
// The former build incorrectly placed a fake short door in front of the
// intact 4.2-metre south entrance, creating conflicting geometry.
const entranceHinge = new Group();
entranceHinge.position.set(8.16, 0, 0);
const innerSouthSlider = new Group();
const eastChapelSlider = new Group();
const rearSanctuaryHinge = new Group();
rearSanctuaryHinge.position.set(12, 0, -15.25);
const staffSanctuaryHinge = new Group();
staffSanctuaryHinge.position.set(12, 0, -2.65);
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
            rearSanctuaryHinge, staffSanctuaryHinge, northCourtSlider);
  scene.updateMatrixWorld(true);
  const southDoor = mesh("TALL SINGLE WHITE PIVOT DOOR");
  const northPublicDoor = mesh("SANCTUARY MAIN PUBLIC DOOR");
  const southStaffDoor = mesh("SANCTUARY STAFF DOOR");
  entranceHinge.attach(southDoor);
  innerSouthSlider.attach(mesh("D SOUTH COURT inner glass vestibule door"));
  eastChapelSlider.attach(mesh("C EAST CHAPEL large sliding glass door"));
  rearSanctuaryHinge.attach(northPublicDoor);
  staffSanctuaryHinge.attach(southStaffDoor);
  // Critical: the original door leaves have already been reparented to
  // scene-level hinge Groups. Traversing `building` now misses those meshes.
  // Purge from the ENTIRE scene after reparenting. Remove hardware geometry,
  // do not merely hide a parent which may later be reused or cloned.
  const handles = [];
  scene.traverse(object => {
    if (object !== scene && /handle|knob|pull|lever|latch|lockset|grip|hardware|fitting/i.test(modelName(object.name)))
      handles.push(object);
  });
  for (const object of handles) {
    object.visible = false;
    object.castShadow = false;
    object.parent?.remove(object);
  }
  const remaining = [];
  scene.traverse(object => {
    if (object.isMesh && object.visible && /handle|knob|pull|lever|latch|lockset|grip|hardware|fitting/i.test(modelName(object.name)))
      remaining.push(object.name);
  });
  window.__churchHardwareAudit = {
    removed: handles.map(object => object.name),
    remaining
  };
  if (remaining.length) throw new Error("Door hardware still visible: " + remaining.join(", "));
  northCourtSlider.attach(mesh("A NORTH COURT double-wide glass door"));
  doorsAttached = true;
}

// The complete model includes the original realistic CC0 Japanese maple.
// Re-use its geometry beyond the entrance as a landscaping entourage.
function addNativeLandscape(building) {
  // No extra perimeter trees. Keep the original courtyard maple from the GLB.
  // Nothing is cloned across the exterior or pasted onto the architecture.
}

// Source GLB material IDs: 15 fine twig bark, 16 rough living bark,
// 17/18/19 red Japanese maple foliage. Preserve imported trunk/root/twig
// materials as-is; recolor *only the foliage image* across four seasons.
const seasonalLeaves = new Map();
const originalStructuralMaterials = new Map();
// Original GLB architecture stays untouched; seasonal snow affects only the
// separate exterior ground and landscape soil, never bark or stone walls.
const winterGroundColor = new MeshStandardMaterial({color:0xe5e6e1}).color;
const winterSoilColor = new MeshStandardMaterial({color:0xd9dbd5}).color;
const seasonalGroundColors = new Map([
  [finishes.ground, finishes.ground.color.clone()],
  [finishes.earth, finishes.earth.color.clone()]
]);
const mapleAutumn = {r:0.56,g:0.18,b:0.15}; // V24 source burgundy, not guessed
function registerMapleSource(mesh) {
  const n=modelName(mesh.name);
  if(!/maple cc0/.test(n)) return false;
  if(!/connected crown|foliage/.test(n)) return true; // bark: untouched
  const material=mesh.material.clone();
  mesh.material=material;
  material.side=DoubleSide;
  const record={material,source:material.color.clone(),lastBucket:-1,sourceImage:null};
  // The CC0 tree is RED in its original texture. To recover the previously
  // approved green spring/summer canopy, tint its own leaf texture by hue
  // rotation, not the bark and not a newly invented solid green material.
  const originalMap=material.map;
  const image=originalMap?.image;
  if(image?.width&&image?.height){
    const paint=document.createElement("canvas");
    paint.width=Math.max(16,Math.min(image.width,512));
    paint.height=Math.max(16,Math.min(image.height,512));
    const ctx=paint.getContext("2d");
    const newMap=new CanvasTexture(paint);
    newMap.colorSpace=originalMap.colorSpace;
    newMap.flipY=originalMap.flipY;
    newMap.wrapS=originalMap.wrapS;
    newMap.wrapT=originalMap.wrapT;
    newMap.repeat.copy(originalMap.repeat);
    newMap.offset.copy(originalMap.offset);
    newMap.rotation=originalMap.rotation;
    newMap.anisotropy=originalMap.anisotropy;
    record.ctx=ctx;record.sourceImage=image;record.map=newMap;
    material.map=newMap;
    material.color.setRGB(1,1,1);
    material.needsUpdate=true;
  }
  seasonalLeaves.set(material,record);
  return true;
}
function seasonalSmooth(x) {x=Math.max(0,Math.min(1,x));return x*x*(3-2*x);}
function updateMapleSeason(t,duration) {
  const x=Math.min(1,Math.max(0,t/duration));
  // Distinct seasons remain bound to the real walking camera. Preserve
  // all original leaf image detail and foliage transparency through tint.
  const summer=seasonalSmooth((x-.18)/.22);
  const autumn=seasonalSmooth((x-.48)/.16);
  const winter=seasonalSmooth((x-.73)/.16);
  const hueRotate=(118-14*summer)*(1-autumn);  // original red -> green
  const brightness=1-.46*winter;                // winter deep red
  const bucket=Math.round(hueRotate*4)+"_"+Math.round(brightness*100);
  for(const record of seasonalLeaves.values()) {
    const {material,source,ctx,sourceImage,map}=record;
    if(ctx && sourceImage && map){
      if(record.lastBucket===bucket)continue;
      record.lastBucket=bucket;
      ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);
      ctx.filter="hue-rotate("+hueRotate.toFixed(2)+"deg) brightness("+brightness.toFixed(3)+")";
      ctx.drawImage(sourceImage,0,0,ctx.canvas.width,ctx.canvas.height);
      ctx.filter="none";
      map.needsUpdate=true;
    }else{
      // Fallback for leaf material without an imported image.
      const color=source.clone();
      const hsl={h:0,s:0,l:0};color.getHSL(hsl);
      color.setHSL((hsl.h+hueRotate/360)%1,hsl.s,hsl.l*brightness);
      material.color.copy(color);
    }
  }
  // The approved winter tour includes visible snow on exterior ground.
  // Do not recolor the original building or tree bark: ground and soil are
  // independent materials, so the autumn-to-winter transition remains gradual.
  const snow=seasonalSmooth((x-.77)/.14);
  for(const [mat,original] of seasonalGroundColors){
    mat.color.copy(original).lerp(
      mat===finishes.ground ? winterGroundColor : winterSoilColor, snow
    );
  }
  for(const [mat,original] of originalStructuralMaterials){
    mat.color.copy(original);
    mat.color.r+=(1-mat.color.r)*snow*.35;
    mat.color.g+=(1-mat.color.g)*snow*.35;
    mat.color.b+=(1-mat.color.b)*snow*.35;
  }
}

// Preserve doors, true stair treads, walls and the third-level overlook.
// The original concept GLB also contained room-study slabs and ghost roof
// panels which are NOT walkable head-clearance-safe in the sunken forum.
const ghostRoofMeshes=[];
const removedObstructions=[];
const forumSafetyBoxes=[];
const eliminatedHeadHazards=[];
const cameraSafetyReport={samples:0,corrected:0,penetrations:0,forwardOcclusions:0,headroomHazards:0,objects:[]};
const forumPathTimes=()=>Array.from({length:111},(_,i)=>121+i*.5);
const isCForumTime=t=>t>=121&&t<=178;
const isInteriorClearanceTime=t=>t>=103&&t<=232;
function meshWorldBox(mesh){
  if(!mesh.geometry?.boundingBox)mesh.geometry?.computeBoundingBox();
  if(!mesh.geometry?.boundingBox)return null;
  return mesh.geometry.boundingBox.clone().applyMatrix4(mesh.matrixWorld);
}
function overlapsWalkColumn(box,p,radius=.72){
  return box.min.x<=p[0]+radius&&box.max.x>=p[0]-radius
    &&box.min.z<=p[2]+radius&&box.max.z>=p[2]-radius;
}
// R27: The eight V26 upper-ascent treads were isolated individual cubes,
// visually forming loose fragments. Use their ORIGINAL GLB coordinates to
// add two narrow structural stringers just beneath their undersides.
// Preserve treads, landings and the open usable space under the staircase.
const upperStairAudit={treads:0,stringers:0,source:"V26_ROUTE_03",centers:[]};
function connectUpperStairTreads(building){
  const steps=[];
  building.updateMatrixWorld(true);
  building.traverse(mesh=>{
    if(!mesh.isMesh||!mesh.visible)return;
    if(!/^v26 route 03 .*inhabited upper ascent/i.test(modelName(mesh.name)))return;
    const b=meshWorldBox(mesh);if(b)steps.push({mesh,b});
  });
  steps.sort((a,b)=>a.b.min.x-b.b.min.x);
  upperStairAudit.treads=steps.length;
  upperStairAudit.centers=steps.map(x=>([
    +(x.b.min.x+x.b.max.x).toFixed(2)/2,
    +(x.b.min.y+x.b.max.y).toFixed(2)/2
  ]));
  if(steps.length<6)return;
  const first=steps[0].b,last=steps[steps.length-1].b;
  const x0=(first.min.x+first.max.x)/2;
  const x1=(last.min.x+last.max.x)/2;
  const rise=(last.min.y-first.min.y)/(x1-x0);
  const baseX=x0-.28,topX=x1+.28;
  const baseY=first.min.y-.075-rise*.28;
  const topY=last.min.y-.075+rise*.28;
  const length=Math.hypot(topX-baseX,topY-baseY);
  const depth=(first.max.z-first.min.z);
  const zCenter=(first.min.z+first.max.z)/2;
  const angle=Math.atan2(topY-baseY,topX-baseX);
  const beamMaterial=whiteArchitecture;
  for(const zSide of [-1,1]){
    const beam=new Mesh(new BoxGeometry(length,.15,.105),beamMaterial);
    beam.name="V26 continuous upper stair structural side stringer";
    beam.position.set((baseX+topX)/2,(baseY+topY)/2,
      zCenter+zSide*(depth/2-.09));
    beam.rotation.z=angle;
    beam.castShadow=true;
    beam.receiveShadow=true;
    building.add(beam);
    upperStairAudit.stringers++;
  }
}

function removeHeadHeightHazards(building){
  // Check REAL BIM/GLB bounds against every half-second of the LOWER
  // forum descent. A low horizontal projection into the walking corridor
  // is removed, instead of merely steering the camera through its mesh.
  const samples=forumPathTimes().map(t=>positionAlongRoute(t));
  building.updateMatrixWorld(true);
  building.traverse(mesh=>{
    if(!mesh.isMesh||!mesh.visible)return;
    const n=modelName(mesh.name);
    if(!/(?:soffit|fascia|room|gallery|mid|cantilever|overhang|bridge|slab|balcony|project|landing|terrace|beam)/i.test(n)
      ||/(?:tread|stair|step|skylight|glass|door|railing|handrail|roof|floor|paving|maple|tree|column|foundation)/i.test(n))return;
    const box=meshWorldBox(mesh);if(!box)return;
    const thickness=box.max.y-box.min.y;
    if(thickness>1.15)return; // full walls and inhabited rooms are not fake soffits
    const headStrike=samples.find(v=>overlapsWalkColumn(box,v.p,.85)
      &&box.min.y>=v.p[1]-.30
      &&box.min.y<=v.p[1]+.62
      &&box.max.y>=v.p[1]+.17);
    if(!headStrike)return;
    mesh.visible=false;mesh.castShadow=false;
    eliminatedHeadHazards.push({name:mesh.name,
      min:[box.min.x,box.min.y,box.min.z].map(v=>+v.toFixed(2)),
      max:[box.max.x,box.max.y,box.max.z].map(v=>+v.toFixed(2))});
  });
}
function buildCameraSafetyBoxes(building){
  // AABB broad phase only; omit large curved envelopes to avoid treating
  // their empty interior as solid. Ground and actual stair treads remain.
  building.updateMatrixWorld(true);
  building.traverse(mesh=>{
    if(!mesh.isMesh||!mesh.visible)return;
    const n=modelName(mesh.name);
    if(!/(wall|partition|panel|soffit|fascia|column|post|support|screen|balustrade|railing|glass|mullion|door|beam|parapet|ledge|lintel|landing|terrace|slab|roof|ceiling|floor)/i.test(n)
       ||/(?:foliage|maple|tree|ground|sky|ghost cutaway)/i.test(n))return;
    const box=meshWorldBox(mesh);if(!box)return;
    if(box.max.x < -1||box.min.x>18||box.max.z<-19||box.min.z>1)return;
    // Protect camera from bounded solid surfaces only, not large
    // ring-shaped forum geometry whose box contains empty air.
    const dx=box.max.x-box.min.x,dz=box.max.z-box.min.z;
    const h=box.max.y-box.min.y;
    // Large ring-shaped floor envelopes have empty centers: do not use
    // their AABBs as collision solids. Thin bounded roof/floor panels are safe.
    if((dx>7||dz>7)&&h>.20)return;
    if(dx>15||dz>15)return;
    forumSafetyBoxes.push({name:mesh.name,box});
  });
}
function eyeInBox(p,b,r=.18){
  return p.x>b.min.x-r&&p.x<b.max.x+r&&p.y>b.min.y-r
    &&p.y<b.max.y+r&&p.z>b.min.z-r&&p.z<b.max.z+r;
}
function rayBoxNear(p,dir,b,reach){
  let entry=0,exit=reach;
  for(const ax of ["x","y","z"]){
    const speed=dir[ax];
    if(Math.abs(speed)<1e-7){
      if(p[ax]<b.min[ax]-.13||p[ax]>b.max[ax]+.13)return false;
      continue;
    }
    const a=(b.min[ax]-.13-p[ax])/speed;
    const z=(b.max[ax]+.13-p[ax])/speed;
    entry=Math.max(entry,Math.min(a,z));
    exit=Math.min(exit,Math.max(a,z));
    if(exit<entry)return false;
  }
  return exit>=0&&entry<reach;
}
const eyeSafetyDirection=new Vector3(),eyeSafetyScratch=new Vector3();
function safeCameraInForum(point,target){
  if(!forumSafetyBoxes.length)return {position:point,blocked:0,occluded:0,correction:0};
  eyeSafetyDirection.subVectors(target,point).normalize();
  const offsets=[[0,0,0],[-.36,0,0],[.36,0,0],[0,0,-.36],[0,0,.36],
     [-.62,0,-.4],[.62,0,-.4],[-.62,0,.4],[.62,0,.4],
     [-.95,0,0],[.95,0,0],[0,.38,0]];
  let best=null;
  for(const [dx,dy,dz] of offsets){
    const candidate=eyeSafetyScratch.set(point.x+dx,point.y+dy,point.z+dz);
    const penetrations=forumSafetyBoxes.filter(o=>eyeInBox(candidate,o.box));
    const occlusions=forumSafetyBoxes.filter(o=>rayBoxNear(candidate,eyeSafetyDirection,o.box,1.15));
    const cost=Math.hypot(dx,dy,dz)+penetrations.length*12+occlusions.length*3;
    if(!best||cost<best.cost)best={position:candidate.clone(),cost,penetrations,occlusions,correction:Math.hypot(dx,dy,dz)};
    if(!penetrations.length&&!occlusions.length)break;
  }
  return {position:best.position,blocked:best.penetrations.length,
    occluded:best.occlusions.length,correction:best.correction,
    names:[...best.penetrations,...best.occlusions].map(o=>o.name).slice(0,7)};
}

// Resolve actual Z-fighting instead of pushing *all* white architecture
// with the same polygon offset. Only suppress coincident, large, opaque
// planar sheets that occupy the same world plane.
const sheetRepair={compared:0,removed:[],kept:0,glassSinglePass:true,planeThreshold:.24};
function removeCoplanarDuplicateSheets(building){
  const panels=[];
  building.updateMatrixWorld(true);
  building.traverse(mesh=>{
    if(!mesh.isMesh||!mesh.visible||!mesh.geometry)return;
    const name=modelName(mesh.name);
    // Include overlapping *glass panels* in the double-sheet test; they
    // are otherwise liable to sort in opposite orders while the camera moves.
    if(/mullion|door|handle|pull|tree|maple|stair|tread|railing|handrail|cross|plant|leaf/i.test(name))return;
    const b=meshWorldBox(mesh);if(!b)return;
    const sz=b.getSize(new Vector3()),dims=[sz.x,sz.y,sz.z];
    const axis=dims.indexOf(Math.min(...dims));
    const other=[0,1,2].filter(i=>i!==axis);
    if(dims[axis]>.24||dims[other[0]]*dims[other[1]]<1.8)return;
    const plane=(b.min.getComponent(axis)+b.max.getComponent(axis))*.5;
    panels.push({mesh,b,dims,axis,plane,other,
      surfaceArea:dims[other[0]]*dims[other[1]]});
  });
  panels.sort((a,b)=>b.surfaceArea-a.surfaceArea);
  const planeBuckets=new Map();
  for(const a of panels){
    const group=/(glass|glazing|window pane|skylight)/i.test(modelName(a.mesh.name))?'glass':'opaque';
    const key=group+':'+a.axis+':'+Math.round(a.plane/.018);
    // Adjacent bucket keys catch planes near a rounding boundary.
    let duplicate=null;
    for(const j of [-1,0,1]){
      const members=planeBuckets.get(group+':'+a.axis+':'+(Math.round(a.plane/.018)+j))||[];
      for(const b of members){
        if(Math.abs(a.plane-b.plane)>.025)continue;
        const [u,v]=a.other;
        const overlapU=Math.max(0,Math.min(a.b.max.getComponent(u),b.b.max.getComponent(u))
          -Math.max(a.b.min.getComponent(u),b.b.min.getComponent(u)));
        const overlapV=Math.max(0,Math.min(a.b.max.getComponent(v),b.b.max.getComponent(v))
          -Math.max(a.b.min.getComponent(v),b.b.min.getComponent(v)));
        if(overlapU*overlapV/a.surfaceArea>.985){duplicate=b;break;}
      }
      if(duplicate)break;
    }
    sheetRepair.compared++;
    if(duplicate){
      a.mesh.visible=false;a.mesh.castShadow=false;
      sheetRepair.removed.push({hidden:a.mesh.name,under:duplicate.mesh.name});
    }else{
      if(!planeBuckets.has(key))planeBuckets.set(key,[]);
      planeBuckets.get(key).push(a);
      sheetRepair.kept++;
    }
  }
}
function cleanOpenPublicSpaces(building){
  building.updateMatrixWorld(true);
  building.traverse(object=>{
    if(!object.isMesh)return;
    const n=modelName(object.name);
    if(/roof (north|west).*ghost.cutaway/i.test(n)){
      ghostRoofMeshes.push(object);
      return;
    }
    // Earlier wide regex cut away inhabited gallery floors, creating the
    // apparent giant pit and leaving individual stair treads floating.
    // Only the original narrow low soffit is a nonstructural obstruction.
    const conceptualOverhead=/^v13 west mid .*curved solid room.edge fascia/i;
    // Selected conceptual mid-level plates created low hanging ceilings across
    // the open C forum. Remove these only, never V19 terrace steps or V13 high.
    const routesidePost=/^v11 support post.*(?:northwest gallery inner|west mid public edge|north mid public edge)/i;
    if(conceptualOverhead.test(n)||routesidePost.test(n)){
      object.visible=false;object.castShadow=false;removedObstructions.push(object.name);
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
    if (/^Model frame|study silhouette|construction guide|debug marker/i.test(object.name)) {
      object.visible = false;
      return;
    }
    const originalMaterial=object.material;
    if (registerMapleSource(object)) {
      object.castShadow = true;
      object.receiveShadow = true;
      return;
    }
    object.material = chooseFinish(object.name, originalMaterial);
    const part = modelName(object.name);
    if (/^roof/i.test(part) && object.material?.color)
      originalStructuralMaterials.set(object.material,object.material.color.clone());
    const isGlazing = /glass|glazing|glazed|window pane/.test(part);
    if (isGlazing) {
      object.material.transparent = true;
      object.material.depthWrite = false;
      object.material.forceSinglePass=true;
      object.renderOrder = 2;
    }
    object.castShadow = !isGlazing && object.material !== finishes.leaves;
    object.receiveShadow = true;
  });
  cleanOpenPublicSpaces(building);
  removeCoplanarDuplicateSheets(building);
  connectUpperStairTreads(building);
  removeHeadHeightHazards(building);
  buildCameraSafetyBoxes(building);
  window.__churchSurfaceAudit=sheetRepair;
  window.__churchUpperStairAudit=upperStairAudit;
  scene.add(building);
  const sweptClearance=forumPathTimes().map(t=>{
    const step=positionAlongRoute(t);
    const safe=safeCameraInForum(new Vector3(...step.p),new Vector3(...step.look));
    return {t,blocked:safe.blocked,occluded:safe.occluded,
      displacement:+safe.correction.toFixed(3),names:safe.names||[]};
  });
  window.__churchRouteClearanceAudit={
    headHazardsRemoved:eliminatedHeadHazards,
    collisionBoxes:forumSafetyBoxes.length,
    sampledFrames:sweptClearance.length,
    blockedFrames:sweptClearance.filter(x=>x.blocked>0||x.occluded>0),
    maxCameraDisplacement:Math.max(...sweptClearance.map(x=>x.displacement)),
    correctedSamples:sweptClearance.filter(x=>x.displacement>.001).length
  };

  // Read-only screen-space diagnostics: identify any unlabeled GLB component
  // visible where a floating handle was reported. No on-screen UI or overlay.
  window.__churchMeshProbe = (screenX,screenY,rad=100)=>{
    const found=[];
    scene.updateMatrixWorld(true);
    scene.traverse(object=>{
      if(!object.isMesh || !object.visible || !object.geometry) return;
      if(!object.geometry.boundingBox) object.geometry.computeBoundingBox();
      const b=object.geometry.boundingBox;
      if(!b)return;
      const world=b.getCenter(new Vector3()).applyMatrix4(object.matrixWorld);
      const clip=world.clone().project(camera);
      const px=(clip.x+1)*450,py=(1-clip.y)*300;
      const distance=Math.hypot(px-screenX,py-screenY);
      if(distance>rad || clip.z>1 || clip.z< -1)return;
      const sz=b.getSize(new Vector3());
      found.push({name:object.name,px:Math.round(px),py:Math.round(py),
        distance:Math.round(distance),world:[world.x,world.y,world.z].map(v=>+v.toFixed(3)),
        localSize:[sz.x,sz.y,sz.z].map(v=>+v.toFixed(3)),
        material:object.material?.name||null});
    });
    return found.sort((a,b)=>a.distance-b.distance).slice(0,60);
  };
  addNativeLandscape(building);
  connectArchitecturalDoors(building);
}

// The touring camera belongs to the actual 3D world, not the exterior
// maquette orbit camera. All positions are metres in GLB scene coordinates.
// Coordinate-verified route, following the actual openings.
// Entrance x8.16..10.54 z0; south inner glass z-6;
// courtyard x6..12 z-6..-12; east sliding door x12 z-7.5..-10.5;
// rear sanctuary door x12 z-15.25..-14.15; north court glass z-12.
// Restored from the user's approved Nov 20 2026 actual walking itinerary:
// SOUTH full facade -> tall door -> vestibule -> courtyard -> NORTH court
// glass -> north chapel public rear entrance -> walk from chapel REAR toward
// SOUTH cross and pulpit -> SOUTH staff door -> SOUTH foyer -> WEST cafe ->
// C-shaped sunken congregational terraces -> NORTH -> V26 upper stairs ->
// THIRD-floor gallery overlooking central court and red maple ->
// RISING SKY panorama. Not the improvised east-glass shortcut of R1.
// Eye heights follow the source GLB actual inhabited floors (metres).
// Segment durations are reconstructed because original Sites front-end
// timing source is not recoverable; route order is original user-approved.
const route = [
  { at:  0, p:[16.0,7.1,20.0], look:[9.0,3.5,-2.8] },     // full front
  { at: 12, p:[9.4,2.0,8.0],   look:[9.35,2.3,0.0] },     // approach
  { at: 22, p:[9.4,1.76,1.0],  look:[9.35,1.8,-5.4] },    // south opening
  { at: 31, p:[9.0,1.76,-4.8], look:[9.0,1.85,-8.9] },    // vestibule
  { at: 40, p:[9.0,1.78,-8.9], look:[7.4,2.3,-10.3] },    // courtyard maple
  { at: 47, p:[9.0,1.76,-11.25],look:[9.0,1.8,-13.2] },  // north court glass
  { at: 55, p:[9.1,1.77,-13.0],look:[11.6,1.7,-14.7] },  // level route
  { at: 63, p:[11.45,1.76,-14.7],look:[14.4,1.7,-14.7] },// north public door
  { at: 73, p:[13.4,1.77,-14.7],look:[15.0,2.0,-6.4] },  // sanctuary rear
  { at: 84, p:[15.0,1.78,-10.6],look:[15.0,2.4,-0.15] }, // aisle, cross
  { at: 95, p:[15.0,1.76,-5.2],look:[15.0,3.65,-0.1] }, // pulpit/cross light
  { at:103, p:[13.25,1.76,-2.14],look:[12.0,1.8,-2.14]},// south staff door
  { at:111, p:[10.7,1.76,-2.14],look:[7.2,1.7,-4.4] },   // south hall
  { at:122, p:[6.6,1.76,-4.5],look:[4.8,0.6,-6.0] },    // south->west opening
  { at:132, p:[5.0,1.45,-5.9],look:[3.1,0.0,-7.6] },    // broad descent
  { at:143, p:[3.5,0.35,-7.8],look:[3.9,-0.25,-10.1] },   // -1.50 piazza
  { at:154, p:[2.6,-0.38,-9.7],look:[4.9,-0.25,-11.3] },  // -2.10 cafe
  { at:165, p:[3.5,0.08,-11.5],look:[5.9,0.45,-13.6] },  // C-shaped return
  { at:176, p:[4.6,1.1,-14.65],look:[6.2,2.2,-16.0]},  // north terraces
  // The V26 staircase follows z=-16.82. Its occupied third-floor
  // slab begins at z=-16.05: keep the visitor NORTH of that soffit while
  // climbing instead of passing through the low floor/ceiling cavity.
  { at:187, p:[6.0,2.7,-16.84],look:[8.5,2.68,-16.83]}, // keep stair treads in view, not soffit
  { at:199, p:[8.3,3.90,-16.84],look:[10.7,3.78,-16.84]},// level sightline, no ceiling stare
  { at:202, p:[9.3,4.35,-16.71],look:[9.5,4.2,-15.6]},  // turn before crossing upper threshold
  { at:205, p:[10.15,4.78,-16.52],look:[8.0,2.4,-9.4]},// atrium visible before upper room
  { at:211, p:[10.9,5.04,-13.8],look:[8.0,1.65,-9.3]}, // continuous courtyard reveal
  { at:223, p:[10.65,5.03,-13.0],look:[7.65,1.30,-9.65]}, // red maple reveal
  { at:236, p:[9.0,12.4,-9.0],look:[9.0,1.8,-9.0]},   // rising sky
  { at:246, p:[18.2,6.8,17.7],look:[13.8,3.35,-2.6]},// more intimate front vista
  { at:251, p:[18.2,6.8,17.7],look:[13.8,3.35,-2.6]} // same stable dusk cross finale
];

// The original scenes each played their own sunrise-to-sunset time lapse.
// Keep a discrete light-day per location rather than jumping from winter
// morning to afternoon at the north sanctuary door.
const daylightChapters = [
  [0,31], [31,63], [63,103], [103,132],
  [132,176], [176,223], [223,251]
];
function daylightAt(t) {
  // V4.1: approximately TWELVE seconds per full day's sunlight, repeated
  // continuously while the camera moves through every major interior scene.
  // The phase is periodic: the next day begins at the same solar angle.
  const DAY_SECONDS=22;
  return ((t / DAY_SECONDS + .065) % 1 + 1) % 1;
}
function updateDaylight(t,duration) {
  const phase=daylightAt(t);
  // Each chapter runs a full sunrise-day-sunset-night cycle. A circular
  // solar trajectory makes the boundary 23:59 -> 00:00 continuous and
  // prevents the previously rejected bright sunlight teleport.
  const angle=phase*Math.PI*2;
  const solar=Math.max(0,Math.sin(angle));
  // A smooth day-to-night irradiance curve, with a soft low-sun shoulder.
  const daylight=solar*solar*(3-2*solar);
  const season=Math.min(1,Math.max(0,t/duration));
  // Sun moves SOUTH from screen left to screen right while it is up;
  // its return happens below the horizon during night.
  sun.position.set(9-25*Math.cos(angle),1.3+25*Math.sin(angle),25);
  sun.target.position.set(15,2.7,-5);
  sun.target.updateMatrixWorld();
  const winter=Math.max(0,Math.min(1,(season-.73)/.16));
  const morningEvening=1-solar;
  sun.color.setRGB(
    1.0-.21*winter,
    1.0-.08*morningEvening-.09*winter,
    .98-.21*morningEvening+.015*winter
  );
  sun.intensity=Math.max(0.035, .08+1.65*daylight-.10*winter);
  // Prevent a constant hard shaft of light remaining through the night.
  sanctuaryLight.intensity=.10+.22*daylight;
  const sunlight=daylight*daylight*(3-2*daylight);
  // Project the cross from its REAL height to the inhabited floor:
  // high summer sun -> near altar; low sun -> elongated toward rear pews.
  const solarFall=Math.max(9.8,25*solar-1.4);
  const groundTravel=Math.min(9.7,Math.max(3.2,crossAperture.y*30/solarFall));
  apertureGlow.material.opacity=.040+.21*sunlight;
  crossFloorLight.material.opacity=.08+.40*sunlight;
  crossFloorLight.position.z=-groundTravel;
  crossFloorLight.position.x=crossAperture.x+
    Math.max(-1.2,Math.min(1.2,crossAperture.y*(6+25*Math.cos(angle))/solarFall));
  crossFloorLight.scale.set(.86+groundTravel*.025, .80+groundTravel*.045,1);
  // Real surfaces now catch a moving warm cone and reflected floor light,
  // instead of relying entirely on alpha-blended decorative cards.
  crossPortalKey.intensity=21*sunlight;
  crossPortalKey.target.position.set(crossFloorLight.position.x,.04,crossFloorLight.position.z);
  crossPortalKey.target.updateMatrixWorld();
  crossWallBounce.intensity=9*sunlight;
  crossWallBounce.position.set(crossFloorLight.position.x,.24,crossFloorLight.position.z);
  crossWallBounce.target.updateMatrixWorld();
  // Reorient all atmosphere slices to the true solar path, not fixed cards.
  crossRayTarget.set(crossFloorLight.position.x,.16,crossFloorLight.position.z);
  crossRayDirection.subVectors(crossRayTarget,crossRayOrigin);
  const beamLength=crossRayDirection.length();
  crossRayUnit.copy(crossRayDirection).normalize();
  crossRayMidpoint.copy(crossRayOrigin).addScaledVector(crossRayDirection,.5);
  for(const ray of crossAirVolumes){
    ray.position.copy(crossRayMidpoint);
    ray.quaternion.setFromUnitVectors(localBeamAxis,crossRayUnit);
    ray.rotateY(ray.userData.rotationalSlice);
    ray.scale.y=beamLength/10;
  }
  // Preserve the near-field exposure headroom from R18 while restoring
  // the gentle honey-gold scattering lost after the highlight correction.
  crossAirMaterial.uniforms.uLight.value=.006+.159*sunlight;
  crossAirMaterial.uniforms.uTint.value.set(
    1,.78+.12*daylight,.62+.20*daylight
  );
  crossAirMaterial.uniforms.uTime.value=t;
  // Daylight changes; the wall PBR base colors remain from the original GLB.
  // Colour temperature follows the time of day, not arbitrary flashing:
  // cool twilight -> neutral daylight -> muted warm sunset.
  const dusk=1-daylight;
  skyFill.color.setRGB(.81+.11*daylight,.86+.10*daylight,1);
  skyFill.groundColor.setRGB(.68+.09*daylight,.67+.10*daylight,.65+.11*daylight);
  ambientFill.color.setRGB(.71+.13*daylight,.80+.10*daylight,.93+.04*daylight);
  ambientFill.intensity=.19+.25*daylight;
  bounceFill.intensity=.18+.22*daylight;
  bounceFill.color.setRGB(1,.86+.10*daylight,.77+.19*daylight);
  skyFill.intensity=.86+.20*daylight;
  // Gentle exposure adaptation preserves wall relief and the white chapel.
  // Lens-like approach compensation: close chapel views keep detail in the
  // true slit and scattered light; walls remain their original white PBR.
  const cp=positionAlongRoute(t).p;
  const lensDistance=Math.hypot(
    cp[0]-crossAperture.x,
    cp[1]-crossAperture.y,
    cp[2]-crossAperture.z
  );
  const lensNear=Math.max(0,Math.min(1,(10-lensDistance)/6));
  renderer.toneMappingExposure=(.86+.11*daylight)*(1-.16*lensNear*sunlight);
  // Final dusk: day gently fades, then a warm light from INSIDE the house
  // awakens the real cross opening, carrying a soft beam outward.
  const twilight=eveningSky(t);
  const lit=ease((t-239)/9);
  if(twilight>0){
    sun.intensity*=1-.88*twilight;
    skyFill.intensity*=1-.57*twilight;
    ambientFill.intensity*=1-.45*twilight;
    bounceFill.intensity*=1-.30*twilight;
    // A white facade stays legible against first-night blue, not black.
    renderer.toneMappingExposure*=1+.035*twilight;
    // Daytime sunlight entering the cross ends before the final outward glow.
    apertureGlow.material.opacity*=1-twilight;
    crossFloorLight.material.opacity*=1-twilight;
    crossPortalKey.intensity*=1-twilight;
    crossWallBounce.intensity*=1-twilight;
    crossAirMaterial.uniforms.uLight.value*=1-twilight;
  }
  finaleInteriorLamp.intensity=12*lit;
  finaleExteriorLamp.intensity=11*lit;
  finaleFacadeBounce.intensity=19*lit;
  finaleCrossCore.material.opacity=.36*lit;
  finaleCrossHalo.material.opacity=.20*lit;
  finaleGroundPool.material.opacity=.24*lit;
  finaleAirMaterial.uniforms.uLight.value=.15*lit;
  finaleAirMaterial.uniforms.uTime.value=t;
  window.__churchFinaleAudit={
    active:t>=232,twilight:+twilight.toFixed(4),
    crossCore:finaleCrossCore.material.opacity,
    interiorLamp:finaleInteriorLamp.intensity,
    exteriorLamp:finaleExteriorLamp.intensity,
    facadeBounce:finaleFacadeBounce.intensity,
    groundPool:finaleGroundPool.material.opacity,
    outwardBeam:finaleAirMaterial.uniforms.uLight.value,
    skyGradient:scene.background===finalSkyTexture,
    direction:"inside-to-outside",
    mode:"first-dark-evening"
  };
  updateMapleSeason(t,duration);
}

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

// Optional preview entry point for inspecting a finished chapter in motion.
// Does not affect the default door-to-courtyard-to-chapel-to-gallery itinerary.
const entryParams=new URLSearchParams(location.search);
const requestedStart=entryParams.get("startAt");
const startSeconds=requestedStart!==null&&Number.isFinite(Number(requestedStart))
  ?Math.min(route[route.length-1].at,Math.max(0,Number(requestedStart))):0;
let elapsed = startSeconds, previousFrame = 0, isVisible = !document.hidden;
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
function animate(now,forcedTime=null) {
  if(forcedTime===null)requestAnimationFrame(animate);
  if (!isVisible) { previousFrame = now; return; }
  const dt = previousFrame ? Math.min(0.045, Math.max(0, (now - previousFrame) / 1000)) : 0;
  previousFrame = now;
  if (!prefersReducedMotion) elapsed += dt;
  const duration = route[route.length - 1].at;
  // Do not reset early: perform the entire route, including the third level
  // and the final aerial, before restarting after a short panoramic hold.
  // A deterministic visual QA position, without adding any on-screen text.
  const params = new URLSearchParams(location.search);
  const proof = params.get("proofFrame");
  const t=Number.isFinite(forcedTime)
    ? Math.min(duration,Math.max(0,forcedTime))
    : proof!==null && Number.isFinite(Number(proof))
      ? Math.min(duration,Math.max(0,Number(proof)))
      : (prefersReducedMotion ? duration : Math.min(duration,elapsed % (duration + 20)));
  updateDaylight(t,duration);
  window.__churchFrameAudit={
    at:t,daylight:daylightAt(t),
    crossHeight:crossAperture.y,
    apertureOpacity:apertureGlow.material.opacity,
    floorOpacity:crossFloorLight.material.opacity,
    floorPosition:[crossFloorLight.position.x,crossFloorLight.position.y,crossFloorLight.position.z],
    portalIntensity:crossPortalKey.intensity,
    reflectedIntensity:crossWallBounce.intensity,
    airStrength:crossAirMaterial.uniforms.uLight.value,
    exposure:renderer.toneMappingExposure,
    beamAlignment:localBeamAxis.clone()
      .applyQuaternion(crossAirVolumes[0].quaternion).dot(crossRayUnit)
  };
  // Remove ghost-cutaway roof panels from ALL inhabited/terraced chapters;
  // keep the actual east/south roof and full exterior profile intact.
  for(const roof of ghostRoofMeshes) roof.visible = t<20 || t>232;
  window.__churchSpatialAudit={
    removed:removedObstructions.length,
    names:removedObstructions,
    ghostRoofs:ghostRoofMeshes.length,
    ghostRoofVisible:ghostRoofMeshes.filter(x=>x.visible).length
  };
  const sample = positionAlongRoute(t);
  lookAtVector.set(sample.look[0],sample.look[1],sample.look[2]);
  camera.position.set(sample.p[0],sample.p[1],sample.p[2]);
  if(isInteriorClearanceTime(t)){
    const safe=safeCameraInForum(camera.position,lookAtVector);
    camera.position.copy(safe.position);
    cameraSafetyReport.samples++;
    if(safe.correction>.001)cameraSafetyReport.corrected++;
    cameraSafetyReport.penetrations=safe.blocked;
    cameraSafetyReport.forwardOcclusions=safe.occluded;
    cameraSafetyReport.objects=safe.names||[];
  }
  window.__churchSafetyAudit={
    at:t,headHazardsRemoved:eliminatedHeadHazards.length,
    cameraPenetrations:isInteriorClearanceTime(t)?cameraSafetyReport.penetrations:0,
    forwardOcclusions:isInteriorClearanceTime(t)?cameraSafetyReport.forwardOcclusions:0,
    cameraPosition:[camera.position.x,camera.position.y,camera.position.z].map(v=>+v.toFixed(3)),
    corrected:isInteriorClearanceTime(t)?cameraSafetyReport.corrected:0,
    collidingObjects:isInteriorClearanceTime(t)?cameraSafetyReport.objects:[],
    boxes:forumSafetyBoxes.length
  };
  const distance = camera.position.distanceTo(lookAtVector);
  lookAtVector.x += Math.sin(yawOffset) * Math.min(7, distance * 0.6);
  lookAtVector.y -= pitchOffset * Math.min(5, distance * 0.5);
  camera.lookAt(lookAtVector);
  if (!pointerDown) {
    yawOffset *= Math.pow(0.89, dt * 60);
    pitchOffset *= Math.pow(0.89, dt * 60);
  }
  if (doorsAttached) {
    entranceHinge.rotation.y = 1.5 * ease((t - 11) / 8);
    innerSouthSlider.position.x = -2.14 * ease((t - 24) / 6);
    // The east courtyard event entrance stays closed: approved entry
    // to the chapel is via the NORTH PUBLIC rear west-facing door.
    eastChapelSlider.position.z = 0;
    northCourtSlider.position.x = 2.15 * ease((t - 41) / 5);
    rearSanctuaryHinge.rotation.y = 1.43 * ease((t - 56) / 6);
    staffSanctuaryHinge.rotation.y = -1.4 * ease((t - 95) / 7);
  }
  renderer.render(scene, camera);
}

loadArchitecture().then(() => {
  document.body.classList.add("ready");
  // Direct, synchronous proof rendering: capture the requested actual
  // WebGL frame without reloading the architecture or guessing RAF timing.
  window.__churchRenderProofFrame=at=>animate(performance.now(),at);
  requestAnimationFrame(animate);
}).catch(error => {
  console.error("Virtual church model load failed", error);
  document.body.classList.add("failed");
});
