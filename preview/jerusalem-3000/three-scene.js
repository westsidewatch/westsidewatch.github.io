import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/controls/OrbitControls.js';

// Direct Jerusalem port of threejs-architecture-effects/PagodaThreeScene:
// PerspectiveCamera + WebGLRenderer + OrbitControls + one shared build clock.
export function mountJerusalemThreeScene(mount,{onReady}={}){
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(34,1,.1,18000);
  camera.position.set(3800,2250,5700);
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,innerWidth<700?1.5:2));
  renderer.setClearColor(0xf4f1e9,0);
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.shadowMap.autoUpdate=false;
  mount.replaceChildren(renderer.domElement);

  scene.add(new THREE.HemisphereLight(0xfaf7ef,0x706a5c,.72));
  const key=new THREE.DirectionalLight(0xfff2e2,2.4);key.position.set(-2200,3800,3000);key.castShadow=true;
  key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-4500;key.shadow.camera.right=4500;key.shadow.camera.top=4500;key.shadow.camera.bottom=-4500;key.shadow.camera.near=50;key.shadow.camera.far=12000;key.shadow.normalBias=.025;key.shadow.bias=-.00015;key.shadow.radius=3;
  key.target.position.set(0,0,0);scene.add(key,key.target);
  const fill=new THREE.DirectionalLight(0xe5eced,.55);fill.position.set(2500,1800,-1000);scene.add(fill);
  const rim=new THREE.DirectionalLight(0xfff4de,.7);rim.position.set(-1200,3000,-2400);scene.add(rim);

  const controls=new OrbitControls(camera,renderer.domElement);
  controls.target.set(0,0,0);controls.enableDamping=true;controls.dampingFactor=.075;controls.enablePan=true;
  controls.minDistance=1200;controls.maxDistance=11000;controls.minPolarAngle=.35;controls.maxPolarAngle=Math.PI*.51;
  controls.autoRotate=true;controls.autoRotateSpeed=.32;

  const root=new THREE.Group();root.name='jerusalem-temporal-city';scene.add(root);
  const terrain=new THREE.Mesh(new THREE.PlaneGeometry(7600,7600,48,48),new THREE.MeshStandardMaterial({color:0xc8b99e,roughness:.96,metalness:0}));
  terrain.rotation.x=-Math.PI/2;terrain.receiveShadow=true;terrain.name='terrain-pending-canonical-dem';root.add(terrain);

  const buildProgress={value:0};
  const cityMaterial=new THREE.MeshStandardMaterial({color:0xb9a486,roughness:.9,metalness:0});
  const pieces=[];
  function addPiece(x,z,w,d,h,start){
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),cityMaterial);mesh.position.set(x,h/2,z);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.build={start,duration:.035,lift:220};mesh.visible=false;root.add(mesh);pieces.push(mesh);
  }
  // Temporary geometry consumer only; historical geometry ledgers replace these boxes.
  for(let z=-1900,zi=0;z<=1900;z+=380,zi++)for(let x=-1900,xi=0;x<=1900;x+=380,xi++){
    const r=Math.hypot(x*.82,z);if(r>2300)continue;const start=Math.min(.97,(zi*11+xi)/(11*11));addPiece(x,z,260,250,90+((zi+xi)%5)*35,start);
  }
  function setBuildProgress(v){buildProgress.value=Math.max(0,Math.min(1,v));for(const mesh of pieces){const b=mesh.userData.build,t=Math.max(0,Math.min(1,(buildProgress.value-b.start)/b.duration));mesh.visible=t>0;if(!mesh.visible)continue;const settle=Math.sin(t*Math.PI*2)*(1-t)*(1-t)*.035;mesh.position.y=mesh.geometry.parameters.height/2+b.lift*((1-t)**3-settle);}}

  let needsFrame=true,lastNow=performance.now(),raf=0;
  controls.addEventListener('change',()=>{needsFrame=true});
  const resize=()=>{const w=Math.max(1,mount.clientWidth),h=Math.max(1,mount.clientHeight);renderer.setSize(w,h,false);camera.aspect=w/h;camera.fov=camera.aspect<.58?39:34;camera.updateProjectionMatrix();needsFrame=true};
  const ro=new ResizeObserver(resize);ro.observe(mount);resize();
  function render(now){const dt=Math.min((now-lastNow)/1000,.1);lastNow=now;const changed=controls.update(dt);if(!document.hidden&&(needsFrame||changed||controls.autoRotate)){renderer.shadowMap.needsUpdate=true;renderer.render(scene,camera);needsFrame=false}raf=requestAnimationFrame(render)}
  raf=requestAnimationFrame(render);onReady?.();
  return {scene,camera,renderer,controls,root,setBuildProgress,dispose(){cancelAnimationFrame(raf);ro.disconnect();controls.dispose();terrain.geometry.dispose();terrain.material.dispose();pieces.forEach(p=>p.geometry.dispose());cityMaterial.dispose();renderer.dispose();renderer.domElement.remove();}};
}
