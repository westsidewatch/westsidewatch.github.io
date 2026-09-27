const INHERITANCE={
 'middle-bronze':{from:'chalcolithic-early-bronze',retain:.18},
 'late-bronze-iron1':{from:'middle-bronze',retain:.34},
 'david-solomon':{from:'late-bronze-iron1',retain:.42},
 'late-first-temple':{from:'david-solomon',retain:.55},
 'babylonian-destruction':{from:'late-first-temple',retain:1,ruin:true},
 'persian-nehemiah':{from:'late-first-temple',retain:.22,ruin:true},
 'hellenistic-hasmonean':{from:'persian-nehemiah',retain:.38},
 'herodian-jesus':{from:'hellenistic-hasmonean',retain:.44},
 'roman-destruction':{from:'herodian-jesus',retain:1,ruin:true},
 'aelia':{from:'herodian-jesus',retain:.14,ruin:true},
 'byzantine':{from:'aelia',retain:.46},
 'early-islamic':{from:'byzantine',retain:.48},
 'crusader':{from:'early-islamic',retain:.35},
 'ayyubid-mamluk':{from:'crusader',retain:.42},
 'ottoman':{from:'ayyubid-mamluk',retain:.56},
 'outside-walls':{from:'ottoman',retain:.72},
 'modern':{from:'outside-walls',retain:.78}
};
export function inheritanceFor(phaseId){return INHERITANCE[phaseId]||null}
export function applyInheritedMorphology(runtime,{retain=0,ruin=false,progress=1}={}){if(!runtime?.meshes)return;const p=Math.max(0,Math.min(1,progress)),keep=Math.max(0,Math.min(1,retain));runtime.inherited=true;runtime.inheritanceRetain=keep;runtime.inheritanceRuin=ruin;for(let i=0;i<runtime.meshes.length;i++){const mesh=runtime.meshes[i],meta=mesh.userData?.phase2;if(!meta)continue;const threshold=i/Math.max(1,runtime.meshes.length-1),survives=threshold<=keep;mesh.visible=survives;if(!survives)continue;const inheritedScale=ruin?.18:.72+.28*p;mesh.scale.y=Math.max(.02,inheritedScale);mesh.material.opacity=ruin?.34:.42+.42*p;mesh.material.transparent=true;mesh.userData.inherited=true}}
