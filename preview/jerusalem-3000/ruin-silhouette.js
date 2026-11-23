const clamp=v=>Math.max(0,Math.min(1,v));
// Stable spatial presentation field, not an attack direction or excavated debris.
export function ruinSilhouetteProfile(x,z){const field=(Math.sin(x*.037+Math.cos(z*.021)*1.7)+Math.cos(z*.049-x*.013)+2)/4;return{delay:.28*field,residual:.06+.12*field};}
export function stagedRuinAmount(amount,profile){if(amount<=0)return 0;if(amount>=1)return 1;const t=clamp((amount-profile.delay)/(1-profile.delay));return t*t*(3-2*t);}
export function ruinHeightFactor(amount,x,z,profile=ruinSilhouetteProfile(x,z)){if(amount<=0)return 1;const progress=stagedRuinAmount(amount,profile),residual=ruinSilhouetteProfile(x,z).residual;return 1-progress*(1-residual);}
