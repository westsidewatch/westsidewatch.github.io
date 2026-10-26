import * as THREE from 'three';
// Fit the authored period envelope above the phase caption, with aspect-aware margins.
export function fitCityOverview({points,aspect,fov=34,landscape=false}){
 if(!points?.length||!points.every(p=>[p.x,p.y,p.z].every(Number.isFinite))||!(aspect>0)||!(fov>0&&fov<170))throw new Error('Invalid city overview inputs');
 const bounds=new THREE.Box3().setFromPoints(points),centre=bounds.getCenter(new THREE.Vector3()),direction=new THREE.Vector3(.85,.9,1.25).normalize(),right=new THREE.Vector3().crossVectors(new THREE.Vector3(0,1,0),direction).normalize(),up=new THREE.Vector3().crossVectors(direction,right).normalize();
 const tan=Math.tan(THREE.MathUtils.degToRad(fov/2)),horizontal=(landscape ? .92 : .82)*aspect*tan,vertical=(landscape ? .88 : .52)*tan;
 let distance=80;
 for(const p of points){const q=new THREE.Vector3(p.x,p.y,p.z).sub(centre);distance=Math.max(distance,q.dot(direction)+Math.abs(q.dot(right))/horizontal,q.dot(direction)+Math.abs(q.dot(up))/vertical);}
 distance*=1.06;
 // A lower target puts the district's visual centre above the lower caption.
 const target=centre.clone().addScaledVector(up,-(landscape ? .08 : .2)*distance*tan),position=target.clone().addScaledVector(direction,distance);
 return{target,position,distance,bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()},authority:'authored-period-envelope-not-historical-city-boundary'};
}
