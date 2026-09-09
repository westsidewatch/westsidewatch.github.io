(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.DoreMultiwriteBibleStudy = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const ACTIONS = new Set(["keep", "flow", "present"]);
  const DEFAULT_LABELS = Object.freeze({ keep: "保留", flow: "流程", present: "投影" });

  function asArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function safeText(value) {
    return value == null ? "" : String(value);
  }

  function normalizeAction(action) {
    const id = typeof action === "string" ? action : action && (action.id || action.action || action.type);
    const normalized = safeText(id).toLowerCase();
    return ACTIONS.has(normalized) ? normalized : null;
  }

  function normalizeResult(result, index) {
    const actions = asArray(result && result.actions)
      .map(normalizeAction)
      .filter(Boolean)
      .filter((value, position, values) => values.indexOf(value) === position);
    return {
      id: safeText((result && (result.id || result.result_id || result.source_ref)) || `result-${index + 1}`),
      type: safeText(result && result.type),
      title: safeText((result && result.title) || (result && result.canonical_reference) || "未命名結果"),
      snippet: safeText(result && result.snippet),
      relation: safeText(result && result.relation),
      sourceKind: safeText(result && result.source_kind),
      sourceRef: safeText(result && result.source_ref),
      confidence: result && typeof result.confidence === "number" ? result.confidence : null,
      provenance: asArray(result && result.provenance),
      preview: result && result.preview != null ? result.preview : null,
      canonicalReference: safeText(result && result.canonical_reference),
      evidenceStatus: safeText(result && result.evidence_status),
      actions,
      raw: result || {},
    };
  }

  function normalizeResponse(payload, maxResults) {
    const source = Array.isArray(payload) ? payload : asArray(payload && (payload.results || payload.hits));
    return source.slice(0, maxResults).map(normalizeResult);
  }

  function createElement(doc, tag, className, text) {
    const node = doc.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = safeText(text);
    return node;
  }

  function installStyles(doc) {
    if (!doc || doc.getElementById("dore-bi3-styles")) return;
    const style = doc.createElement("style");
    style.id = "dore-bi3-styles";
    style.textContent = `
      .dore-bi3{font:inherit;color:inherit;position:relative;--bi3-border:color-mix(in srgb,currentColor 16%,transparent);--bi3-muted:color-mix(in srgb,currentColor 58%,transparent);--bi3-surface:color-mix(in srgb,currentColor 4%,transparent)}
      .dore-bi3__ghost{min-height:1.4em;margin:.25rem 0;color:var(--bi3-muted);font-size:.86em;opacity:.72;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:opacity .18s ease}
      .dore-bi3__ghost[hidden]{display:block;opacity:0;visibility:hidden}
      .dore-bi3__search{display:flex;gap:.5rem;align-items:center}
      .dore-bi3__input{width:100%;box-sizing:border-box;border:1px solid var(--bi3-border);border-radius:.65rem;background:transparent;color:inherit;padding:.62rem .75rem;font:inherit;outline:none}
      .dore-bi3__input:focus{border-color:color-mix(in srgb,currentColor 34%,transparent)}
      .dore-bi3__rail{display:grid;gap:.42rem;margin-top:.55rem}
      .dore-bi3__result{appearance:none;text-align:left;width:100%;border:1px solid var(--bi3-border);border-radius:.65rem;background:var(--bi3-surface);color:inherit;padding:.62rem .72rem;cursor:pointer}
      .dore-bi3__result[aria-current=true]{border-color:color-mix(in srgb,currentColor 38%,transparent)}
      .dore-bi3__result-title{display:block;font-weight:650}
      .dore-bi3__result-snippet{display:block;color:var(--bi3-muted);font-size:.9em;margin-top:.16rem;line-height:1.42}
      .dore-bi3__preview{border-top:1px solid var(--bi3-border);margin-top:.72rem;padding-top:.72rem}
      .dore-bi3__preview[hidden],.dore-bi3__rail[hidden]{display:none}
      .dore-bi3__preview-head{display:flex;justify-content:space-between;gap:.7rem;align-items:baseline}
      .dore-bi3__evidence{font-size:.76em;color:var(--bi3-muted);text-transform:none}
      .dore-bi3__preview-body{margin:.45rem 0;line-height:1.55;white-space:pre-wrap}
      .dore-bi3__actions{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.55rem}
      .dore-bi3__action{appearance:none;border:1px solid var(--bi3-border);border-radius:999px;background:transparent;color:inherit;padding:.34rem .68rem;font:inherit;font-size:.86em;cursor:pointer}
      .dore-bi3__status{font-size:.78em;color:var(--bi3-muted);margin-top:.35rem;min-height:1em}
      @media (prefers-reduced-motion:reduce){.dore-bi3__ghost{transition:none}}
    `;
    (doc.head || doc.documentElement).appendChild(style);
  }

  function createPrepareController(options) {
    const config = options || {};
    if (typeof config.search !== "function") throw new TypeError("BI-3 requires a DORÉ search adapter");

    const state = {
      host: config.host || "multiwrite",
      mode: "prepare",
      embedded: Boolean(config.embedded),
      maxResults: Math.max(1, Math.min(Number(config.maxResults) || 5, 5)),
      debounceMs: Math.max(80, Number(config.debounceMs) || 420),
      query: "",
      results: [],
      selectedIndex: -1,
      pendingToken: 0,
      timer: null,
      mounted: false,
      nodes: null,
    };

    const labels = Object.assign({}, DEFAULT_LABELS, config.labels || {});
    const onAction = typeof config.onAction === "function" ? config.onAction : function () {};
    const onStateChange = typeof config.onStateChange === "function" ? config.onStateChange : function () {};

    function context(lane) {
      return {
        capability: "context.fuzzy-search",
        host: state.host,
        mode: state.mode,
        embedded: state.embedded,
        lane: lane || "passive",
      };
    }

    function emitState() {
      onStateChange({
        query: state.query,
        resultCount: state.results.length,
        selectedIndex: state.selectedIndex,
        host: state.host,
        mode: state.mode,
        embedded: state.embedded,
      });
    }

    function setStatus(text) {
      if (state.nodes) state.nodes.status.textContent = safeText(text);
    }

    function renderGhost() {
      if (!state.nodes) return;
      const ghost = state.nodes.ghost;
      const first = state.results[0];
      if (!first || !state.query) {
        ghost.textContent = "";
        ghost.hidden = true;
        return;
      }
      ghost.textContent = first.canonicalReference || first.title;
      ghost.hidden = false;
    }

    function renderRail() {
      if (!state.nodes) return;
      const rail = state.nodes.rail;
      rail.replaceChildren();
      rail.hidden = state.results.length === 0;
      state.results.forEach((result, index) => {
        const button = createElement(rail.ownerDocument, "button", "dore-bi3__result");
        button.type = "button";
        button.dataset.index = String(index);
        button.setAttribute("aria-current", index === state.selectedIndex ? "true" : "false");
        button.appendChild(createElement(rail.ownerDocument, "span", "dore-bi3__result-title", result.canonicalReference || result.title));
        if (result.snippet) button.appendChild(createElement(rail.ownerDocument, "span", "dore-bi3__result-snippet", result.snippet));
        button.addEventListener("click", () => select(index));
        rail.appendChild(button);
      });
    }

    function previewText(result) {
      if (typeof result.preview === "string") return result.preview;
      if (result.preview && typeof result.preview === "object") {
        return safeText(result.preview.text || result.preview.snippet || result.preview.content || result.snippet);
      }
      return result.snippet;
    }

    function renderPreview() {
      if (!state.nodes) return;
      const preview = state.nodes.preview;
      preview.replaceChildren();
      const result = state.results[state.selectedIndex];
      preview.hidden = !result;
      if (!result) return;

      const head = createElement(preview.ownerDocument, "div", "dore-bi3__preview-head");
      head.appendChild(createElement(preview.ownerDocument, "strong", "", result.canonicalReference || result.title));
      if (result.evidenceStatus) head.appendChild(createElement(preview.ownerDocument, "span", "dore-bi3__evidence", result.evidenceStatus));
      preview.appendChild(head);
      const body = previewText(result);
      if (body) preview.appendChild(createElement(preview.ownerDocument, "div", "dore-bi3__preview-body", body));

      const actions = createElement(preview.ownerDocument, "div", "dore-bi3__actions");
      result.actions.forEach((action) => {
        const button = createElement(preview.ownerDocument, "button", "dore-bi3__action", labels[action]);
        button.type = "button";
        button.dataset.action = action;
        button.addEventListener("click", () => dispatchAction(action, result));
        actions.appendChild(button);
      });
      if (result.actions.length) preview.appendChild(actions);
    }

    function render() {
      renderGhost();
      renderRail();
      renderPreview();
      emitState();
    }

    function select(index) {
      const next = Number(index);
      state.selectedIndex = Number.isInteger(next) && next >= 0 && next < state.results.length ? next : -1;
      renderRail();
      renderPreview();
      emitState();
      return state.results[state.selectedIndex] || null;
    }

    function actionPayload(action, result) {
      return {
        action,
        host: state.host,
        mode: state.mode,
        embedded: state.embedded,
        result_id: result.id,
        canonical_reference: result.canonicalReference || null,
        source_ref: result.sourceRef || null,
        evidence_status: result.evidenceStatus || null,
        result: result.raw,
      };
    }

    function dispatchAction(action, result) {
      const normalized = normalizeAction(action);
      if (!normalized) return false;
      onAction(actionPayload(normalized, result));
      return true;
    }

    async function runSearch(query, lane) {
      const trimmed = safeText(query).trim();
      state.query = trimmed;
      const token = ++state.pendingToken;
      if (!trimmed) {
        state.results = [];
        state.selectedIndex = -1;
        setStatus("");
        render();
        return [];
      }
      setStatus("搜尋中…");
      try {
        const payload = await config.search(trimmed, context(lane));
        if (token !== state.pendingToken) return state.results;
        state.results = normalizeResponse(payload, state.maxResults);
        state.selectedIndex = state.results.length ? 0 : -1;
        setStatus(state.results.length ? "" : "沒有找到相關證據");
        render();
        return state.results;
      } catch (error) {
        if (token !== state.pendingToken) return state.results;
        state.results = [];
        state.selectedIndex = -1;
        setStatus("搜尋暫時不可用");
        render();
        if (typeof config.onError === "function") config.onError(error);
        return [];
      }
    }

    function schedulePassive(query) {
      if (state.timer) clearTimeout(state.timer);
      const trimmed = safeText(query).trim();
      state.query = trimmed;
      if (trimmed.length < 2) {
        state.pendingToken += 1;
        state.results = [];
        state.selectedIndex = -1;
        render();
        return;
      }
      state.timer = setTimeout(() => runSearch(trimmed, "passive"), state.debounceMs);
    }

    function mount(container) {
      if (!container || !container.ownerDocument) throw new TypeError("BI-3 mount requires a DOM container");
      const doc = container.ownerDocument;
      installStyles(doc);
      container.replaceChildren();
      container.classList.add("dore-bi3");
      container.dataset.doreCapability = "bible-study.prepare";
      container.dataset.host = state.host;
      container.dataset.embedded = String(state.embedded);

      const ghost = createElement(doc, "div", "dore-bi3__ghost");
      ghost.hidden = true;
      ghost.setAttribute("aria-live", "polite");
      const searchWrap = createElement(doc, "div", "dore-bi3__search");
      const input = createElement(doc, "input", "dore-bi3__input");
      input.type = "search";
      input.autocomplete = "off";
      input.spellcheck = false;
      input.placeholder = config.placeholder || "查找經文、人物、地點、原文或你記得的一句話…";
      input.setAttribute("aria-label", config.ariaLabel || "多雷查經搜尋");
      searchWrap.appendChild(input);
      const rail = createElement(doc, "div", "dore-bi3__rail");
      rail.hidden = true;
      rail.setAttribute("aria-label", "相關證據");
      const preview = createElement(doc, "section", "dore-bi3__preview");
      preview.hidden = true;
      const status = createElement(doc, "div", "dore-bi3__status");
      status.setAttribute("aria-live", "polite");
      container.append(ghost, searchWrap, rail, preview, status);

      state.nodes = { ghost, input, rail, preview, status };
      state.mounted = true;
      input.addEventListener("input", (event) => schedulePassive(event.target.value));
      input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          if (state.timer) clearTimeout(state.timer);
          runSearch(input.value, "explicit");
        } else if (event.key === "ArrowDown" && state.results.length) {
          event.preventDefault();
          select(Math.min(state.selectedIndex + 1, state.results.length - 1));
        } else if (event.key === "ArrowUp" && state.results.length) {
          event.preventDefault();
          select(Math.max(state.selectedIndex - 1, 0));
        } else if (event.key === "Escape") {
          state.results = [];
          state.selectedIndex = -1;
          render();
        }
      });
      render();
      return controller;
    }

    function destroy() {
      if (state.timer) clearTimeout(state.timer);
      state.pendingToken += 1;
      if (state.nodes) {
        const container = state.nodes.input.closest(".dore-bi3");
        if (container) container.replaceChildren();
      }
      state.nodes = null;
      state.mounted = false;
    }

    const controller = {
      mount,
      destroy,
      search: (query) => runSearch(query, "explicit"),
      passiveSearch: (query) => runSearch(query, "passive"),
      select,
      dispatchAction: (action) => {
        const result = state.results[state.selectedIndex];
        return result ? dispatchAction(action, result) : false;
      },
      getState: () => ({
        host: state.host,
        mode: state.mode,
        embedded: state.embedded,
        query: state.query,
        results: state.results.slice(),
        selectedIndex: state.selectedIndex,
        mounted: state.mounted,
      }),
    };
    return controller;
  }

  return Object.freeze({
    createPrepareController,
    normalizeResult,
    normalizeResponse,
  });
});
