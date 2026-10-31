import {herodianRitualLayout} from './temple-precinct-layout.js';
// Model metres. A chosen 0.525 m cubit, not an assertion of a unique ancient cubit.
export const HERODIAN_DIMENSIONS=Object.freeze({
 cubitMetres:.525,
 relativeCourtLevels:Object.freeze(herodianRitualLayout(.525).levels),
 courtLevelAuthority:"selected-Middot2:5-6-tradition-relative-to-authored-womens-court-datum-not-ancient-survey",
 platform:Object.freeze({eastWest:300,northSouth:480,pavingThickness:.8,authority:'rounded-14.4ha-envelope-not-surveyed-rectangle'}),
 sanctuary:Object.freeze({eastWest:52.5,bodyNorthSouth:36.75,porchNorthSouth:52.5,height:52.5}),
 priestCourt:Object.freeze({eastWest:98.175,northSouth:70.875}),
 womenCourt:Object.freeze({eastWest:70.875,northSouth:70.875}),
 stoa:Object.freeze({eastWest:185,depth:32,sideHeight:15.24,centreHeight:30.48}),
 sources:Object.freeze({courtLevels:'https://www.sefaria.org/Mishnah_Middot.2.6',porch:'https://www.sefaria.org/Mishnah_Middot.3.7',porchStairs:'https://www.sefaria.org/Mishnah_Middot.3.6',gates:'https://www.sefaria.org/Mishnah_Middot.2.3',antonia:'https://penelope.uchicago.edu/josephus/war-5.html',sanctuary:'https://www.sefaria.org/Mishnah_Middot.4.6',court:'https://www.sefaria.org/Mishnah_Middot.5.1',women:'https://www.sefaria.org/Mishnah_Middot.2.5',cubit:'https://library.biblicalarchaeology.org/sidebar/dimensions-of-architectural-elements-of-the-temple-as-recorded-in-middot-all-dimensions-are-in-cubits-1-cubit-52-5-cm-20-7-inches/',platform:'https://rsc.byu.edu/new-testament-history-culture-society/jerusalem-holy-city',stoa:'https://avande1.sites.luc.edu/jerusalem/sources/antiquities15.htm'}),
 geometryVerified:false,placementVerified:false,cubitChoiceUnique:false
});
