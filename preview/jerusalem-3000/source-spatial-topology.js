// Existing source anchors are coarse zones, never measured footprints or new meshes.
const ORIGIN={lat:31.778,lon:35.235},DEG=Math.PI/180,R=6378137;
export function sourceSpatialTopology(object,terrain){
 const s=object.spatial;
 if(!s||s.frame!=='local-enu'||String(s.registration).includes('withheld')||String(object.geometry?.status).includes('withheld'))return null;
 // This adapter deliberately supports only the declared Herodian source pack.
 if(!String(object.id).startsWith('j3k:object:')||!String(s.registration).startsWith('provisional-'))return null;
 if(!terrain?.grid?.origin||typeof terrain.heightAtWorld!=='function')return null;
 if(terrain.grid.origin.lat!==ORIGIN.lat||terrain.grid.origin.lon!==ORIGIN.lon)throw new Error('Source anchor canonical origin mismatch');
 const {east,north}=s.enuMetres||{},a=s.anchor;
 if(![east,north,a?.lat,a?.lon].every(Number.isFinite))throw new Error(`Invalid source anchor ${object.id}`);
 const expectedX=(a.lon-ORIGIN.lon)*DEG*R*Math.cos(ORIGIN.lat*DEG),expectedN=(a.lat-ORIGIN.lat)*DEG*R;
 if(Math.hypot(east-expectedX,north-expectedN)>1)throw new Error(`Source anchor geographic/ENU mismatch ${object.id}`);
 if(!Number.isFinite(terrain.heightAtWorld(east,-north)))throw new Error(`Source anchor outside canonical DEM ${object.id}`);
 return {authority:'source-provisional-anchor-v1',frame:'canonical-dem-enu',point:{x:east,z:-north},confidence:'inferred',representation:'source-provisional-zone-not-footprint',registration:s.registration,accuracy:s.accuracy,anchor:{...a},geometryVerified:false,ancientGroundVerified:false};
}
