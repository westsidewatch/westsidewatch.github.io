import fs from 'node:fs';
import { buildBookIntent } from '../static/multiwrite/book-model.mjs';

const project = JSON.parse(fs.readFileSync(new URL('../data/publishing/tian-guo-yu-yan.book-intent.v1.json', import.meta.url), 'utf8'));
const manifest = JSON.parse(fs.readFileSync(new URL('../data/publishing/projects.manifest.v1.json', import.meta.url), 'utf8'));
const sourceAuthority = JSON.parse(fs.readFileSync(new URL('../data/publishing/tian-guo-yu-yan.source-authority.v1.json', import.meta.url), 'utf8'));

if (project.schema !== 'dore.book-project.v1') throw new Error('invalid project schema');
if (project.id !== 'book.tian-guo-yu-yan') throw new Error('invalid project id');
if (project.development?.targetChineseCharacters !== 100000) throw new Error('100k target missing');
if (project.development?.writingCapability !== 'writing.westside-dimensional-journalism') throw new Error('Westside writing capability missing');
if (project.development?.publishingCapability !== 'publishing.book-compile') throw new Error('book compile capability missing');
if (project.development?.mayRewriteThesis !== false) throw new Error('author thesis rewrite boundary missing');
if (project.development?.noSilentTruncation !== true) throw new Error('no-silent-truncation boundary missing');

const row = manifest.projects.find(item => item.id === project.id);
if (!row) throw new Error('project not registered in publishing manifest');
if (row.consumer !== 'multiwrite' || row.entryAction !== '成書') throw new Error('Multiwrite publishing route missing');

const intent = buildBookIntent(project.source);
if (intent.category !== 'narrative-theological-popular-nonfiction') throw new Error('genre contract missing');
if (!intent.thesis || intent.thesis !== project.source.bookIntent.thesis) throw new Error('thesis authority drift');
if (intent.readingMode !== 'continuous-narrative') throw new Error('narrative reading mode missing');

if (sourceAuthority.schema !== 'dore.book-source-authority.v1') throw new Error('source authority map missing');
if (sourceAuthority.projectId !== project.id) throw new Error('source authority project mismatch');
if (sourceAuthority.canonicalSource?.sourceRole !== 'canonical-manuscript-source') throw new Error('canonical manuscript role missing');
if (sourceAuthority.supportingSource?.sourceRole !== 'evidence-and-research-layer') throw new Error('research paper role boundary missing');
if (sourceAuthority.supportingSource?.mayOverrideCanonicalManuscript !== false) throw new Error('research paper may override manuscript');
if (sourceAuthority.supportingSource?.mayOverrideAuthorThesis !== false) throw new Error('research paper may override author thesis');
if (sourceAuthority.census?.exactHanCharacters !== null) throw new Error('unverified exact census admitted');
if (sourceAuthority.census?.sourceLabelApproxChineseCharacters !== 54000) throw new Error('source-label approximation missing');
if (sourceAuthority.authority?.observedStructureMayNotBePromotedToFrozenToc !== true) throw new Error('observed chapter graph freeze boundary missing');
if (!Array.isArray(sourceAuthority.observedChapterGraph?.nodes) || sourceAuthority.observedChapterGraph.nodes.length !== 14) throw new Error('observed chapter graph incomplete');

console.log(JSON.stringify({
  schema: 'dore.book-project-admission-acceptance.v1',
  status: 'PASS',
  project: project.id,
  targetChineseCharacters: project.development.targetChineseCharacters,
  route: `${row.consumer}:${row.entryAction}`,
  sourceStage: sourceAuthority.status,
  observedChapterNodes: sourceAuthority.observedChapterGraph.nodes.length,
  checks: [
    'publishing-manifest-registration',
    'canonical-book-intent',
    '100k-book-target',
    'narrative-theological-popular-nonfiction-genre',
    'westside-writing-capability',
    'book-compile-capability',
    'author-thesis-authority',
    'no-silent-truncation',
    'canonical-manuscript-vs-research-source-boundary',
    'no-false-exact-census',
    'observed-chapter-graph-not-frozen-toc'
  ]
}, null, 2));
