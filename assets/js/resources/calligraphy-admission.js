const BLOCKED_TITLE_PATTERNS = [/金剛經/u, /金刚经/u, /道德經/u, /道德经/u];
const BUDDHIST_TEMPLE_PATTERNS = [/佛寺/u, /寺院/u, /寺廟/u, /寺庙/u, /禪寺/u, /禅寺/u, /寺額/u, /寺额/u];

export function evaluateCalligraphyAdmission(work = {}) {
  const title = String(work.title || '');
  const normalizedTitle = String(work.normalizedTitle || title);
  const subject = String(work.subject || '');
  const commissionContext = String(work.commissionContext || '');
  const provenanceContext = String(work.provenanceContext || '');
  const primaryContent = String(work.primaryContent || '');
  const titleText = `${title}\n${normalizedTitle}`;
  const contextText = `${subject}\n${commissionContext}\n${provenanceContext}\n${primaryContent}`;

  if (BLOCKED_TITLE_PATTERNS.some(pattern => pattern.test(titleText))) {
    return { admitted: false, reason: 'excluded-title' };
  }
  if (BUDDHIST_TEMPLE_PATTERNS.some(pattern => pattern.test(contextText))) {
    return { admitted: false, reason: 'excluded-buddhist-temple-context' };
  }
  return { admitted: true, reason: 'policy-pass' };
}

export function requireCalligraphyAdmission(work) {
  const result = evaluateCalligraphyAdmission(work);
  if (!result.admitted) throw new Error(`Calligraphy admission rejected: ${result.reason}`);
  return work;
}
