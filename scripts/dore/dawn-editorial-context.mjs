#!/usr/bin/env node

const arr = value => Array.isArray(value) ? value : value == null ? [] : [value];
const compact = values => values.map(value => String(value || '').trim()).filter(Boolean);

export function deriveDawnEditorialRequests(resources) {
  const theme = resources?.weekly_theme || {};
  const morningStars = arr(resources?.resources).filter(resource => resource?.morning_star === true);
  const content = compact([
    theme.title_en,
    theme.title,
    theme.description,
    ...morningStars.flatMap(resource => [
      resource.name_en,
      resource.name,
      resource.description,
      resource.recommendation,
      ...arr(resource.collections),
      ...arr(resource.use_cases),
    ]),
  ]).join(' · ');

  const scriptureRefs = compact([
    ...arr(theme.scripture_refs),
    ...morningStars.flatMap(resource => arr(resource.scripture_refs)),
  ]);

  const visual = compact([
    ...arr(theme.visual_context),
    ...morningStars.flatMap(resource => arr(resource.visual_context)),
  ]);

  return [{
    id: 'dawn-library-featured',
    label: theme.title || 'Editorial Focus',
    contextSource: 'resources.weekly_theme+morning_stars',
    input: {
      content,
      w: 'WATCH',
      scriptureRefs,
      visual,
      aspectRatio: '8:5',
      surfacePreset: 'card-8x5',
      operation: 'display',
      authorityMinimum: 'C',
      limit: 3,
    },
  }];
}
