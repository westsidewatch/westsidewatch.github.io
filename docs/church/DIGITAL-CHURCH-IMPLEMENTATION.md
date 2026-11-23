# Living Water West · Digital Church implementation
Status: implementation branch (not automatically production approved) · 2026-11-23

## Authority and preservation
- Original repo only: `westsidewatch/westsidewatch.github.io`; Github / Cloudflare Pages. **Never use ChatGPT Sites.**
- Retain P2 Red Sea 1.72–2.37, maquette 2.50–3.27, magazine 3.36, original 251s virtual tour, GLB geometry, camera route, cross-light, maple seasons, OS typography.
- The phrase 「一座可以走進去的教會，也是一個可以繼續參與的教會。」 is INTERNAL engineering vocabulary only. Never render it on public pages.
- A physical, constructed congregation building is future-oriented; any virtual design image must be labeled illustrative, not current architecture or documented history. Free exploration after physical building exists: ROADMAP ONLY.

## Data
`static/data/church/current-sunday.json` is the SOLE live Sunday source for P2, tour finale and static visitor page. The 2026-10-11 bulletin is a verified historical source, so its status is `archive` until an editor enters the actual upcoming week. Never auto relabel an old bulletin as current or generate future personnel. No separate editing of tour's Sunday rows.
`static/data/church/gatherings.json` records recurring Sunday worship, Monday noon Bible study, Friday evening Bible study and Wednesday evening online prayer. Publish precise times only when verified; the earlier Gate lists different weekday meetings, and is historical reference, not a source of current exact Monday/Friday times.
`static/data/church/ministries.json` maps seven established chapters onto real routes without adding fictional programmes.

## Sunday editorial workflow
1. Open `/tools/church-schedule-editor.html`; edit ordinary fields and all seven rows; export JSON.
2. Upload / commit only the exported `static/data/church/current-sunday.json` in GitHub; the site deploy rebuilds.
3. On P2, 3D finale and static page, fetch this single path; degrade explicitly on network failure. Archive state MUST be visibly labeled.
4. Acceptance: edit one time, one name and one theme, confirm all THREE surfaces agree; no stale next-week schedule.

## 3D identity
- Same church identity in original approved Chinese logo and English `P.A.O.C. Living Water Assembly West`.
- Place a stationary 3D façade sign on original SOUTH entrance wall near x9.3, away from cross x15; never fake a second wall. Verify initial wide shot, approach shot, and 248-second final shot in desktop and phone screenshots; adjust only local placement if required.
- Final scene uses discreet editorial name as well so the identity is always visible without covering the cross. Static visitor page uses existing official logo asset.
- Absolutely no new WebGL engine, jump cut or change to timing.

## Content and visitor experience
- Keep the seven existing story chapters, full CUV / KJV scripture, and 251-second route.
- In each chapter show ONE contextual content action to the real section: welcome → static guide, fellowship → gatherings, worship → Sunday bulletin, prayer → online prayer, care → visitor intake, discipleship → /one/, witness → decision / membership.
- Provide `/church/visit/` as a single, indexable, no-WebGL static editorial overview accessible from existing `/church/` and the tour. It covers identity/history (only verifiable facts), Sunday, gatherings, all seven ministries, first-visit guidance, prayer, baptism/discipleship pathway, contact, forms and return to tour. Preserve canonical legacy `/church/` without rewriting its approved MERSI chapter or hero.
- Existing `/join/` Gate remains available with historical invitation copy and its verified church email. The legacy WeChat QR asset and old Zoom credentials were not reliably available, so do NOT render a broken QR or treat historical credentials as current. The invitation links to `/join/` and instructs visitors to request a confirmed invite from staff. The **four new forms** have independently tested first-party QR codes. Do not publish an unverified founding date or new Zoom ID.

## Four intake routes and privacy
Distinct shareable QR destinations: `/church/forms/?type=join`, `decision`, `newcomer`, `prayer`.
- Only minimum necessary fields; one contact method required; consent to volunteer follow-up must be explicit, privacy note and no public storage of names/requests. Do not infer church membership from a form submission.
- Decision: visitor-selected response, prayer interest; join: relationship with church and meeting interests; newcomer: first-visit needs; prayer: visibility restricted to the responsible team.
- Response target: church inbox from original Gate (`westsidewatchca@gmail.com`); volunteer triage, acknowledgement, contact preference, private handoff, 48h target (aspiration, not a promised SLA), manual closure. Never email details to public/static logs.
- Publishing a UI does NOT prove mail delivery. POST intake is disabled/fail-closed until a Cloudflare Pages Function, verified mail sender/receiver and Turnstile secret are configured. GitHub Pages has no backend. No fake success confirmation.
- If enabled, accept only same-origin POST, validate Turnstile server-side, honeypot, bounded fields and allowed types; send notification with configured provider, no PII in source repo. Add rate limiting at Cloudflare WAF. QR is only a link to secure HTTPS forms; it does not encode personal information.

## Design and verification
- Use Westside Design OS fonts/colors; no new global style authority, no gigantic navigation bar or return button, no engineering notes in rendered page.
- Real architecturally matched render should use proven screenshot of the actual GLB, not fabricated church imagery. A temporary engraving and approved logo may be displayed until a visually checked still exists. Label any conceptual image clearly.
- Test 1440×900, 390×844, 320px width, reduced-motion, keyboard/focus, QR scan, missing JSON, archive dates, refresh, backward P2 scroll, 3D proof 0/248, same-origin cross-page navigation and real email receipt with staff consent before enabling production.
- Deferred: free roam, volunteer dashboard / member CRM, unverified history timeline, historical-photo publishing.

## Latest actual verification
- Original P2 0–100% animation source thresholds preserved; R47 church contract and production Hugo build have passed on the feature branch.
- New static visitor browser QA passed on 1440px, 390px, 320px viewports, with all seven Sunday rows, four recurring groups, seven ministries, QR, Sunday editor and disabled unconfigured form.
- Real 3D sign visual proof is an independent GLB/Chromium run. Source-level presence is established; visual approval only after comparing rendered t0/12/248 screenshots.
- Historical homepage first-look tests and frozen morning-star fingerprint have old baseline expectations independent of these visitor files; diagnose separately before approving a merge. Never alter protected P2 assets just to silence unrelated checks.
