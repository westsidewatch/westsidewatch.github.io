const ACTION_BY_DISPOSITION = Object.freeze({
  'skill-candidate': 'create-or-improve-skill',
  'transfer-candidate': 'improve-skill-family',
  'principle-candidate': 'propose-core-principle'
});

export function generateSkillCandidate(pattern, registry = []) {
  const action = ACTION_BY_DISPOSITION[pattern?.disposition];
  if (!action) return null;

  const capabilities = new Set(pattern.capabilities || []);
  const related = registry.filter(entry => capabilities.has(entry.id));
  const existing = related.filter(entry => entry.kind === 'skill');
  const siblings = findSiblings(existing, registry);

  let mode = action;
  if (pattern.disposition === 'skill-candidate') {
    mode = existing.length ? 'improve-existing-skill' : 'create-new-skill';
  }

  return {
    id: `candidate:${pattern.key}`,
    sourcePattern: pattern.key,
    mode,
    targets: existing.map(entry => entry.id).sort(),
    siblingSkills: siblings.map(entry => entry.id).sort(),
    relatedCapabilities: [...capabilities].sort(),
    evidence: [...(pattern.observationIds || [])],
    requiredNextStage: 'exploration-sandbox',
    authority: {
      canonical: false,
      mayWriteRegistry: false,
      mayRewriteHumanAuthority: false,
      requiresIndependentEvaluation: true
    }
  };
}

function findSiblings(entries, registry) {
  const families = new Set(entries.map(entry => entry.family).filter(Boolean));
  if (!families.size) return [];
  return registry.filter(entry => entry.kind === 'skill' && families.has(entry.family));
}
