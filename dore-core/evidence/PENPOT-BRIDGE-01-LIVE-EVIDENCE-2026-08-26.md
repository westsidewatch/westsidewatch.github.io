# PENPOT-BRIDGE-01 — LIVE EVIDENCE

Status: BRIDGE VERIFIED / FIRST PERSISTENT WRITE VERIFIED
Date: 2026-08-26

## Verified chain

1. Cloudflare runtime can read `PENPOT_MCP_KEY` without exposing it.
2. Doré initializes Penpot Remote MCP using protocol `2025-03-26`.
3. Penpot server identifies as `penpot` version `1.0.0`.
4. `tools/list` returns four remote tools: `execute_code`, `high_level_overview`, `penpot_api_info`, `export_shape`.
5. `execute_code` resolves the live focused design context:
   - file: `Westside Watch — Design System 1.0`
   - page: `Page 1`
6. Doré performed a persistent write through Remote MCP. Penpot created board:
   - name: `00 — WESTSIDE VISUAL CONSTITUTION`
   - id: `53ba078d-e4d8-80ca-8008-8b325546ddaa`
   - size: `1440 × 1024`
7. A later independent MCP call found the same board by name/id and returned `created:false`, proving persistence rather than a transient response.

## Defect discovered during first write

The first typography styling attempt used `Text.getRange()` without explicit bounds and Penpot rejected it with `:getRange-start`. The bridge itself remained healthy and the board write persisted. Repair code removes that invalid range call and is committed; it will complete the foundation layers after the corresponding Cloudflare production deployment catches up.

## Engineering conclusion

The critical bridge is now real, not conceptual:

`Doré Core → Cloudflare Runtime Secret → Penpot Remote MCP → live focused Penpot file → execute_code → persistent editable Penpot object`

This establishes Penpot as an executable Doré design surface. Future Westside visual-system work should use small idempotent writes, readback verification, and export-based visual inspection rather than manual reconstruction.

## Sweep-01 reconciliation — 2026-08-27

**Bounded classification:** `VERIFIED_COMPLETE` for the bridge milestone only: authenticated remote-tool discovery, live design-context resolution, one persistent editable write, and independent readback are all directly evidenced.

**Not included in that completion claim:** completion of the Visual Constitution board, typography/foundation layers, visual quality, export fidelity, responsive/print transfer, or a finished Westside visual grammar. The first styling attempt exposed a real `Text.getRange()` defect, so those downstream design-surface claims remain active work rather than completed evidence.

**Current disposition:** retain Penpot Remote MCP as a proven reusable design-execution capability under the broader `VIS-GRAMMAR` / visual-production work. Do not reopen bridge feasibility unless regression evidence appears; instead use the verified bridge for idempotent asset-system experiments and require readback/export inspection for each consequential visual milestone.

**Capability retained:** Doré can cross the boundary from repository/runtime orchestration into a persistent editable external design surface while keeping credentials in runtime secrets and verifying persistence independently. This is reusable for future visual-system experiments, but it does not itself prove design quality.

**Canonical-register effect:** no status change is warranted. `VIS-GRAMMAR` remains `ACTIVE_PARALLEL / BUILDING`; the bridge is enabling infrastructure inside that workstream, not a reason to promote Brand V1 or visual-grammar completion. P01 remains untouched.