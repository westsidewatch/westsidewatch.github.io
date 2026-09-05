/* DORÉ Companion 1.1 ChatGPT content script. */

const BADGE_ID = "dore-a2a-companion-status";
let lastCommand = "";
let lastCommandAt = 0;
let healthTimer = null;
let pendingComposerCommand = "";

function ensureBadge() {
  let badge = document.getElementById(BADGE_ID);
  if (badge) return badge;
  badge = document.createElement("div");
  badge.id = BADGE_ID;
  badge.textContent = "DORÉ A2A · CHECKING";
  badge.setAttribute("role", "status");
  badge.style.cssText = ["position:fixed","right:14px","bottom:14px","z-index:2147483647","padding:6px 9px","border-radius:999px","font:600 11px/1.2 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif","letter-spacing:.04em","background:rgba(20,20,20,.88)","color:#d7bd72","border:1px solid rgba(215,189,114,.55)","box-shadow:0 2px 12px rgba(0,0,0,.18)","pointer-events:none"].join(";");
  document.documentElement.appendChild(badge);
  return badge;
}

function setBadge(state, detail) {
  const badge = ensureBadge();
  const normalized = String(state || "OFFLINE").toUpperCase();
  badge.textContent = `DORÉ A2A · ${normalized}`;
  badge.title = detail || "";
  badge.style.opacity = normalized === "ONLINE" || normalized === "PASS" ? "1" : normalized === "WORKING" ? ".9" : ".72";
}

async function refreshHealth() {
  try {
    const reply = await browser.runtime.sendMessage({ type: "dore.health" });
    if (reply && reply.online) setBadge("ONLINE", `transport: ${reply.transport || "native"}`);
    else setBadge("OFFLINE", reply && reply.error ? reply.error : "DORÉ native host unavailable");
  } catch (error) { setBadge("OFFLINE", String(error && error.message ? error.message : error)); }
}

function readNode(node) {
  if (!node) return "";
  if (node instanceof HTMLTextAreaElement || node instanceof HTMLInputElement) return node.value || "";
  return node.innerText || node.textContent || "";
}

function composerRoot() {
  return document.querySelector('#prompt-textarea') ||
    document.querySelector('[data-testid="composer-text-input"]') ||
    document.querySelector('form textarea') ||
    document.querySelector('form [contenteditable="true"]') ||
    document.querySelector('main textarea') ||
    document.querySelector('main [contenteditable="true"]');
}

function currentComposerCommand() {
  const direct = String(readNode(composerRoot()) || "").trim();
  if (direct.toLowerCase().startsWith("/dore")) return direct;
  const candidates = Array.from(document.querySelectorAll('textarea,[contenteditable="true"]'));
  for (const node of candidates) {
    const text = String(readNode(node) || "").trim();
    if (text.toLowerCase().startsWith("/dore")) return text;
  }
  return "";
}

function rememberComposer() {
  const command = currentComposerCommand();
  if (command) pendingComposerCommand = command;
}

async function dispatchCommand(raw) {
  const command = String(raw || "").trim();
  if (!command.toLowerCase().startsWith("/dore")) return;
  const now = Date.now();
  if (command === lastCommand && now - lastCommandAt < 2000) return;
  lastCommand = command;
  lastCommandAt = now;
  pendingComposerCommand = "";
  setBadge("WORKING", command);
  try {
    const reply = await browser.runtime.sendMessage({ type: "dore.command", command });
    if (reply && reply.ok && reply.result) {
      const result = reply.result;
      const status = String(result.status || (result.ok ? "PASS" : "ONLINE")).toUpperCase();
      setBadge(status === "COMPLETED" ? "PASS" : status, JSON.stringify(result));
      window.dispatchEvent(new CustomEvent("dore:a2a-result", { detail: result }));
    } else setBadge("OFFLINE", reply && reply.error ? reply.error : "DORÉ command failed");
  } catch (error) { setBadge("OFFLINE", String(error && error.message ? error.message : error)); }
}

// Track the live composer continuously. ChatGPT can clear/reparent it during submit.
document.addEventListener("input", rememberComposer, true);
document.addEventListener("beforeinput", rememberComposer, true);
document.addEventListener("pointerdown", rememberComposer, true);

document.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing) return;
  rememberComposer();
  const command = currentComposerCommand() || pendingComposerCommand;
  if (command) dispatchCommand(command);
}, true);

// Send-button capture deliberately does not depend on English aria-labels/test ids.
document.addEventListener("click", (event) => {
  const button = event.target && event.target.closest ? event.target.closest("button") : null;
  if (!button) return;
  const form = button.closest("form");
  if (!form && !button.closest('main')) return;
  const command = currentComposerCommand() || pendingComposerCommand;
  if (command) dispatchCommand(command);
}, true);

// Form submit is the most stable semantic boundary across ChatGPT UI revisions/locales.
document.addEventListener("submit", () => {
  const command = currentComposerCommand() || pendingComposerCommand;
  if (command) dispatchCommand(command);
}, true);

ensureBadge();
refreshHealth();
healthTimer = window.setInterval(refreshHealth, 10000);
window.addEventListener("beforeunload", () => { if (healthTimer) window.clearInterval(healthTimer); }, { once: true });
