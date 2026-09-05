/* DORÉ Companion 1.3 ChatGPT content script. */

const BADGE_ID = "dore-a2a-companion-status";
const TERMINAL_HOLD_MS = 30000;
let lastCommand = "";
let lastCommandAt = 0;
let healthTimer = null;
let pendingComposerCommand = "";
let commandInFlight = false;
let terminalHoldUntil = 0;
const seenMessageNodes = new WeakSet();

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

function setBadge(state, detail, hold = false) {
  const badge = ensureBadge();
  const normalized = String(state || "OFFLINE").toUpperCase();
  badge.textContent = `DORÉ A2A · ${normalized}`;
  badge.title = detail || "";
  badge.dataset.doreDetail = detail || "";
  badge.style.opacity = ["ONLINE","PASS","CAPTURED","SENT","FAILED","ERROR"].includes(normalized) ? "1" : ".8";
  if (hold) terminalHoldUntil = Date.now() + TERMINAL_HOLD_MS;
}

async function refreshHealth() {
  if (commandInFlight || Date.now() < terminalHoldUntil) return;
  try {
    const reply = await browser.runtime.sendMessage({ type: "dore.health" });
    if (reply && reply.online) setBadge("ONLINE", `transport: ${reply.transport || "native"}`);
    else setBadge("OFFLINE", reply && reply.error ? reply.error : "DORÉ native host unavailable");
  } catch (error) {
    setBadge("OFFLINE", String(error && error.message ? error.message : error));
  }
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

function normalizeCommand(raw) {
  const text = String(raw || "").replace(/\u00a0/g, " ").trim();
  return text.toLowerCase().startsWith("/dore") ? text : "";
}

function currentComposerCommand() {
  const direct = normalizeCommand(readNode(composerRoot()));
  if (direct) return direct;
  for (const node of Array.from(document.querySelectorAll('textarea,[contenteditable="true"]'))) {
    const text = normalizeCommand(readNode(node));
    if (text) return text;
  }
  return "";
}

function rememberComposer() {
  const command = currentComposerCommand();
  if (command) {
    pendingComposerCommand = command;
    terminalHoldUntil = 0;
    setBadge("CAPTURED", command);
  }
}

function submittedRoots(node) {
  if (!(node instanceof Element)) return [];
  const roots = [];
  if (node.matches('[data-message-author-role="user"]')) roots.push(node);
  roots.push(...node.querySelectorAll('[data-message-author-role="user"]'));
  return roots;
}

function observeSubmittedMessages() {
  // Existing messages are history, not new commands. Mark them seen without dispatch.
  document.querySelectorAll('[data-message-author-role="user"]').forEach((node) => seenMessageNodes.add(node));

  const scan = (node) => {
    for (const root of submittedRoots(node)) {
      if (seenMessageNodes.has(root)) continue;
      seenMessageNodes.add(root);
      const command = normalizeCommand(readNode(root));
      if (!command) continue;
      terminalHoldUntil = 0;
      setBadge("CAPTURED", `submitted: ${command}`);
      dispatchCommand(command, "submitted-message");
    }
  };

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) scan(node);
    }
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  return observer;
}

function resultDetail(result) {
  if (!result || typeof result !== "object") return String(result || "empty result");
  if (result.error && typeof result.error === "object") {
    return `${result.error.code || "error"}: ${result.error.message || JSON.stringify(result.error)}`;
  }
  if (result.error) return String(result.error);
  return JSON.stringify(result);
}

async function dispatchCommand(raw, source = "composer") {
  const command = normalizeCommand(raw);
  if (!command) return;
  const now = Date.now();
  if (command === lastCommand && now - lastCommandAt < 2500) return;
  lastCommand = command;
  lastCommandAt = now;
  pendingComposerCommand = "";
  terminalHoldUntil = 0;
  commandInFlight = true;
  setBadge("SENT", `${source}: ${command}`);
  try {
    const reply = await browser.runtime.sendMessage({ type: "dore.command", command, source });
    if (reply && reply.ok && reply.result) {
      const result = reply.result;
      const status = String(result.status || (result.ok ? "PASS" : "RESULT")).toUpperCase();
      const visible = status === "COMPLETED" || status === "SUCCEEDED" ? "PASS" : status;
      setBadge(visible, resultDetail(result), true);
      window.dispatchEvent(new CustomEvent("dore:a2a-result", { detail: result }));
    } else {
      setBadge("ERROR", reply && reply.error ? reply.error : "DORÉ command failed before result", true);
    }
  } catch (error) {
    setBadge("ERROR", String(error && error.message ? error.message : error), true);
  } finally {
    commandInFlight = false;
  }
}

document.addEventListener("input", rememberComposer, true);
document.addEventListener("beforeinput", rememberComposer, true);
document.addEventListener("pointerdown", rememberComposer, true);
document.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing) return;
  rememberComposer();
  const command = currentComposerCommand() || pendingComposerCommand;
  if (command) dispatchCommand(command, "keydown");
}, true);
document.addEventListener("click", (event) => {
  const button = event.target && event.target.closest ? event.target.closest("button") : null;
  if (!button) return;
  const command = currentComposerCommand() || pendingComposerCommand;
  if (command) dispatchCommand(command, "click");
}, true);
document.addEventListener("submit", () => {
  const command = currentComposerCommand() || pendingComposerCommand;
  if (command) dispatchCommand(command, "submit");
}, true);

ensureBadge();
const submittedObserver = observeSubmittedMessages();
refreshHealth();
healthTimer = window.setInterval(refreshHealth, 10000);
window.addEventListener("beforeunload", () => {
  if (healthTimer) window.clearInterval(healthTimer);
  submittedObserver.disconnect();
}, { once: true });
