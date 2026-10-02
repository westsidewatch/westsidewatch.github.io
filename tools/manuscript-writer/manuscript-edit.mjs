import crypto from 'node:crypto';

/**
 * One-call manuscript edit.
 * Public surface: manuscriptEdit({ octokit, owner, repo, path, find, replace, branch, message })
 *
 * Internally performs the whole transaction:
 * latest read -> unique match -> replacement -> diff validation -> one GitHub commit.
 * Nothing is written unless every guard passes.
 */
export async function manuscriptEdit({
  octokit,
  owner,
  repo,
  path,
  find,
  replace,
  branch = 'main',
  message = 'edit(manuscript): atomic text update',
  expectedHash = null,
}) {
  if (!octokit) throw new Error('octokit is required');
  for (const [name, value] of Object.entries({ owner, repo, path, find, replace })) {
    if (typeof value !== 'string' || (name !== 'replace' && value.length === 0)) {
      throw new Error(`${name} must be a ${name === 'replace' ? 'string' : 'non-empty string'}`);
    }
  }

  const current = await octokit.rest.repos.getContent({ owner, repo, path, ref: branch });
  if (Array.isArray(current.data) || current.data.type !== 'file' || !current.data.content) {
    throw new Error(`Not a UTF-8 file: ${path}`);
  }

  const before = Buffer.from(current.data.content.replace(/\n/g, ''), 'base64').toString('utf8');
  const beforeHash = sha256(before);
  if (expectedHash && expectedHash !== beforeHash) {
    throw new Error(`Stale manuscript: expected ${expectedHash}, got ${beforeHash}`);
  }

  const exact = occurrences(before, find);
  let needle = find;
  let start = exact.length === 1 ? exact[0] : -1;

  // Mature edit_file behavior: if exact matching misses, allow a conservative
  // whitespace-normalized line match, but only when it resolves uniquely.
  if (start < 0 && exact.length === 0) {
    const normalized = normalizedUniqueMatch(before, find);
    if (normalized) {
      start = normalized.start;
      needle = before.slice(normalized.start, normalized.end);
    }
  }

  if (start < 0) {
    const count = exact.length;
    throw new Error(count > 1 ? `Unsafe edit: find text occurs ${count} times` : 'Edit target not found uniquely');
  }

  const after = before.slice(0, start) + replace + before.slice(start + needle.length);
  if (after === before) return { changed: false, sha: current.data.sha, hash: beforeHash, diff: '' };

  const diff = compactDiff(before, after, path, start, needle.length, replace.length);
  if (!diff || diff.added === 0 && diff.removed === 0) throw new Error('Diff validation failed');

  // GitHub Contents API uses the latest blob SHA as an optimistic concurrency
  // guard and creates exactly one commit for this file update.
  const written = await octokit.rest.repos.createOrUpdateFileContents({
    owner,
    repo,
    path,
    branch,
    message,
    sha: current.data.sha,
    content: Buffer.from(after, 'utf8').toString('base64'),
  });

  return {
    changed: true,
    commit: written.data.commit.sha,
    sha: written.data.content?.sha || null,
    hash: sha256(after),
    diff,
  };
}

function sha256(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex');
}

function occurrences(text, needle) {
  const out = [];
  let from = 0;
  while (true) {
    const i = text.indexOf(needle, from);
    if (i < 0) return out;
    out.push(i);
    from = i + Math.max(1, needle.length);
  }
}

function normalizeLine(s) {
  return s.trim().replace(/\s+/g, ' ');
}

function normalizedUniqueMatch(text, wanted) {
  const sourceLines = text.split('\n');
  const wantedLines = wanted.split('\n');
  const n = wantedLines.length;
  const target = wantedLines.map(normalizeLine).join('\n');
  const matches = [];
  let offset = 0;
  const offsets = sourceLines.map((line) => {
    const here = offset;
    offset += line.length + 1;
    return here;
  });
  for (let i = 0; i <= sourceLines.length - n; i++) {
    if (sourceLines.slice(i, i + n).map(normalizeLine).join('\n') === target) {
      const start = offsets[i];
      const endLine = i + n - 1;
      const end = offsets[endLine] + sourceLines[endLine].length;
      matches.push({ start, end });
    }
  }
  return matches.length === 1 ? matches[0] : null;
}

function compactDiff(before, after, path, start, removedChars, addedChars) {
  const beforeLine = 1 + before.slice(0, start).split('\n').length - 1;
  const removed = before.slice(start, start + removedChars);
  const added = after.slice(start, start + addedChars);
  return {
    path,
    line: beforeLine,
    removed: removed.length ? removed : '',
    added: added.length ? added : '',
  };
}
