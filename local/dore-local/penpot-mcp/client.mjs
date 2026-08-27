#!/usr/bin/env node
import fs from 'node:fs';
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';

const url = process.env.PENPOT_MCP_URL || 'http://127.0.0.1:4401/mcp';
const op = process.argv[2] || 'status';
const client = new Client({ name: 'dore-penpot', version: '0.1.0' });
const transport = new StreamableHTTPClientTransport(new URL(url));

function out(value) { process.stdout.write(JSON.stringify(value)); }

try {
  await client.connect(transport);
  if (op === 'status') {
    const tools = await client.listTools();
    out({ ok: true, url, server: client.getServerVersion?.() || null, tool_count: tools.tools?.length || 0, tools: (tools.tools || []).map(t => t.name) });
  } else if (op === 'list') {
    const tools = await client.listTools();
    out({ ok: true, tools: tools.tools || [] });
  } else if (op === 'call') {
    const raw = fs.readFileSync(0, 'utf8');
    const payload = JSON.parse(raw || '{}');
    if (!payload.name) throw new Error('missing tool name');
    const result = await client.callTool({ name: payload.name, arguments: payload.arguments || {} });
    out({ ok: !result?.isError, result });
  } else {
    throw new Error(`unknown operation: ${op}`);
  }
} catch (error) {
  out({ ok: false, error: String(error?.message || error), url });
  process.exitCode = 1;
} finally {
  try { await client.close(); } catch {}
}
