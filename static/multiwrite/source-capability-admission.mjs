const ENVELOPE_SCHEMA = 'dore.source-capability-envelope.v1';
const ADMISSION_SCHEMA = 'dore.multiwrite-source-capability-admission.v1';

const BASE_OPERATION = {
  rehost: 'read',
  redistribute: 'read',
  'material-transform': 'extract'
};
const RIGHTS_GATED = new Set(['rehost', 'redistribute', 'material-transform']);
const EDITORIAL_GATED = new Set(['rehost', 'material-transform', 'publish']);

function list(value) {
  return Array.isArray(value) ? value.map(String) : [];
}

function explicitPermission(admission, use) {
  return admission?.admitted === true && list(admission?.permissions).includes(use);
}

function evaluateSourceUse(row = {}, index = 0) {
  const use = String(row.use || 'cite');
  const envelope = row.envelope || {};
  const sourceId = String(row.id || envelope.sourcePointer || `source-${index + 1}`);
  const operations = list(envelope.operations);
  const requiredOperation = BASE_OPERATION[use] || use;

  if (envelope.schema !== ENVELOPE_SCHEMA || envelope.ok !== true) {
    return { sourceId, use, status: 'blocked', reason: 'invalid-capability-envelope' };
  }
  if (envelope.authority?.canonicalIdentityAuthority === true || envelope.authority?.envelopeAuthority === true) {
    return { sourceId, use, status: 'blocked', reason: 'source-authority-boundary-violated' };
  }
  if (envelope.editorialBoundary?.sourceContentMayBeRewrittenSilently !== false) {
    return { sourceId, use, status: 'blocked', reason: 'editorial-authority-unclear' };
  }
  if (envelope.runtimeBoundary?.required === true) {
    return {
      sourceId,
      use,
      status: 'deferred',
      reason: 'runtime-capability-required',
      runtimeMode: envelope.runtimeBoundary?.mode || null
    };
  }
  if (!operations.includes(requiredOperation)) {
    return { sourceId, use, status: 'blocked', reason: `operation-not-admitted:${requiredOperation}` };
  }
  if (RIGHTS_GATED.has(use) && !explicitPermission(row.rightsAdmission, use)) {
    return { sourceId, use, status: 'blocked', reason: `rights-admission-required:${use}` };
  }
  if (EDITORIAL_GATED.has(use) && !explicitPermission(row.editorialAdmission, use)) {
    return { sourceId, use, status: 'blocked', reason: `editorial-admission-required:${use}` };
  }

  return {
    sourceId,
    use,
    status: 'admitted',
    access: envelope.access?.preferred || null,
    provenance: {
      sourcePointer: envelope.sourcePointer || null,
      probeSchema: envelope.provenance?.probeSchema || null
    }
  };
}

export function admitSourceUses(sourceUses = []) {
  const rows = (Array.isArray(sourceUses) ? sourceUses : []).map(evaluateSourceUse);
  const blocked = rows.filter(row => row.status === 'blocked').length;
  const deferred = rows.filter(row => row.status === 'deferred').length;
  const admitted = rows.filter(row => row.status === 'admitted').length;
  return {
    schema: ADMISSION_SCHEMA,
    status: blocked ? 'blocked' : deferred ? 'deferred' : 'admitted',
    counts: { total: rows.length, admitted, deferred, blocked },
    rows,
    policy: {
      envelopeAuthority: false,
      publicArtifactPersistence: false,
      rightsClaimsAreNotAdmission: true,
      editorialCanonRequiredForTransform: true,
      providerSpecificRoutingForbidden: true
    }
  };
}

export { ADMISSION_SCHEMA, ENVELOPE_SCHEMA };
