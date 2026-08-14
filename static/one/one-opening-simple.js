/* ONE opening rail compatibility layer.
 * The actual wheel / pointer / keyboard rail interaction belongs to one-app.js.
 * Do not intercept it here: unvisited books stay as numbers and reveal their names
 * only when they reach the rail focus; visited books keep their status treatment.
 */
(() => {
  "use strict";
  const list=document.getElementById("cover-books");
  if(!list)return;
  list.classList.add("one-rail-enabled");
})();
