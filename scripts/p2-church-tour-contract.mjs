// P2 native virtual church: dependency and regression contract.
// Run from repo root: node scripts/p2-church-tour-contract.mjs
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { Script } from "node:vm";
const read = p => readFileSync(p, "utf8");
const html = read("static/p2/church-tour.html");
const script = read("static/p2/church-tour.js");
const folio = read("static/p2/living-water.html");
const interaction = read("static/js/p2-living-water.js");
const firstLayer = read("static/p2-maquette/index.html");
const legacyDomain = /chatgpt\.site/i;
for (const [name, source] of [
  ["second-layer HTML", html], ["second-layer JS", script],
  ["P2 church folio", folio], ["P2 church click controller", interaction]
]) assert(!legacyDomain.test(source), name + " must not depend on Sites");
assert(!/location\.replace|http-equiv=["']refresh/.test(html), "No redirect in tour page");
assert(/<canvas\b/.test(html), "Tour owns its own WebGL canvas");
assert(!/<h[1-6]\b|<p\b|<button\b|<aside\b/i.test(html), "No visible UI or engineering labels");
assert(script.includes("entranceHinge.rotation.y"), "A real scene door must open");
assert(script.includes("entranceHinge.attach(mesh(\"TALL SINGLE WHITE PIVOT DOOR\")"), "The original tall GLB entrance must be the moving door");
assert(!script.includes("const leaf = new Mesh"), "Do not introduce a short fake entrance leaf");
assert(script.includes("new PerspectiveCamera("), "Use an actual perspective camera");
assert(script.includes("south cross wall|solid quadrant"), "The cross is a wall aperture, not luminous solid quadrants");
assert(script.includes("surfaceMaps.stone"), "Architectural materials must remain textured");

assert(script.includes("loadArchitecture()"), "Native GLB loading required");
assert((script.match(/at:\s*[0-9]+,\s*p:/g) || []).length >= 22,
  "Full original walk through sanctuary, cafe, terraces and final aerial required");
assert(script.includes("staffSanctuaryHinge.attach(mesh(\"SANCTUARY STAFF DOOR\")"),
  "Do not omit the true south sanctuary staff exit");
assert(script.includes("northCourtSlider.position.x"),
  "Courtyard north official passage must open");
assert(script.includes("updateMapleSeason(t,duration)"),
  "Japanese maple foliage must transition with the seasons");
assert(script.includes("registerMapleSource(object)"),
  "Real CC0 maple bark cannot be replaced by foliage colors");
assert(script.includes("daylightChapters") && script.includes("solar=Math.max(0,Math.sin(angle))"),
  "Daily sunlight loops must be continuous through scene changes");
for (const file of [
  "static/p2-maquette/model-v34.0.part",
  "static/p2-maquette/model-v34.1.part",
  "static/p2-maquette/model-v34.2.part",
  "static/p2-maquette/assets/GLTFLoader-j388d5bW.js"
]) assert(existsSync(file), "Missing local asset: " + file);
assert(folio.match(/\/p2\/church-tour\.html/g)?.length >= 3, "Both first-layer church names and model must link to native tour");
assert(interaction.includes("new URL('/p2/church-tour.html?scene=20261121-architecture-r3', window.location.href)"), "Iframe click must produce a resolved local URL");
assert(firstLayer.includes("p2-BIwqVfIr.js"), "First-layer growth model remains untouched");
const syntax = script.replace(/import\s*\{[\s\S]*?\}\s*from\s*["'][^"']+["'];?/m, "");
new Script(syntax, { filename: "church-tour.js" });
console.log("P2 native virtual church: 12 contract checks passed");
