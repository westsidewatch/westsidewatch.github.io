#!/usr/bin/env node
/**
 * Xi Wang poster toolchain routing and evidence gate (offline only).
 * This is NOT a rendering engine, installer, or a substitute for art review.
 * No imports from the P2 runtime and no changes to public-facing files.
 */
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname, isAbsolute, join } from 'node:path';
import { homedir } from 'node:os';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const root = resolve(new URL('../..', import.meta.url).pathname);
const variants = new Set(['A', 'B']);
const common = [
  { id: 'editorial', role: 'one visual event, ink/paper logic, negative space', tool: 'mono-color-skill (read SKILL.md; not an SVG renderer)' },
  { id: 'glyph', role: 'original editable 西望 letterforms', tool: 'Inkscape / KAGE Editor / Kumiko / Graphite' },
  { id: 'geometry', role: 'unions, differences, counters, optical adjustment', tool: 'skia-pathops / Inkscape' },
  { id: 'composition', role: 'editorial layout variants under Design OS', tool: 'flowshape method; native SVG' },
  { id: 'export', role: 'editable native SVG and source/seed', tool: 'SVG export / SVGO (optional)' },
  { id: 'review', role: 'actual browser screenshots and OS 10-part review', tool: 'browser + editorial reviewer' },
];
const engraving = { id: 'engraving', role: 'seven distinct line fields INSIDE seven upright glyph groups', tool: 'd3-shape / d3-contour / penfill / vpype' };
const stagesFor = v => v === 'B' ? [...common.slice(0,3), engraving, ...common.slice(3)] : common;

function result(command, args) {
  try {
    const r = spawnSync(command, args, { encoding: 'utf8', timeout: 4000 });
    const message = String(r.stdout || r.stderr || '').trim().split('\n').at(0);
    return { available: !r.error && r.status === 0, info: (message || (r.error && r.error.message) || '').slice(0, 125) };
  } catch (e) { return { available: false, info: String(e.message) }; }
}
function mod(name) {
  try { return { available: Boolean(require.resolve(name)), info: 'resolve OK' }; }
  catch { return { available: false, info: 'not resolvable here' }; }
}
function probes() {
  const skillPath = join(homedir(), '.claude', 'skills', 'mono-color', 'SKILL.md');
  return [
    ['mono-color local skill', { available: existsSync(skillPath), info: existsSync(skillPath) ? skillPath : 'read upstream SKILL.md directly; NOT auto-installed' }],
    ['inkscape', result('inkscape', ['--version'])],
    ['python3', result('python3', ['--version'])],
    ['skia-pathops (Python pathops)', result('python3', ['-c', 'import pathops; print("import OK")'])],
    ['penfill (Python)', result('python3', ['-c', 'import penfill; print("import OK")'])],
    ['vpype', result('vpype', ['--version'])],
    ['d3-shape', mod('d3-shape')],
    ['d3-contour', mod('d3-contour')],
  ];
}
function plan(v) {
  console.log('Xi Wang / ' + v + ' — preflight only; available != executed != accepted');
  for (const s of stagesFor(v)) console.log('  ' + s.id.padEnd(13) + ' | ' + s.tool + '\n' + ' '.repeat(18) + s.role);
  console.log('\nLocal tool checks (unavailable tools are NOT silently simulated):');
  for (const [name, p] of probes()) console.log('  ' + (p.available ? 'FOUND  ' : 'MISSING') + ' | ' + name + ' | ' + p.info);
  console.log('\nDraft a trace: node scripts/xiwang/poster-toolchain.mjs init ' + v.toLowerCase() + ' /tmp/xiwang-' + v.toLowerCase() + '-receipt.json');
}
function init(v, file) {
  if (existsSync(file)) throw new Error('receipt already exists; refusing overwrite: ' + file);
  const doc = {
    variant: v, createdAt: new Date().toISOString(),
    authority: 'docs/design/XIWANG-POSTER-TOOLCHAIN-EXECUTION.md',
    stages: stagesFor(v).map(({id, role, tool}) => ({
      id, role, selectedTool: tool, status: 'planned', operation: '', evidenceFile: '', notes: ''
    })),
    proofs: {
      nativeSvg: '', desktop1648: '', tablet768: '', mobile390: '', mobile320: '',
      zoom200: '', reducedMotion: '', reverseScroll: ''
    },
    artReview: { scoreOutOf20: null, blockingProblems: [], approvedByHuman: false }
  };
  mkdirSync(dirname(file), {recursive:true});
  writeFileSync(file, JSON.stringify(doc, null, 2) + '\n', { flag: 'wx' });
  console.log('Created unexecuted receipt: ' + file + '\nNo tools were run. Fill evidence only after actual work.');
}
function proofPath(p, file) { return isAbsolute(p) ? p : resolve(dirname(file), p); }
function verify(file) {
  if (!existsSync(file)) throw new Error('receipt not found: ' + file);
  const d = JSON.parse(readFileSync(file, 'utf8'));
  const v = String(d.variant || '').toUpperCase();
  if (!variants.has(v)) throw new Error('unknown variant in receipt');
  const problems = [];
  for (const expected of stagesFor(v)) {
    const s = (d.stages || []).find(s => s.id === expected.id);
    if (!s) { problems.push('missing stage ' + expected.id); continue; }
    if (s.status !== 'executed' && s.status !== 'reviewed') problems.push(expected.id + ': not executed');
    if (!s.operation || !String(s.operation).trim()) problems.push(expected.id + ': missing actual operation/command');
    if (!s.evidenceFile || !existsSync(proofPath(s.evidenceFile, file))) problems.push(expected.id + ': missing actual evidence file');
  }
  for (const [key, path] of Object.entries(d.proofs || {})) {
    if (!path || !existsSync(proofPath(path, file))) problems.push('missing real proof: ' + key);
  }
  if (!d.proofs || Object.keys(d.proofs).length !== 8) problems.push('proof set incomplete');
  if (d.proofs?.nativeSvg && existsSync(proofPath(d.proofs.nativeSvg, file))) {
    const source = readFileSync(proofPath(d.proofs.nativeSvg, file), 'utf8');
    if (!/<svg[\s>]/.test(source)) problems.push('nativeSvg is not valid-looking SVG markup');
    if (v === 'B') {
      const layers = (source.match(/data-word-layer\s*=/g) || []).length;
      if (layers !== 7) problems.push('B must expose exactly 7 data-word-layer attributes; found ' + layers);
    }
  }
  const score = d.artReview?.scoreOutOf20;
  if (typeof score !== 'number' || score < 15 || score > 20) problems.push('editorial score not within exploratory 15–20 range');
  if (!d.artReview?.approvedByHuman) problems.push('art direction not approved by a real reviewer');
  if (d.artReview?.blockingProblems?.length) problems.push('blocking visual problems remain');
  console.log(problems.length ? 'BLOCKED — evidence/acceptance incomplete:' : 'EVIDENCE STRUCTURE COMPLETE — human visual quality still requires judgment');
  problems.forEach(p => console.log('  - ' + p));
  process.exitCode = problems.length ? 1 : 0;
}
function build(v, dir) {
  if (v !== 'B') throw new Error('A build is NOT available: requires original hand-built glyphs. No fallback to rejected A2');
  const destination = resolve(dir || 'xiwang-poster-output');
  const py = spawnSync('python3', [join(root, 'scripts/xiwang/build-engraved-b.py'), '--outdir', destination, '--version', 'v7'], { cwd:root, encoding:'utf8', env:process.env, timeout:120000, maxBuffer:8*1024*1024 });
  if (py.error || py.status !== 0) throw new Error('Actual Python SVG build failed: ' + String(py.stderr || py.error?.message || py.stdout));
  const svg = join(destination, 'xiwang-poster-b-v7.svg');
  if (!existsSync(svg)) throw new Error('Generator did not create native SVG: '+svg);
  console.log(String(py.stdout).trim());
  const png = join(destination, 'xiwang-poster-b-v7.png');
  const ink = spawnSync('inkscape', [svg, '--export-width=1000', '--export-filename='+png], {cwd:root,encoding:'utf8',timeout:60000,maxBuffer:8*1024*1024});
  if (ink.error || ink.status !== 0 || !existsSync(png)) {
    console.warn('Inkscape preview unavailable; SVG is valid output but browser/visual QA is still required. ' + String(ink.stderr || ink.error?.message || ''));
  } else console.log('Inkscape PNG proof: ' + png);
  console.log('Tool execution occurred. This is still a DRAFT artistic experiment; never mark review approved automatically.');
}

function main() {
  const [action, arg, arg2] = process.argv.slice(2);
  if (action === 'verify') { if (!arg) throw new Error('verify RECEIPT.json'); return verify(resolve(arg)); }
  const v = String(arg || '').toUpperCase();
  if (!variants.has(v)) throw new Error('usage: plan a|b, build b [OUTDIR], init a|b RECEIPT.json, verify RECEIPT.json');
  if (action === 'plan') return plan(v);
  if (action === 'build') return build(v, arg2);
  if (action === 'init') { if (!arg2) throw new Error('init a|b RECEIPT.json'); return init(v, resolve(arg2)); }
  throw new Error('usage: plan a|b, init a|b RECEIPT.json, verify RECEIPT.json');
}
try { main(); } catch (e) { console.error(e.message); process.exitCode = 2; }
